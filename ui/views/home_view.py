import customtkinter as ctk
from typing import Callable
from ui.themes.colors import MaterialColors


class HomeView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        folder_var: ctk.StringVar,
        interval_var: ctk.StringVar,
        on_browse_folder: Callable[[], None],
        on_auto_sync_toggle: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        row = 0
        ctk.CTkLabel(
            self, text="🏠 Trang chủ", font=ctk.CTkFont(size=24, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=row, column=0, padx=20, pady=(20, 10), sticky="w")
        row += 1

        # --- Output Folder Management ---
        folder_frame = ctk.CTkFrame(self, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT)
        folder_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=(8, 12))
        folder_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            folder_frame, text="📁 Thư mục lưu trữ:", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, padx=(16, 8), pady=16)

        self._folder_entry = ctk.CTkEntry(
            folder_frame,
            textvariable=folder_var,
            height=36,
            font=ctk.CTkFont(size=13),
            state="disabled",
            fg_color=MaterialColors.BG_CONTENT,
            text_color=MaterialColors.TEXT_MAIN,
            border_color=MaterialColors.BORDER_INPUT
        )
        self._folder_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            folder_frame,
            text="Thay đổi",
            width=90,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=MaterialColors.PRIMARY,
            text_color="#FFFFFF",
            hover_color=MaterialColors.PRIMARY_HOVER,
            command=on_browse_folder,
        ).grid(row=0, column=2, padx=(0, 16))

        row += 1

        # --- Auto Sync Settings ---
        auto_frame = ctk.CTkFrame(self, fg_color=MaterialColors.BG_CARD, corner_radius=12, border_width=1, border_color=MaterialColors.BORDER_LIGHT)
        auto_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=(4, 12))

        ctk.CTkLabel(
            auto_frame, text="⏰ Tự động đồng bộ:", font=ctk.CTkFont(size=14, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, padx=(16, 8), pady=16)

        self._interval_dropdown = ctk.CTkOptionMenu(
            auto_frame,
            variable=interval_var,
            values=["15 phút", "30 phút", "60 phút", "3 giờ", "6 giờ"],
            width=120,
            height=32,
            font=ctk.CTkFont(size=13),
            fg_color=MaterialColors.BG_CONTENT,
            button_color=MaterialColors.BORDER_LIGHT,
            button_hover_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN,
            dropdown_fg_color=MaterialColors.BG_CARD,
            dropdown_text_color=MaterialColors.TEXT_MAIN,
        )
        self._interval_dropdown.grid(row=0, column=1, padx=(0, 16))

        self._auto_sync_switch = ctk.CTkSwitch(
            auto_frame,
            text="Bật",
            font=ctk.CTkFont(size=13),
            text_color=MaterialColors.TEXT_MAIN,
            progress_color=MaterialColors.PRIMARY,
            command=on_auto_sync_toggle,
            width=60,
        )
        self._auto_sync_switch.grid(row=0, column=2, padx=(0, 16))

        row += 1
        
        # Add a stretchable empty row to push the status bar to the very bottom
        self.grid_rowconfigure(row, weight=1)
        row += 1

        # --- StatusBar ---
        from ui.components import StatusBar
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=row, column=0, sticky="sew", padx=20, pady=(10, 20))
