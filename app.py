"""
GKeepSync - Main Application Window
Quản lý frame switching, threading, kết nối UI ↔ Engine.
"""

import threading
import customtkinter as ctk
from typing import Callable, Optional
from auth_browser import exchange_oauth_for_master

from config import Config
from keep_client import KeepClient
from sync_engine import SyncEngine
from token_server import TokenServer
from ui.login_frame import LoginFrame
from ui.main_frame import MainFrame
from ui.components import NotificationToast
from utils.logger import logger


class GKeepSyncApp(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # --- Config ---
        self._config = Config()
        self._keep = KeepClient()
        self._sync = SyncEngine(self._keep)

        # Wire sync callbacks
        self._sync.on_sync_start = self._on_sync_start
        self._sync.on_sync_progress = self._on_sync_progress
        self._sync.on_sync_complete = self._on_sync_complete
        self._sync.on_sync_error = self._on_sync_error

        # Start token receiver server (for Chrome Extension)
        self._token_server = TokenServer(
            on_token_received=self._on_extension_token
        )
        self._token_server.start()

        # --- Window Setup ---
        self.title("GKeepSync")
        self.geometry(self._config.get("window_geometry", "900x650"))
        self.minsize(750, 550)

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self._login_frame = LoginFrame(
            self,
            on_login=self._handle_login,
            on_browser_login=self._handle_browser_login,
        )

        self._main_frame = MainFrame(
            self,
            on_sync=self._handle_sync,
            on_auto_sync_toggle=self._handle_auto_sync_toggle,
            on_folder_change=self._handle_folder_change,
            on_logout=self._handle_logout,
        )

        # Check for saved credentials
        if self._config.has_credentials:
            logger.info("Found saved credentials, attempting auto-login...")
            self._login_frame.prefill(
                self._config.get("email", ""),
                self._config.get("master_token", ""),
            )
            self._show_login()
            # Auto-login
            self.after(500, lambda: self._handle_login(
                self._config.get("email"),
                self._config.get("master_token"),
            ))
        else:
            self._show_login()

    def _show_login(self):
        """Show login frame."""
        self._main_frame.grid_forget()
        self._login_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    def _show_main(self):
        """Show main frame."""
        self._login_frame.grid_forget()
        self._main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Set output folder
        self._main_frame.set_folder(str(self._config.get_output_folder()))

        # Load labels
        labels = self._keep.get_labels()
        self._main_frame.set_labels(labels)

        # Update status
        last_sync = self._sync.get_last_sync_time()
        self._main_frame.update_status(f"✅ Đã kết nối | Last sync: {last_sync}")
        logger.info("Switched to main frame, labels loaded: %d", len(labels))

        # Pre-fill NotebookLM settings
        # Set states
        if getattr(self._main_frame, 'home_view', None):
            if self._config.get("auto_sync_enabled"):
                try:
                    self._main_frame.home_view._auto_sync_switch.select()
                except AttributeError:
                    pass

            if self._config.get("nlm_sync_enabled"):
                try:
                    self._main_frame.nlm_view.nlm_switch.select()
                except AttributeError:
                    pass
        nlm_id = self._config.get("nlm_notebook_id", "")
        if nlm_id:
            self._main_frame._nlm_id_var.set(nlm_id)

    # ═══════════════════════════════════════════
    # LOGIN
    # ═══════════════════════════════════════════

    def _handle_login(self, email: str, token: str):
        """Handle login - runs in background thread."""
        self._login_frame.set_loading(True)

        def _do_login():
            success, msg = self._keep.login(email, token)
            # Schedule UI update on main thread
            self.after(0, lambda: self._on_login_result(success, msg, email, token))

        thread = threading.Thread(target=_do_login, daemon=True)
        thread.start()

    def _on_login_result(self, success: bool, msg: str, email: str, token: str):
        """Handle login result on main thread."""
        if success:
            logger.info("Login successful for %s", email)
            self._login_frame.show_success(msg)

            # Save credentials
            self._config.set("email", email)
            self._config.set("master_token", token)
            self._config.save()

            # Switch to main frame
            self.after(500, self._show_main)
        else:
            logger.error("Login failed: %s", msg)
            self._login_frame.show_error(msg)

    # ═══════════════════════════════════════════
    # BROWSER OAUTH LOGIN
    # ═══════════════════════════════════════════

    def _handle_browser_login(self, email: str, oauth_token: str):
        """Handle browser OAuth login - exchange oauth_token for master token."""
        self._login_frame.set_loading(True)

        def _do_exchange():
            success, result = exchange_oauth_for_master(email, oauth_token)
            if success:
                master_token = result
                # Now login with the master token
                login_ok, msg = self._keep.login(email, master_token)
                self.after(0, lambda: self._on_login_result(
                    login_ok, msg, email, master_token
                ))
            else:
                self.after(0, lambda: self._login_frame.show_error(result))

        thread = threading.Thread(target=_do_exchange, daemon=True)
        thread.start()

    def _on_extension_token(self, email: str, oauth_token: str) -> Optional[str]:
        """Called when Chrome Extension sends oauth_token & email to localhost server."""
        logger.info("[AppExtToken] Received token from Chrome Extension for %s, processing...", email or "(empty)")

        email = email or self._config.get("email", "") or self._login_frame._browser_email.get().strip()
        
        if not email:
            logger.warning("[AppExtToken] No email available to complete login!")
            self.after(0, lambda: self._login_frame.show_error(
                "Nhận được token từ extension nhưng bị thiếu email! Vui lòng nhập email vào ô Đăng nhập trình duyệt."
            ))
            return None

        self.after(0, lambda: self._login_frame._set_status(
            "✨ Nhận thông tin từ Extension! Đang tự động đăng nhập...", "#3498db"
        ))
        
        # Determine master token using keep_client smart rules
        # KeepClient handles oauth2_ vs aas_et internally.
        success, msg = self._keep.login(email, oauth_token)
        
        if success:
            master_token = self._keep.get_master_token()
            self.after(0, lambda: self._on_login_result(True, msg, email, master_token))
            return master_token
        else:
            self.after(0, lambda: self._on_login_result(False, msg, email, ""))
            return None

    # ═══════════════════════════════════════════
    # SYNC
    # ═══════════════════════════════════════════

    def _handle_sync(self):
        """Handle manual sync - runs in background thread."""
        labels = self._main_frame.get_selected_labels()
        date_from = self._main_frame.get_date_from()
        date_to = self._main_frame.get_date_to()

        def _do_sync():
            synced, total, msg = self._sync.sync_now(
                labels=labels, date_from=date_from, date_to=date_to
            )
            # Get notes for display
            notes = self._keep.get_notes(
                labels=labels, date_from=date_from, date_to=date_to
            )
            self.after(0, lambda: self._on_sync_done(notes))

        thread = threading.Thread(target=_do_sync, daemon=True)
        thread.start()

    def _on_sync_start(self):
        self.after(0, lambda: self._main_frame.set_syncing(True))

    def _on_sync_progress(self, title: str, current: int, total: int):
        self.after(
            0,
            lambda t=title, c=current, tot=total:
                self._main_frame.update_progress(f"📝 {t}", c, tot),
        )

    def _on_sync_complete(self, synced: int, total: int, msg: str):
        logger.info("Sync complete: %s", msg)
        self.after(0, lambda: self._main_frame.set_syncing(False))
        self.after(0, lambda: self._main_frame.reset_progress())
        self.after(0, lambda: self._show_toast(msg, "success"))

        last = self._sync.get_last_sync_time()
        next_sync = self._sync.get_next_sync_time()
        info = f"Last: {last}"
        if self._sync.is_auto_sync_running:
            info += f" | Next: {next_sync}"
        self.after(0, lambda: self._main_frame.update_sync_info(info))
        self.after(0, lambda: self._main_frame.update_status(
            f"✅ {synced}/{total} notes | {last}"
        ))

    def _on_sync_error(self, msg: str):
        logger.error("Sync error: %s", msg)
        self.after(0, lambda: self._main_frame.set_syncing(False))

        # Check for NotebookLM auth expiration specifically
        if "Authentication expired" in msg:
            self.after(0, lambda: self._show_toast(
                "Phiên NotebookLM đã hết hạn. Vui lòng bấm 'Login NLM' để đăng nhập lại.",
                "error",
            ))
        else:
            self.after(0, lambda: self._show_toast(msg, "error"))

    def _on_sync_done(self, notes: list[dict]):
        """Update notes list after sync."""
        self._main_frame.update_notes_list(notes)

    # ═══════════════════════════════════════════
    # AUTO SYNC
    # ═══════════════════════════════════════════

    def _handle_auto_sync_toggle(self, enabled: bool, interval_minutes: int):
        if enabled:
            logger.info("Auto sync enabled: every %d minutes", interval_minutes)
            self._config.set("auto_sync_enabled", True)
            self._config.set("auto_sync_interval_minutes", interval_minutes)
            self._config.save()

            labels = self._main_frame.get_selected_labels()
            date_from = self._main_frame.get_date_from()
            date_to = self._main_frame.get_date_to()

            self._sync.start_auto_sync(
                interval_minutes, labels=labels, date_from=date_from, date_to=date_to
            )
            self._show_toast(f"Auto sync bật: mỗi {interval_minutes} phút", "info")
        else:
            logger.info("Auto sync disabled")
            self._sync.stop_auto_sync()
            self._config.set("auto_sync_enabled", False)
            self._config.save()
            self._show_toast("Auto sync đã tắt", "info")

    # ═══════════════════════════════════════════
    # NOTEBOOKLM
    # ═══════════════════════════════════════════

    def _handle_nlm_toggle(self, enabled: bool):
        self._config.set("nlm_sync_enabled", enabled)
        self._config.save()
        state = "bật" if enabled else "tắt"
        logger.info("NotebookLM sync %s", state)
        self._show_toast(f"NotebookLM sync đã {state}", "info")

    def _handle_nlm_id_change(self, notebook_id: str):
        self._config.set("nlm_notebook_id", notebook_id)
        self._config.save()
        logger.info("NotebookLM notebook ID set to: %s", notebook_id)

    def _handle_nlm_login(self):
        self._show_toast("Đang mở trình duyệt để đăng nhập NotebookLM...", "info")
        
        def _do_login():
            import subprocess
            from utils.nlm_worker import _UV_NLM_PYTHON
            try:
                # Build command to run nlm login
                if _UV_NLM_PYTHON.exists():
                    cmd = [
                        str(_UV_NLM_PYTHON), "-c",
                        "import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8'); from notebooklm_tools.cli.main import cli_main; cli_main()",
                        "login"
                    ]
                else:
                    cmd = ["nlm", "login"]
                
                # We need to show window so user can interact if there are prompts, 
                # but nlm login usually opens the browser directly.
                env = __import__("os").environ.copy()
                env["PYTHONUTF8"] = "1"
                env["PYTHONIOENCODING"] = "utf-8"
                
                logger.info("[NLM] Running login command...")
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    encoding='utf-8', 
                    env=env,
                    # CREATE_NO_WINDOW so terminal doesn't pop up briefly, since browser will open
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                
                # Check if it succeeded
                if result.returncode == 0 or "Authenticating profile" in result.stdout or "Authentication Error" not in result.stderr:
                     self.after(0, lambda: self._show_toast("Đăng nhập NotebookLM thành công!", "success"))
                else:
                     logger.error("[NLM] Login failed: %s %s", result.stdout, result.stderr)
                     self.after(0, lambda: self._show_toast("Đăng nhập NotebookLM thất bại. Vui lòng thử lại.", "error"))

            except Exception as exc:
                logger.error("[NLM] Login error: %s", exc)
                self.after(0, lambda: self._show_toast(f"Lỗi đăng nhập NLM: {exc}", "error"))

        thread = threading.Thread(target=_do_login, daemon=True)
        thread.start()

    # ═══════════════════════════════════════════
    # FOLDER
    # ═══════════════════════════════════════════

    def _handle_folder_change(self, folder: str):
        self._config.set("output_folder", folder)
        self._config.save()
        logger.info("Output folder changed to: %s", folder)

    # ═══════════════════════════════════════════
    # LOGOUT
    # ═══════════════════════════════════════════

    def _handle_logout(self):
        self._sync.stop_auto_sync()
        self._config.set("email", "")
        self._config.set("master_token", "")
        self._config.save()
        logger.info("Logged out")
        self._show_login()

    # ═══════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════

    def _show_toast(self, message: str, toast_type: str = "info"):
        toast = NotificationToast(self, message, toast_type, duration=4000)
        toast.place(relx=0.5, rely=0.02, anchor="n")

    def _on_close(self):
        """Handle window close."""
        self._sync.stop_auto_sync()
        self._sync._nlm_worker.stop()
        self._token_server.stop()
        # Save window geometry
        self._config.set("window_geometry", self.geometry())
        self._config.save()
        self.destroy()
