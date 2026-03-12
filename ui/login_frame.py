"""
GKeepSync - Login Frame
Form nhập email + App Password hoặc đăng nhập qua Browser OAuth.
(Material 3 UI Update - Logic Retained)
"""

import customtkinter as ctk
from typing import Callable, Optional
import sys
import os

# Import MaterialColors if available, otherwise define polyfills
try:
    from ui.themes.colors import MaterialColors
except ImportError:
    class MaterialColors:
        BG_CONTENT_MAC = "#F5F5F7"
        BG_CARD = "#FFFFFF"
        PRIMARY = "#0B57D0"
        PRIMARY_HOVER = "#0842A0"
        TEXT_MAIN = "#1F1F1F"
        TEXT_MUTED = "#444746"
        ERROR = "#B3261E"
        SUCCESS = "#146C2E"
        WARNING = "#B3261E"
        BORDER_LIGHT = "#E0E2E5"
        BORDER_INPUT = "#747775"


class LoginFrame(ctk.CTkFrame):
    """Login form: email + app password/token + browser OAuth option."""

    def __init__(
        self,
        master,
        on_login: Callable[[str, str], None],
        on_browser_login: Callable[[str, str], None] = None,
        **kwargs,
    ):
        kwargs["fg_color"] = kwargs.get("fg_color", MaterialColors.BG_CONTENT_MAC)
        super().__init__(master, **kwargs)
        self._on_login = on_login
        self._on_browser_login = on_browser_login

        # Configure self grid to center the card
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # --- Main Card ---
        self.card = ctk.CTkFrame(self, fg_color=MaterialColors.BG_CARD, corner_radius=16, width=420)
        self.card.grid(row=1, column=1, padx=20, pady=20)
        self.card.grid_columnconfigure(0, weight=1)

        # --- Logo / Title ---
        title_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        title_frame.grid(row=0, column=0, pady=(40, 16))

        ctk.CTkLabel(
            title_frame,
            text="GKeepSync",
            font=("Segoe UI", 32, "bold"),
            text_color=MaterialColors.PRIMARY
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            title_frame,
            text="Đồng bộ Google Keep → NotebookLM",
            font=("Segoe UI", 14),
            text_color=MaterialColors.TEXT_MUTED,
        ).pack()

        # --- Status message (shared) ---
        self._status_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Segoe UI", 13),
            text_color=MaterialColors.TEXT_MUTED,
            wraplength=350,
        )
        self._status_label.grid(row=1, column=0, pady=(4, 4))

        # --- Tab View: Browser Login vs Manual ---
        self._tabview = ctk.CTkTabview(
            self.card, 
            width=360, 
            height=340,
            fg_color="transparent",
            segmented_button_fg_color=MaterialColors.BG_CONTENT_MAC,
            segmented_button_selected_color=MaterialColors.PRIMARY,
            segmented_button_selected_hover_color=MaterialColors.PRIMARY_HOVER,
            segmented_button_unselected_color=MaterialColors.BG_CONTENT_MAC,
            segmented_button_unselected_hover_color=MaterialColors.BORDER_LIGHT
        )
        self._tabview.grid(row=2, column=0, padx=30, pady=(10, 20), sticky="ew")
        self._tabview.add("🌐 Đăng nhập qua Browser")
        self._tabview.add("🔑 Nhập Master Token")

        # ===== TAB 1: Browser Login =====
        tab_browser = self._tabview.tab("🌐 Đăng nhập qua Browser")
        tab_browser.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tab_browser, text="📧 Email", font=("Segoe UI", 13, "bold"), text_color=MaterialColors.TEXT_MAIN, anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(8, 4))

        self._browser_email = ctk.CTkEntry(
            tab_browser,
            placeholder_text="your.email@gmail.com",
            height=40,
            corner_radius=8,
            fg_color="white",
            border_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN,
            font=("Segoe UI", 14),
        )
        self._browser_email.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        # Step 1: Open browser button
        self._open_browser_btn = ctk.CTkButton(
            tab_browser,
            text="1. Mở trình duyệt đăng nhập",
            height=40,
            font=("Segoe UI", 14, "bold"),
            command=self._handle_open_browser,
            corner_radius=8,
            fg_color=MaterialColors.BG_CONTENT_MAC,
            text_color=MaterialColors.PRIMARY,
            hover_color=MaterialColors.BORDER_LIGHT,
        )
        self._open_browser_btn.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        # Step 2: Paste oauth_token
        ctk.CTkLabel(
            tab_browser,
            text='2. Dán cookie "oauth_token" từ DevTools:',
            font=("Segoe UI", 12, "bold"),
            text_color=MaterialColors.TEXT_MAIN,
            anchor="w",
        ).grid(row=3, column=0, sticky="w", pady=(0, 4))

        self._oauth_entry = ctk.CTkEntry(
            tab_browser,
            placeholder_text="oauth2_4/...",
            height=40,
            corner_radius=8,
            fg_color="white",
            border_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN,
            font=("Segoe UI", 14),
            show="•",
        )
        self._oauth_entry.grid(row=4, column=0, sticky="ew", pady=(0, 12))

        # Step 3: Connect
        self._browser_connect_btn = ctk.CTkButton(
            tab_browser,
            text="3. Lấy Master Token & Kết nối",
            height=44,
            font=("Segoe UI", 15, "bold"),
            command=self._handle_browser_connect,
            corner_radius=8,
            fg_color=MaterialColors.PRIMARY,
            text_color="white",
            hover_color=MaterialColors.PRIMARY_HOVER,
        )
        self._browser_connect_btn.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        # ===== TAB 2: Manual Token =====
        tab_manual = self._tabview.tab("🔑 Nhập Master Token")
        tab_manual.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tab_manual, text="📧 Email", font=("Segoe UI", 13, "bold"), text_color=MaterialColors.TEXT_MAIN, anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(8, 4))

        self._email_entry = ctk.CTkEntry(
            tab_manual,
            placeholder_text="your.email@gmail.com",
            height=40,
            corner_radius=8,
            fg_color="white",
            border_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN,
            font=("Segoe UI", 14),
        )
        self._email_entry.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            tab_manual,
            text="🔑 Master Token",
            font=("Segoe UI", 13, "bold"),
            text_color=MaterialColors.TEXT_MAIN,
            anchor="w",
        ).grid(row=2, column=0, sticky="w", pady=(0, 4))

        self._token_entry = ctk.CTkEntry(
            tab_manual,
            placeholder_text="aas_et/...",
            height=40,
            corner_radius=8,
            fg_color="white",
            border_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN,
            font=("Segoe UI", 14),
            show="•",
        )
        self._token_entry.grid(row=3, column=0, sticky="ew", pady=(0, 4))

        self._show_token = ctk.CTkCheckBox(
            tab_manual,
            text="Hiện token",
            font=("Segoe UI", 12),
            text_color=MaterialColors.TEXT_MUTED,
            command=self._toggle_token_visibility,
            height=20,
            checkbox_width=20,
            checkbox_height=20,
            border_color=MaterialColors.BORDER_LIGHT,
            hover_color=MaterialColors.PRIMARY_HOVER,
            fg_color=MaterialColors.PRIMARY
        )
        self._show_token.grid(row=4, column=0, sticky="w", pady=(0, 16))

        self._connect_btn = ctk.CTkButton(
            tab_manual,
            text="🔗 Kết nối",
            height=44,
            font=("Segoe UI", 15, "bold"),
            command=self._handle_connect,
            corner_radius=8,
            fg_color=MaterialColors.PRIMARY,
            text_color="white",
            hover_color=MaterialColors.PRIMARY_HOVER,
        )
        self._connect_btn.grid(row=5, column=0, sticky="ew", pady=(0, 8))


        # --- Help Section ---
        help_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        help_frame.grid(row=3, column=0, padx=30, pady=(0, 30))

        ctk.CTkLabel(
            help_frame,
            text="💡 Hướng dẫn đăng nhập qua Browser (Fallback):",
            font=("Segoe UI", 12, "bold"),
            text_color=MaterialColors.TEXT_MAIN,
            anchor="w",
        ).pack(anchor="w")

        help_text = (
            "Tiện ích mở rộng Chrome (Extension) sẽ tự bắt token khi\n"
            "đăng nhập thành công và đẩy thẳng vào App (Không cần dán).\n"
            "Nếu tiện ích lỗi, hãy copy cookie 'oauth_token' dán vào Tab 1."
        )
        ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=("Segoe UI", 12),
            text_color=MaterialColors.TEXT_MUTED,
            justify="left",
            anchor="w",
        ).pack(anchor="w", padx=(12, 0))

    # ═══════════ Browser OAuth Flow ═══════════

    def _handle_open_browser(self):
        email = self._browser_email.get().strip()
        if not email:
            self._set_status("⚠️ Vui lòng nhập email trước!", MaterialColors.WARNING)
            return
        self._set_status("🌐 Đang mở browser... Hãy đăng nhập Google!", MaterialColors.PRIMARY)
        from auth_browser import get_master_token_via_browser

        get_master_token_via_browser(email)

    def _handle_browser_connect(self):
        email = self._browser_email.get().strip()
        oauth_token = self._oauth_entry.get().strip()

        if not email:
            self._set_status("⚠️ Vui lòng nhập email!", MaterialColors.WARNING)
            return
        if not oauth_token:
            self._set_status("⚠️ Vui lòng dán oauth_token!", MaterialColors.WARNING)
            return

        self._set_status("⏳ Đang đổi oauth_token → master token...", MaterialColors.TEXT_MUTED)
        self._browser_connect_btn.configure(
            state="disabled", text="⏳ Đang xử lý..."
        )

        if self._on_browser_login:
            self._on_browser_login(email, oauth_token)

    # ═══════════ Manual Token Flow ═══════════

    def _toggle_token_visibility(self):
        if self._show_token.get():
            self._token_entry.configure(show="")
        else:
            self._token_entry.configure(show="•")

    def _handle_connect(self):
        email = self._email_entry.get().strip()
        token = self._token_entry.get().strip()

        if not email:
            self._set_status("⚠️ Vui lòng nhập email!", MaterialColors.WARNING)
            return
        if not token:
            self._set_status("⚠️ Vui lòng nhập Master Token!", MaterialColors.WARNING)
            return

        self._set_status("⏳ Đang kết nối...", MaterialColors.TEXT_MUTED)
        self._connect_btn.configure(state="disabled", text="⏳ Đang kết nối...")
        self._on_login(email, token)

    # ═══════════ Public Methods ═══════════

    def set_loading(self, loading: bool):
        if loading:
            self._connect_btn.configure(state="disabled", text="⏳ Đang kết nối...")
            self._browser_connect_btn.configure(
                state="disabled", text="⏳ Đang xử lý..."
            )
        else:
            self._connect_btn.configure(state="normal", text="🔗 Kết nối")
            self._browser_connect_btn.configure(
                state="normal", text="3️⃣ Lấy Master Token & Kết nối"
            )

    def _set_status(self, text: str, color: str = MaterialColors.TEXT_MUTED):
        self._status_label.configure(text=text, text_color=color)

    def show_error(self, message: str):
        self._set_status(f"❌ {message}", MaterialColors.ERROR)
        self.set_loading(False)

    def show_success(self, message: str):
        self._set_status(f"✅ {message}", MaterialColors.SUCCESS)

    def prefill(self, email: str, token: str):
        """Pre-fill credentials from saved config."""
        if email:
            self._email_entry.insert(0, email)
            self._browser_email.insert(0, email)
        if token:
            self._token_entry.insert(0, token)
            # Switch to Manual tab if we have a saved token
            self._tabview.set("🔑 Nhập Master Token")

