import customtkinter as ctk
from typing import Callable

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
        self.grid_rowconfigure(2, weight=1)

        row = 0
        ctk.CTkLabel(
            self, text="📓 NotebookLM", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=row, column=0, padx=20, pady=(20, 10), sticky="w")
        row += 1

        # NLM Controls
        nlm_ctrl = ctk.CTkFrame(self, fg_color="#F5F5F7", corner_radius=12)
        nlm_ctrl.grid(row=row, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(
            nlm_ctrl, text="📓 NotebookLM:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1C1C1E"
        ).pack(side="left", padx=(16, 8), pady=16)

        self.nlm_switch = ctk.CTkSwitch(
            nlm_ctrl,
            text="Sync",
            font=ctk.CTkFont(size=13),
            command=on_nlm_toggle,
            width=60,
        )
        self.nlm_switch.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            nlm_ctrl, text="Notebook ID:", font=ctk.CTkFont(size=12), text_color="#8E8E93"
        ).pack(side="left", padx=(16, 4))

        self.nlm_id_entry = ctk.CTkEntry(
            nlm_ctrl,
            textvariable=nlm_id_var,
            height=36,
            width=220,
            corner_radius=8,
            placeholder_text="Paste notebook ID here",
            font=ctk.CTkFont(size=12),
            fg_color="#FFFFFF",
            border_color="#D1D1D6"
        )
        self.nlm_id_entry.pack(side="left", padx=(0, 16))
        self.nlm_id_entry.bind("<FocusOut>", lambda e: on_nlm_id_change())

        # Login button
        self.nlm_login_btn = ctk.CTkButton(
            nlm_ctrl,
            text="Đăng nhập NLM",
            width=120,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=on_nlm_login,
            fg_color="#007AFF",
            hover_color="#0056B3",
            text_color="#FFFFFF"
        )
        self.nlm_login_btn.pack(side="left", padx=(0, 12))

        # Fetch Notebooks button
        self.fetch_nb_btn = ctk.CTkButton(
            nlm_ctrl,
            text="Tải Notebooks",
            width=120,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#34C759",
            hover_color="#28A745",
            text_color="#FFFFFF",
            command=on_nlm_fetch_notebooks
        )
        self.fetch_nb_btn.pack(side="left", padx=(0, 16))

        # Content area (Browser 2 col)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left: Notebooks
        self.nb_scroll = ctk.CTkScrollableFrame(
            content_frame, 
            label_text="📚 My Notebooks", 
            label_font=ctk.CTkFont(size=14, weight="bold"),
            label_text_color="#1C1C1E",
            fg_color="#F5F5F7",
            corner_radius=12
        )
        self.nb_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.nb_scroll.grid_columnconfigure(0, weight=1)

        # Right: Sources
        self.src_scroll = ctk.CTkScrollableFrame(
            content_frame, 
            label_text="📄 Sources", 
            label_font=ctk.CTkFont(size=14, weight="bold"),
            label_text_color="#1C1C1E",
            fg_color="#F5F5F7",
            corner_radius=12
        )
        self.src_scroll.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.src_scroll.grid_columnconfigure(0, weight=1)
