import customtkinter as ctk
from ui.components import SyncProgressBar

class SyncView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        row = 0
        ctk.CTkLabel(
            self, text="⏱️ Lịch sử Sync", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=row, column=0, padx=20, pady=(20, 10), sticky="w")
        row += 1

        self.progress = SyncProgressBar(self)
        self.progress.grid(row=row, column=0, sticky="ew", padx=20, pady=(0, 4))
        row += 1

        # Dual Logging Area
        log_container = ctk.CTkFrame(self, fg_color="transparent")
        log_container.grid(row=row, column=0, sticky="nsew", padx=20, pady=(4, 20))
        log_container.grid_columnconfigure(0, weight=1)
        log_container.grid_columnconfigure(1, weight=1)
        log_container.grid_rowconfigure(0, weight=1)

        # Keep Log
        self.keep_log_scroll = ctk.CTkScrollableFrame(
            log_container,
            label_text="📝 Google Keep Log",
            label_font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("gray95", "gray15"),
        )
        self.keep_log_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 4))

        # NLM Log
        self.nlm_log_scroll = ctk.CTkScrollableFrame(
            log_container,
            label_text="📓 NotebookLM Log",
            label_font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("gray95", "gray15"),
        )
        self.nlm_log_scroll.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
