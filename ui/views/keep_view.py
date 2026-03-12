import customtkinter as ctk
from typing import Callable, Optional
from ui.themes.colors import MaterialColors
from datetime import datetime

class DummyDatePicker:
    """A dummy date picker to satisfy the get_date API."""
    def get_date(self) -> Optional[datetime]:
        return None

class KeepView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        tag_var: ctk.StringVar,
        on_filter_change: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1) # Push filters to right

        ctk.CTkLabel(
            header_frame, text="📝 Ghi Chú Của Bạn", font=ctk.CTkFont(size=24, weight="bold"), text_color=MaterialColors.TEXT_MAIN
        ).grid(row=0, column=0, sticky="w")

        # Filters
        filter_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filter_frame.grid(row=0, column=2, sticky="e")

        ctk.CTkLabel(
            filter_frame, text="Nhãn:", font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MUTED
        ).pack(side="left", padx=(0, 8))

        self.tag_dropdown = ctk.CTkComboBox(
            filter_frame,
            variable=tag_var,
            font=ctk.CTkFont(size=13),
            fg_color=MaterialColors.BG_CONTENT,
            text_color=MaterialColors.TEXT_MAIN,
            border_color=MaterialColors.BORDER_INPUT,
            button_color=MaterialColors.BORDER_LIGHT,
            button_hover_color=MaterialColors.PRIMARY_LIGHT,
            dropdown_font=ctk.CTkFont(size=13),
            dropdown_fg_color=MaterialColors.BG_CONTENT,
            dropdown_text_color=MaterialColors.TEXT_MAIN,
            dropdown_hover_color=MaterialColors.PRIMARY_LIGHT,
            values=["Tất cả"],
            command=lambda e: on_filter_change(),
            state="readonly",
            width=160
        )
        self.tag_dropdown.pack(side="left")

        # Dummy Date Pickers to satisfy API
        self.date_from = DummyDatePicker()
        self.date_to = DummyDatePicker()

        # --- Notes Grid (Scrollable) ---
        self.notes_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.notes_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Grid layout handling inside `notes_scroll` will be done via `main_frame.update_notes_list`
        
        self._show_placeholder()

    def _show_placeholder(self):
        # Initial placeholder text
        ctk.CTkLabel(
            self.notes_scroll, 
            text="Đang lấy dữ liệu từ Home View hoặc Google Keep...", 
            text_color=MaterialColors.TEXT_MUTED,
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, columnspan=2, pady=60)

