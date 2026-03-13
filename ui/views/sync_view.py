import customtkinter as ctk
from ui.themes.colors import MaterialColors

class ProgressBarWrapper(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.status_lbl = ctk.CTkLabel(
            self, text="Sẵn sàng", font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MUTED
        )
        self.status_lbl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.progress_bar = ctk.CTkProgressBar(
            self,
            progress_color=MaterialColors.PRIMARY,
            fg_color=MaterialColors.BORDER_LIGHT,
            height=6,
            corner_radius=3
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)

    def update_progress(self, text: str, current: int, total: int):
        self.status_lbl.configure(text=f"{text} ({current}/{total})")
        if total > 0:
            self.progress_bar.set(current / total)
        else:
            self.progress_bar.set(0)

class SyncView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        ctk.CTkLabel(
            header_frame, text="⏳ Lịch Sử Đồng Bộ", font=ctk.CTkFont(size=24, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).pack(side="left")

        # --- Progress Area ---
        progress_card = ctk.CTkFrame(
            self, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT
        )
        progress_card.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        progress_card.grid_columnconfigure(0, weight=1)

        self.progress = ProgressBarWrapper(progress_card)
        self.progress.pack(fill="x", padx=16, pady=16)

        # --- Logs Area (Split panes) ---
        logs_pane = ctk.CTkFrame(self, fg_color="transparent")
        logs_pane.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        logs_pane.grid_columnconfigure(0, weight=1) # Keep logs
        logs_pane.grid_columnconfigure(1, weight=1) # NLM logs
        logs_pane.grid_rowconfigure(1, weight=1)

        # Headers
        ctk.CTkLabel(
            logs_pane, text="📥 Terminal: Google Keep -> Local", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 8))

        ctk.CTkLabel(
            logs_pane, text="📤 Terminal: Local -> NotebookLM", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 8))

        # Scrollables acting as Terminals
        # Using a dark theme for the console logs to look like a terminal
        self.keep_log_scroll = ctk.CTkScrollableFrame(
            logs_pane,
            fg_color="#1E1E1E", # Dark terminal background
            corner_radius=8
        )
        self.keep_log_scroll.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        self.nlm_log_scroll = ctk.CTkScrollableFrame(
            logs_pane,
            fg_color="#1E1E1E", # Dark terminal background
            corner_radius=8
        )
        self.nlm_log_scroll.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

    def append_keep_log(self, title: str, status: str, msg: str, time_str: str):
        color = MaterialColors.SUCCESS if status == "success" else MaterialColors.ERROR if status == "error" else MaterialColors.TEXT_MAIN
        log = f"[{time_str}] {title}: {msg}"
        lbl = ctk.CTkLabel(self.keep_log_scroll, text=log, text_color=color, anchor="w", justify="left")
        lbl.pack(fill="x", padx=10, pady=2)

    def append_nlm_log(self, filename: str, status: str, msg: str, time_str: str):
        color = MaterialColors.SUCCESS if status == "success" else MaterialColors.ERROR if status == "error" else MaterialColors.TEXT_MAIN
        log = f"[{time_str}] {filename}: {msg}"
        lbl = ctk.CTkLabel(self.nlm_log_scroll, text=log, text_color=color, anchor="w", justify="left")
        lbl.pack(fill="x", padx=10, pady=2)

