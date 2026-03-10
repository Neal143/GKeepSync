"""
GKeepSync - Main Application Window
Quản lý frame switching, threading, kết nối UI ↔ Engine.
"""

import threading
import customtkinter as ctk


from config import Config
from keep_client import KeepClient
from sync_engine import SyncEngine
from auth_browser import exchange_oauth_for_master
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
        self._sync.on_sync_log = self._on_sync_log

        # Start token receiver server (for Chrome Extension)
        self._token_server = TokenServer(
            on_token_received=self._on_extension_token
        )
        self._token_server.start()
        
        # Start NLM Worker thread and wire its callbacks
        self._sync._nlm_worker.on_upload_success = self._on_nlm_upload_success
        self._sync._nlm_worker.on_upload_error = self._on_nlm_upload_error
        self._sync._nlm_worker.start()

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
            **self._get_mainframe_kwargs() # We inject on_filter_change dynamically here via dictionary unpacking or just plain arg
        )
        # Specifically wiring new UI component action
        self._main_frame.on_filter_change = self._handle_filter_change

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
        self._main_frame._on_nlm_toggle = self._handle_nlm_toggle
        self._main_frame._on_nlm_id_change = self._handle_nlm_id_change
        self._main_frame._on_nlm_login = self._handle_nlm_login
        self._main_frame._on_nlm_fetch_notebooks = self._fetch_nlm_notebooks
        self._main_frame._on_nlm_fetch_sources = self._fetch_nlm_sources
        
        if self._config.get("nlm_sync_enabled", False):
            self._main_frame.nlm_view.nlm_switch.select()
        nlm_id = self._config.get("nlm_notebook_id", "")
        if nlm_id:
            self._main_frame._nlm_id_var.set(nlm_id)

        # Load initial notes in background
        def _fetch_initial_notes():
            if self._keep.is_logged_in:
                notes = self._keep.get_notes()
                self.after(0, lambda: self._on_sync_done(notes))

        threading.Thread(target=_fetch_initial_notes, daemon=True).start()

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

    def _on_extension_token(self, oauth_token: str):
        """Called when Chrome Extension sends oauth_token to localhost server."""
        logger.info("Received token from Chrome Extension, processing...")
        email = self._config.get("email", "") or self._login_frame._browser_email.get().strip()

        if not email:
            self.after(0, lambda: self._login_frame.show_error(
                "Nhận được token từ extension nhưng chưa có email! Vui lòng nhập email."
            ))
            return

        self.after(0, lambda: self._login_frame._set_status(
            "✨ Nhận token từ Extension! Đang kết nối...", "#3498db"
        ))
        self._handle_browser_login(email, oauth_token)

    def _get_mainframe_kwargs(self):
        return {}

    # ═══════════════════════════════════════════
    # SYNC
    # ═══════════════════════════════════════════

    def _handle_sync(self):
        """Called when user clicks 'Sync Now'."""
        if not self._keep.is_logged_in:
            return

        self._main_frame.set_syncing(True)
        self._main_frame.reset_progress()
        
        # Apply filters before syncing
        labels = self._main_frame.get_selected_labels()
        date_from = self._main_frame.get_date_from()
        date_to = self._main_frame.get_date_to()

        def _do_sync():
            self._sync.sync_now(labels=labels, date_from=date_from, date_to=date_to)
            # Re-fetch local payload
            if self._keep.is_logged_in:
                notes = self._keep.get_notes(labels=labels, date_from=date_from, date_to=date_to)
                self.after(0, lambda: self._on_sync_done(notes))

        threading.Thread(target=_do_sync, daemon=True).start()

    def _handle_filter_change(self):
        """Called when user changes Tag or Date filters in Keep view (Local Filter Only)"""
        if not self._keep.is_logged_in:
            return
        
        # Get target filter states
        labels = self._main_frame.get_selected_labels()
        date_from = self._main_frame.get_date_from()
        date_to = self._main_frame.get_date_to()

        def _do_filter():
            # Native SQLite fetch (no external API query is blasted)
            notes = self._keep.get_notes(
                labels=labels, date_from=date_from, date_to=date_to
            )
            self.after(0, lambda: self._on_sync_done(notes))

        thread = threading.Thread(target=_do_filter, daemon=True)
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
        self.after(0, lambda: self._show_toast(msg, "error"))

    def _on_sync_log(self, title: str, status: str, msg: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self._main_frame.append_keep_log(title, status, msg, time_str))

    def _on_nlm_upload_success(self, filename: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self._main_frame.append_nlm_log(filename, "success", "Đã upload thành công", time_str))

    def _on_nlm_upload_error(self, msg: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self._main_frame.append_nlm_log("Lỗi NLM Upload", "error", msg, time_str))

    def _on_sync_done(self, notes: list[dict]):
        """Update notes list after sync."""
        logger.info("Sync done! Passing %d notes to UI.", len(notes))
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
        def _login_thread():
            success, msg = self._sync._nlm_worker.login()
            if success:
                self.after(0, lambda: self._show_toast(msg, "success"))
                self.after(0, lambda: self._main_frame.set_nlm_login_state(True, "Đã đăng nhập"))
                # Automatically attempt to fetch notebooks if logic expects it
                self.after(0, self._fetch_nlm_notebooks)
            else:
                self.after(0, lambda: self._show_toast(msg, "error"))
                self.after(0, lambda: self._main_frame.set_nlm_login_state(False, "Đăng nhập NLM"))
            
        threading.Thread(target=_login_thread, daemon=True).start()

    def _fetch_nlm_notebooks(self):
        def _fetch():
            nbs, err = self._sync._nlm_worker.get_notebooks()
            if nbs:
                # If we successfully fetch notebooks, we are clearly logged in
                self.after(0, lambda: self._main_frame.set_nlm_login_state(True, "Đã đăng nhập"))
            self.after(0, lambda: self._main_frame.set_nlm_notebooks(nbs, err))
        threading.Thread(target=_fetch, daemon=True).start()

    def _fetch_nlm_sources(self, nb_id: str):
        def _fetch():
            srcs, err = self._sync._nlm_worker.get_sources(nb_id)
            self.after(0, lambda: self._main_frame.set_nlm_sources(srcs, err))
        threading.Thread(target=_fetch, daemon=True).start()

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
