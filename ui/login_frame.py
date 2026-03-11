"""
GKeepSync - Login Frame
Form nhập email + App Password hoặc đăng nhập qua Browser OAuth.
"""

import customtkinter as ctk
from typing import Callable, Optional


class LoginFrame(ctk.CTkFrame):
    """Login form: email + app password/token + browser OAuth option."""

    def __init__(
        self,
        master,
        on_login: Callable[[str, str], None],
        on_browser_login: Callable[[str, str], None] = None,
        **kwargs,
    ):
        # Thiết lập nền thẻ form login thành trắng tinh cho Apple Light Theme
        kwargs.setdefault("fg_color", "white")
        kwargs.setdefault("corner_radius", 16)
        super().__init__(master, **kwargs)
        self._on_login = on_login
        self._on_browser_login = on_browser_login

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # --- Logo / Title ---
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, pady=(40, 16))

        ctk.CTkLabel(
            title_frame,
            text="🔄",
            font=ctk.CTkFont(size=52),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            title_frame,
            text="GKeepSync",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#1C1C1E"
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            title_frame,
            text="Đồng bộ Google Keep → Markdown",
            font=ctk.CTkFont(size=14),
            text_color="#8E8E93",
        ).pack()

        # --- Tab View: Browser Login vs Manual ---
        self._tabview = ctk.CTkTabview(
            self, 
            width=400, 
            height=340,
            segmented_button_selected_color="#007AFF",
            segmented_button_selected_hover_color="#005ecb",
            fg_color="transparent",
        )
        self._tabview.grid(row=1, column=0, padx=50, pady=10, sticky="ew")
        self._tabview.add("🌐 Đăng nhập qua Browser")
        self._tabview.add("🔑 Nhập Master Token")

        # ===== TAB 1: Browser Login =====
        tab_browser = self._tabview.tab("🌐 Đăng nhập qua Browser")
        tab_browser.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tab_browser, text="📧 Email", font=ctk.CTkFont(size=13, weight="bold"), text_color="#1C1C1E", anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(8, 4))

        self._browser_email = ctk.CTkEntry(
            tab_browser,
            placeholder_text="your.email@gmail.com",
            height=40,
            corner_radius=12,
            fg_color="#F2F2F7",
            border_width=0,
            text_color="#1C1C1E",
            font=ctk.CTkFont(size=14),
        )
        self._browser_email.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        # Step 1: Open browser button
        self._open_browser_btn = ctk.CTkButton(
            tab_browser,
            text="1️⃣  Mở trình duyệt đăng nhập",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._handle_open_browser,
            corner_radius=12,
            fg_color="#F2F2F7",
            text_color="#007AFF",
            hover_color="#E5E5EA",
        )
        self._open_browser_btn.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        # Step 2: Paste oauth_token
        ctk.CTkLabel(
            tab_browser,
            text='2️⃣  Dán cookie "oauth_token" từ DevTools:',
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1C1C1E",
            anchor="w",
        ).grid(row=3, column=0, sticky="w", pady=(0, 4))

        self._oauth_entry = ctk.CTkEntry(
            tab_browser,
            placeholder_text="oauth2_4/...",
            height=40,
            corner_radius=12,
            fg_color="#F2F2F7",
            border_width=0,
            text_color="#1C1C1E",
            font=ctk.CTkFont(size=14),
            show="•",
        )
        self._oauth_entry.grid(row=4, column=0, sticky="ew", pady=(0, 12))

        # Step 3: Connect
        self._browser_connect_btn = ctk.CTkButton(
            tab_browser,
            text="3️⃣  Lấy Master Token & Kết nối",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._handle_browser_connect,
            corner_radius=12,
            fg_color="#007AFF",
            text_color="white",
            hover_color="#005ecb",
        )
        self._browser_connect_btn.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        # ===== TAB 2: Manual Token =====
        tab_manual = self._tabview.tab("🔑 Nhập Master Token")
        tab_manual.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tab_manual, text="📧 Email", font=ctk.CTkFont(size=13, weight="bold"), text_color="#1C1C1E", anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(8, 4))

        self._email_entry = ctk.CTkEntry(
            tab_manual,
            placeholder_text="your.email@gmail.com",
            height=40,
            corner_radius=12,
            fg_color="#F2F2F7",
            border_width=0,
            text_color="#1C1C1E",
            font=ctk.CTkFont(size=14),
        )
        self._email_entry.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            tab_manual,
            text="🔑 Master Token",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#1C1C1E",
            anchor="w",
        ).grid(row=2, column=0, sticky="w", pady=(0, 4))

        self._token_entry = ctk.CTkEntry(
            tab_manual,
            placeholder_text="aas_et/...",
            height=40,
            corner_radius=12,
            fg_color="#F2F2F7",
            border_width=0,
            text_color="#1C1C1E",
            font=ctk.CTkFont(size=14),
            show="•",
        )
        self._token_entry.grid(row=3, column=0, sticky="ew", pady=(0, 4))

        self._show_token = ctk.CTkCheckBox(
            tab_manual,
            text="Hiện token",
            font=ctk.CTkFont(size=12),
            text_color="#8E8E93",
            command=self._toggle_token_visibility,
            height=20,
            checkbox_width=20,
            checkbox_height=20,
            border_color="#C7C7CC",
            hover_color="#005ecb",
            fg_color="#007AFF"
        )
        self._show_token.grid(row=4, column=0, sticky="w", pady=(0, 16))

        self._connect_btn = ctk.CTkButton(
            tab_manual,
            text="🔗  Kết nối",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._handle_connect,
            corner_radius=12,
            fg_color="#007AFF",
            text_color="white",
            hover_color="#005ecb",
        )
        self._connect_btn.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        # --- Status message (shared) ---
        self._status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#8E8E93",
            wraplength=350,
        )
        self._status_label.grid(row=2, column=0, pady=(4, 4))

        # --- Help Section ---
        help_frame = ctk.CTkFrame(self, fg_color="transparent")
        help_frame.grid(row=3, column=0, padx=50, pady=(0, 20))

        ctk.CTkLabel(
            help_frame,
            text="💡 Hướng dẫn đăng nhập qua Browser:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1C1C1E",
            anchor="w",
        ).pack(anchor="w")

        help_text = (
            "1. Nhập email → Bấm 'Mở trình duyệt đăng nhập'\n"
            "2. Đăng nhập tài khoản Google trong browser\n"
            "3. Mở DevTools (F12) → tab Application → Cookies\n"
            '4. Tìm cookie "oauth_token" → copy giá trị\n'
            "5. Dán vào app → Bấm 'Lấy Master Token & Kết nối'"
        )
        ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=12),
            text_color="#8E8E93",
            justify="left",
            anchor="w",
        ).pack(anchor="w", padx=(12, 0))

    # ═══════════ Browser OAuth Flow ═══════════

    def _handle_open_browser(self):
        email = self._browser_email.get().strip()
        if not email:
            self._set_status("⚠️ Vui lòng nhập email trước!", "orange")
            return
        self._set_status("🌐 Đang mở browser... Hãy đăng nhập Google!", "#3498db")
        from auth_browser import get_master_token_via_browser

        get_master_token_via_browser(email)

    def _handle_browser_connect(self):
        email = self._browser_email.get().strip()
        oauth_token = self._oauth_entry.get().strip()

        if not email:
            self._set_status("⚠️ Vui lòng nhập email!", "orange")
            return
        if not oauth_token:
            self._set_status("⚠️ Vui lòng dán oauth_token!", "orange")
            return

        self._set_status("⏳ Đang đổi oauth_token → master token...", "gray")
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
            self._set_status("⚠️ Vui lòng nhập email!", "orange")
            return
        if not token:
            self._set_status("⚠️ Vui lòng nhập Master Token!", "orange")
            return

        self._set_status("⏳ Đang kết nối...", "gray")
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
            self._connect_btn.configure(state="normal", text="🔗  Kết nối")
            self._browser_connect_btn.configure(
                state="normal", text="3️⃣  Lấy Master Token & Kết nối"
            )

    def _set_status(self, text: str, color: str = "gray"):
        self._status_label.configure(text=text, text_color=color)

    def show_error(self, message: str):
        self._set_status(f"❌ {message}", "#e74c3c")
        self.set_loading(False)

    def show_success(self, message: str):
        self._set_status(f"✅ {message}", "#2ecc71")

    def prefill(self, email: str, token: str):
        """Pre-fill credentials from saved config."""
        if email:
            self._email_entry.insert(0, email)
            self._browser_email.insert(0, email)
        if token:
            self._token_entry.insert(0, token)
            # Switch to Manual tab if we have a saved token
            self._tabview.set("🔑 Nhập Master Token")
