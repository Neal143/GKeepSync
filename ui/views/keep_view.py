import customtkinter as ctk
from typing import Callable, Optional
from ui.components import DateEntry

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
        self.grid_rowconfigure(2, weight=1)

        # Filters
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 4))
        filter_frame.grid_columnconfigure(1, weight=1)

        # Tag filter
        ctk.CTkLabel(
            filter_frame, text="🏷️ Tag:", font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=(12, 4), pady=12, sticky="w")

        self.tag_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            variable=tag_var,
            values=["Tất cả"],
            width=160,
            height=30,
            font=ctk.CTkFont(size=12),
            command=lambda _: on_filter_change(),
        )
        self.tag_dropdown.grid(row=0, column=1, padx=4, pady=12, sticky="w")

        # Date range
        ctk.CTkLabel(
            filter_frame, text="📅 Từ:", font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=(12, 4), pady=12, sticky="w")

        self.date_from = DateEntry(filter_frame, placeholder="YYYY-MM-DD")
        self.date_from.grid(row=0, column=3, padx=4, pady=12, sticky="w")

        ctk.CTkLabel(
            filter_frame, text="Đến:", font=ctk.CTkFont(size=12)
        ).grid(row=0, column=4, padx=(12, 4), pady=12, sticky="w")

        self.date_to = DateEntry(filter_frame, placeholder="YYYY-MM-DD")
        self.date_to.grid(row=0, column=5, padx=(4, 12), pady=12, sticky="w")

        # Note Count
        self.note_count_label = ctk.CTkLabel(
            self,
            text="0 notes",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        self.note_count_label.grid(row=1, column=0, sticky="e", padx=20, pady=(0, 4))

        # Notes List
        self.notes_scroll = ctk.CTkScrollableFrame(
            self,
            label_text="📝 Ghi chú",
            label_font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.notes_scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4, 20))
        self.notes_scroll.grid_columnconfigure(0, weight=1)
        self.notes_scroll.grid_columnconfigure(1, weight=1)
        self.notes_scroll.grid_columnconfigure(2, weight=1)
