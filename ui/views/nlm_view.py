import customtkinter as ctk
from typing import Callable
from ui.themes.colors import MaterialColors

class NLMView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        nlm_id_var: ctk.StringVar,
        on_nlm_toggle: Callable[[], None],
        on_nlm_id_change: Callable[[], None],
        on_nlm_login: Callable[[], None],
        on_nlm_fetch_notebooks: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Make lists stretch

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_frame, text="📓 NotebookLM", font=ctk.CTkFont(size=24, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, sticky="w")

        self.nlm_login_btn = ctk.CTkButton(
            header_frame,
            text="Đăng nhập NLM",
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=MaterialColors.PRIMARY,
            text_color="#FFFFFF",
            hover_color=MaterialColors.PRIMARY_HOVER,
            command=on_nlm_login
        )
        self.nlm_login_btn.grid(row=0, column=1, sticky="e")

        # --- Settings Panel ---
        self._build_top_panel(
            nlm_id_var,
            on_nlm_toggle,
            on_nlm_id_change
        )

        # --- Lists Panel ---
        self._build_lists_panel(on_nlm_fetch_notebooks)

    def _build_top_panel(self, nlm_id_var, on_toggle, on_id_change):
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        panel.grid_columnconfigure(0, weight=1)

        # Settings Card
        settings_card = ctk.CTkFrame(panel, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT)
        settings_card.grid(row=0, column=0, sticky="nsew")
        settings_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            settings_card, text="⚙️ Cài đặt đồng bộ NLM", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, columnspan=2, padx=16, pady=(16, 8), sticky="w")

        # Row 1: Notebook ID Label and Entry
        nb_id_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        nb_id_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 8))
        nb_id_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            nb_id_frame, text="Notebook ID:", font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MUTED
        ).grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.nlm_id_entry = ctk.CTkEntry(
            nb_id_frame,
            textvariable=nlm_id_var,
            height=32,
            font=ctk.CTkFont(size=13),
            fg_color=MaterialColors.BG_CONTENT,
            text_color=MaterialColors.TEXT_MAIN,
            border_color=MaterialColors.BORDER_INPUT
        )
        self.nlm_id_entry.grid(row=0, column=1, sticky="ew")
        self.nlm_id_entry.bind("<FocusOut>", lambda e: on_id_change())
        self.nlm_id_entry.bind("<Return>", lambda e: on_id_change())

        # Row 2: Switch
        self.nlm_switch = ctk.CTkSwitch(
            settings_card,
            text="Tự động Upload",
            font=ctk.CTkFont(size=13),
            text_color=MaterialColors.TEXT_MAIN,
            progress_color=MaterialColors.PRIMARY,
            command=on_toggle
        )
        self.nlm_switch.grid(row=2, column=0, columnspan=2, padx=16, pady=(0, 16), sticky="w")


    def _build_lists_panel(self, on_fetch):
        panel = ctk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        # Left Header
        left_header = ctk.CTkFrame(panel, fg_color="transparent")
        left_header.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        left_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            left_header, text="📚 My Notebooks", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, sticky="w")

        self.fetch_nb_btn = ctk.CTkButton(
            left_header,
            text="Tải Notebooks",
            height=28,
            corner_radius=6,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=MaterialColors.BG_CONTENT,
            text_color=MaterialColors.TEXT_MAIN,
            hover_color=MaterialColors.BORDER_LIGHT,
            border_width=1,
            border_color=MaterialColors.BORDER_LIGHT,
            command=on_fetch
        )
        self.fetch_nb_btn.grid(row=0, column=1, sticky="e")

        # Right Header
        ctk.CTkLabel(
            panel, text="📄 Sources in Notebook", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=1, padx=(10, 0), pady=(0, 8), sticky="w")

        # Scrolls
        self.nb_scroll = ctk.CTkScrollableFrame(
            panel, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT
        )
        self.nb_scroll.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        self.src_scroll = ctk.CTkScrollableFrame(
            panel, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT
        )
        self.src_scroll.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        # Initial placeholder text
        ctk.CTkLabel(self.nb_scroll, text="Bấm 'Tải Notebooks' để bắt đầu", text_color=MaterialColors.TEXT_MUTED).pack(pady=40)
        ctk.CTkLabel(self.src_scroll, text="Chọn một Notebook để xem Sources", text_color=MaterialColors.TEXT_MUTED).pack(pady=40)
