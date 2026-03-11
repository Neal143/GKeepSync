import customtkinter as ctk
from typing import Callable
from ui.components import StatusBar

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
            self, text="🏠 Trang chủ", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=row, column=0, padx=20, pady=(20, 10), sticky="w")
        row += 1

        # --- Output Folder ---
        folder_frame = ctk.CTkFrame(self, fg_color="#F5F5F7", corner_radius=12)
        folder_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=(8, 12))
        folder_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            folder_frame, text="📁 Thư mục lưu:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1C1C1E"
        ).grid(row=0, column=0, padx=(16, 8), pady=16)

        self._folder_entry = ctk.CTkEntry(
            folder_frame,
            textvariable=folder_var,
            height=36,
            font=ctk.CTkFont(size=13),
            state="disabled",
            fg_color="#FFFFFF",
            border_color="#D1D1D6"
        )
        self._folder_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=80,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#007AFF",
            text_color="#FFFFFF",
            hover_color="#0056B3",
            command=on_browse_folder,
        ).grid(row=0, column=2, padx=(0, 16))

        row += 1

        # --- Auto Sync ---
        auto_frame = ctk.CTkFrame(self, fg_color="#F5F5F7", corner_radius=12)
        auto_frame.grid(row=row, column=0, sticky="ew", padx=20, pady=(4, 12))

        ctk.CTkLabel(
            auto_frame, text="⏰ Auto Sync:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1C1C1E"
        ).grid(row=0, column=0, padx=(16, 8), pady=16)

        self._interval_dropdown = ctk.CTkOptionMenu(
            auto_frame,
            variable=interval_var,
            values=["15 phút", "30 phút", "60 phút", "3 giờ", "6 giờ"],
            width=100,
            height=28,
            font=ctk.CTkFont(size=12),
        )
        self._interval_dropdown.grid(row=0, column=1, padx=(0, 8))

        self._auto_sync_switch = ctk.CTkSwitch(
            auto_frame,
            text="Bật",
            font=ctk.CTkFont(size=12),
            command=on_auto_sync_toggle,
            width=60,
        )
        self._auto_sync_switch.grid(row=0, column=2, padx=(0, 16))

        row += 1

        # --- StatusBar ---
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=row, column=0, sticky="ew", padx=20, pady=20)
