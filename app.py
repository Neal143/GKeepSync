"""
GKeepSync - Main Application Window
Quản lý frame switching, threading, kết nối UI ↔ Engine.
"""

import threading
import customtkinter as ctk
from customtkinter import CTkLabel, CTkFont
from typing import Optional
from auth_browser import exchange_oauth_for_master

from config import Config
from keep_client import KeepClient
from sync_engine import SyncEngine
from token_server import TokenServer
from ui.login_frame import LoginFrame
from ui.main_frame import MainFrame
from ui.components import NotificationToast
from utils.logger import logger
from utils.nlm_worker import NLMWorker
from utils import os_utils
from ui.tray_manager import TrayManager


class GKeepSyncApp(ctk.CTk):
    """Main application window."""

    def __init__(self, start_hidden: bool = False):
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
        
        # Wire NLMWorker callbacks to update the UI Log
        self._sync._nlm_worker.on_upload_success = self._on_nlm_success
        self._sync._nlm_worker.on_upload_error = self._on_nlm_error

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
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # System Tray logic
        self._tray_manager = TrayManager(self)
        self.protocol("WM_DELETE_WINDOW", self._tray_manager.hide_to_tray)

        if start_hidden:
            self.attributes("-alpha", 0.0) # Vô hình hoàn toàn
            self.withdraw()
            self.after(50, self.withdraw) # Nhồi thêm để chống tick đầu của mainloop

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
            on_startup_toggle=self._handle_startup_toggle,
        )
        self._main_frame.on_filter_change = self._fetch_and_display_notes
        
        # Wire NLM Callbacks
        self._main_frame._on_nlm_login = self._handle_nlm_login
        self._main_frame._on_nlm_toggle = self._handle_nlm_toggle
        self._main_frame._on_nlm_id_change = self._handle_nlm_id_change
        self._main_frame._on_nlm_fetch_notebooks = self._handle_nlm_fetch_notebooks
        self._main_frame._on_nlm_fetch_sources = self._handle_nlm_fetch_sources

        # Check for saved credentials
        if self._config.has_credentials:
            logger.info("Found saved credentials, attempting auto-login...")
            self._login_frame.prefill(
                self._config.get("email", ""),
                self._config.get("master_token", ""),
            )
            
            # Auto-login
            if start_hidden:
                # Nếu chạy ngầm từ Startup thì cứ auto-login dưới nền, cất UI đi
                self._tray_manager.hide_to_tray()
                self.after(500, lambda: self._handle_login(
                    self._config.get("email"),
                    self._config.get("master_token"),
                    hidden=True
                ))
            else:
                self._show_login()
                self.after(500, lambda: self._handle_login(
                    self._config.get("email"),
                    self._config.get("master_token"),
                ))
        else:
            if start_hidden:
                # Chưa login bao giờ mà Windows gọi thì đành phải hiện lên cho User nhập
                self._show_login()
            else:
                self._show_login()

    def _show_login(self):
        """Show login frame."""
        self.attributes("-alpha", 1.0) # Đảm bảo hiện hình
        self.deiconify()
        self._main_frame.grid_forget()
        self._login_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    def _show_main(self, hidden: bool = False):
        """Show main frame."""
        self._login_frame.grid_forget()
        self._main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        if hidden:
            self.attributes("-alpha", 0.0)
            self.withdraw()
        else:
            self.attributes("-alpha", 1.0)
            self.deiconify()

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
            # Khôi phục Auto Sync Interval
            saved_interval = self._config.get("auto_sync_interval_minutes", 60)
            interval_str = f"{saved_interval} phút"
            if saved_interval == 180: interval_str = "3 giờ"
            if saved_interval == 360: interval_str = "6 giờ"
            self._main_frame._interval_var.set(interval_str)

            if self._config.get("auto_sync_enabled") and hasattr(self._main_frame.home_view, '_auto_sync_switch'):
                self._main_frame.home_view._auto_sync_switch.select()
                # Phải tự trigger hàm này để SyncEngine thực sự bắt đầu đếm giờ
                self.after(500, self._main_frame._handle_auto_sync_toggle)

            if self._config.get("nlm_sync_enabled") and hasattr(self._main_frame.nlm_view, 'nlm_switch'):
                self._main_frame.nlm_view.nlm_switch.select()

            # Khôi phục Startup Switch và đồng bộ trạng thái Registry với config
            if self._config.get("run_on_startup"):
                if hasattr(self._main_frame.home_view, '_startup_switch'):
                    self._main_frame.home_view._startup_switch.select()
                # Kích hoạt lại app trong startup list nếu chẳng may bị HĐH xoá mất
                if not os_utils.check_startup_status():
                    os_utils.enable_startup()
            else:
                # Dọn rác
                if os_utils.check_startup_status():
                    os_utils.disable_startup()
                
        nlm_id = self._config.get("nlm_notebook_id", "")
        if nlm_id:
            self._main_frame._nlm_id_var.set(nlm_id)

        # Fetch initial notes for the Keep tab
        self._fetch_and_display_notes()

        # Check NLM Auth asynchronously
        self._check_nlm_auth()

    def _check_nlm_auth(self):
        def _do_check():
            if NLMWorker.check_auth_status():
                self.after(0, lambda: self._main_frame.set_nlm_login_state(True, "Đã đăng nhập"))
        
        thread = threading.Thread(target=_do_check, daemon=True)
        thread.start()

    def _fetch_and_display_notes(self):
        """Fetch notes based on current filters and update UI."""
        # Visual feedback during loading
        if hasattr(self._main_frame, 'keep_view') and hasattr(self._main_frame.keep_view, 'notes_scroll'):
            for widget in self._main_frame.keep_view.notes_scroll.winfo_children():
                widget.destroy()
            
            CTkLabel(
                self._main_frame.keep_view.notes_scroll,
                text="⏳ Đang tải ghi chú từ Google Keep...",
                text_color="#8E8E93",
                font=CTkFont(size=14)
            ).grid(row=0, column=0, columnspan=3, pady=60)

        labels = self._main_frame.get_selected_labels()
        date_from = self._main_frame.get_date_from()
        date_to = self._main_frame.get_date_to()

        def _fetch():
            try:
                notes = self._keep.get_notes(labels=labels, date_from=date_from, date_to=date_to)
                self.after(0, lambda: self._main_frame.update_notes_list(notes))
            except Exception as e:
                logger.error("Error fetching notes: %s", e)
                self.after(0, lambda: self._main_frame.update_notes_list([]))
        
        thread = threading.Thread(target=_fetch, daemon=True)
        thread.start()

    # ═══════════════════════════════════════════
    # LOGIN
    # ═══════════════════════════════════════════

    def _handle_login(self, email: str, token: str, hidden: bool = False):
        """Handle login - runs in background thread."""
        if not hidden:
            self._login_frame.set_loading(True)

        def _do_login():
            success, msg = self._keep.login(email, token)
            # Schedule UI update on main thread
            self.after(0, lambda: self._on_login_result(success, msg, email, token, hidden))

        thread = threading.Thread(target=_do_login, daemon=True)
        thread.start()

    def _on_login_result(self, success: bool, msg: str, email: str, token: str, hidden: bool = False):
        """Handle login result on main thread."""
        if success:
            logger.info("Login successful for %s", email)
            if not hidden:
                self._login_frame.show_success(msg)

            # Save credentials
            self._config.set("email", email)
            self._config.set("master_token", token)
            self._config.save()

            # Switch to main frame
            self.after(500, lambda: self._show_main(hidden=hidden))
        else:
            logger.error("Login failed: %s", msg)
            if hidden:
                # Nếu đang ẩn mà login lỗi (VD: đổi pass), bung lên cho user biết
                self._show_window(None, None)
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

    def _on_extension_token(self, email: str, oauth_token: str) -> Optional[tuple[str, str]]:
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
            "✨ Nhận thông vị từ Extension! Đang tự động đăng nhập...", "#3498db"
        ))
        
        # Determine master token using keep_client smart rules
        # KeepClient handles oauth2_ vs aas_et internally.
        success, msg = self._keep.login(email, oauth_token)
        
        if success:
            master_token = self._keep.get_master_token()
            self.after(0, lambda: self._on_login_result(True, msg, email, master_token))
            return (master_token, email)
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

    def _on_sync_log(self, title: str, status: str, msg: str):
        from datetime import datetime
        now_str = datetime.now().strftime("%H:%M:%S")
        self.after(
            0,
            lambda t=title, s=status, m=msg, d=now_str:
                self._main_frame.append_keep_log(t, s, m, d)
        )

    def _on_nlm_success(self, filename: str):
        from datetime import datetime
        now_str = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self._main_frame.append_nlm_log(filename, "success", "Upload OK", now_str))
        
    def _on_nlm_error(self, msg: str):
        from datetime import datetime
        now_str = datetime.now().strftime("%H:%M:%S")
        self.after(0, lambda: self._main_frame.append_nlm_log("NLM Worker", "error", msg, now_str))

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
    # SYSTEM STARTUP
    # ═══════════════════════════════════════════
    
    def _handle_startup_toggle(self, enabled: bool):
        self._config.set("run_on_startup", enabled)
        self._config.save()
        if enabled:
            success = os_utils.enable_startup()
            if success:
                self._show_toast("Đã bật Khởi động cùng Windows", "success")
            else:
                self._show_toast("Lỗi khi thêm vào Startup", "error")
                # Revert UI state if failed
                if hasattr(self._main_frame.home_view, '_startup_switch'):
                    self._main_frame.home_view._startup_switch.deselect()
                self._config.set("run_on_startup", False)
                self._config.save()
        else:
            os_utils.disable_startup()
            self._show_toast("Đã tắt Khởi động cùng Windows", "info")

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
            success, msg = NLMWorker.login()
            if success:
                 self.after(0, lambda: self._show_toast(msg, "success"))
                 self.after(0, lambda: self._main_frame.set_nlm_login_state(True, "Đã đăng nhập"))
            else:
                 logger.error("[NLM] Login failed: %s", msg)
                 self.after(0, lambda: self._show_toast(f"Đăng nhập NotebookLM thất bại: {msg}", "error"))
                 self.after(0, lambda: self._main_frame.set_nlm_login_state(False, "Đăng nhập NLM"))

        thread = threading.Thread(target=_do_login, daemon=True)
        thread.start()

    def _handle_nlm_fetch_notebooks(self):
        self._show_toast("Đang tải danh sách Notebooks...", "info")
        def _do_fetch():
            nbs, err = NLMWorker.get_notebooks()
            if err:
                logger.error("[NLM] Fetch Notebooks Error: %s", err)
                self.after(0, lambda: self._main_frame.set_nlm_notebooks([], error=err))
            else:
                self.after(0, lambda: self._main_frame.set_nlm_notebooks(nbs))
                self.after(0, lambda: self._main_frame.set_nlm_login_state(True, "Đã đăng nhập"))
                
        thread = threading.Thread(target=_do_fetch, daemon=True)
        thread.start()

    def _handle_nlm_fetch_sources(self, nb_id: str):
        def _do_fetch():
            srcs, err = NLMWorker.get_sources(nb_id)
            if err:
                logger.error("[NLM] Fetch Sources Error: %s", err)
                self.after(0, lambda: self._main_frame.set_nlm_sources([], error=err))
            else:
                self.after(0, lambda: self._main_frame.set_nlm_sources(srcs))
                
        thread = threading.Thread(target=_do_fetch, daemon=True)
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
        """Handle strict window close."""
        self._sync.stop_auto_sync()
        self._sync._nlm_worker.stop()
        self._token_server.stop()
        self._tray_manager.stop()
        # Save window geometry
        self._config.set("window_geometry", self.geometry())
        self._config.save()
        self.destroy()

    # ═══════════════════════════════════════════
    # SYSTEM TRAY CONTROLLER API
    # ═══════════════════════════════════════════

    def restore_from_tray(self):
        """Được gọi bởi TrayManager khi user chọn 'Mở App'."""
        self.attributes("-alpha", 1.0)
        self.deiconify()
        self.lift()
        self.focus_force()

    def force_sync_from_tray(self):
        """Được gọi bởi TrayManager khi user chọn 'Đồng bộ ngay'."""
        self._handle_sync()

    def quit_app_entirely(self):
        """Được gọi bởi TrayManager khi user chọn 'Thoát hẳn App'."""
        self._on_close()
