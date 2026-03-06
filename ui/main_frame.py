"""
GKeepSync - Main Frame
Giao diện chính sau login: folder picker, filters, sync controls, notes list, status bar.
"""

import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
from typing import Callable, Optional

from ui.components import DateEntry, StatusBar, SyncProgressBar


class MainFrame(ctk.CTkFrame):
    """Main application frame after login."""

    def __init__(
        self,
        master,
        on_sync: Callable,
        on_auto_sync_toggle: Callable[[bool, int], None],
        on_folder_change: Callable[[str], None],
        on_logout: Callable,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._on_sync = on_sync
        self._on_auto_sync_toggle = on_auto_sync_toggle
        self._on_folder_change = on_folder_change
        self._on_logout = on_logout

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Notes list expands

        row = 0

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=row, column=0, sticky="ew", padx=16, pady=(12, 4))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="🔄 GKeepSync",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        logout_btn = ctk.CTkButton(
            header,
            text="🚪 Đăng xuất",
            width=100,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            command=self._on_logout,
        )
        logout_btn.grid(row=0, column=2, sticky="e")

        row += 1

        # --- Output Folder ---
        folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        folder_frame.grid(row=row, column=0, sticky="ew", padx=16, pady=(8, 4))
        folder_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            folder_frame, text="📁 Thư mục lưu:", font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=(0, 8))

        self._folder_var = ctk.StringVar()
        self._folder_entry = ctk.CTkEntry(
            folder_frame,
            textvariable=self._folder_var,
            height=32,
            font=ctk.CTkFont(size=12),
            state="disabled",
        )
        self._folder_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=70,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self._browse_folder,
        ).grid(row=0, column=2)

        row += 1

        # --- Filters ---
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=row, column=0, sticky="ew", padx=16, pady=4)
        filter_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            filter_frame,
            text="🔍 Bộ lọc",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=12, pady=(8, 4))

        # Tag filter
        ctk.CTkLabel(
            filter_frame, text="🏷️ Tag:", font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=(12, 4), pady=4, sticky="w")

        self._tag_var = ctk.StringVar(value="Tất cả")
        self._tag_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            variable=self._tag_var,
            values=["Tất cả"],
            width=160,
            height=30,
            font=ctk.CTkFont(size=12),
        )
        self._tag_dropdown.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        # Date range
        ctk.CTkLabel(
            filter_frame, text="📅 Từ:", font=ctk.CTkFont(size=12)
        ).grid(row=2, column=0, padx=(12, 4), pady=4, sticky="w")

        self._date_from = DateEntry(filter_frame, placeholder="YYYY-MM-DD")
        self._date_from.grid(row=2, column=1, padx=4, pady=4, sticky="w")

        ctk.CTkLabel(
            filter_frame, text="Đến:", font=ctk.CTkFont(size=12)
        ).grid(row=2, column=2, padx=(12, 4), pady=4, sticky="w")

        self._date_to = DateEntry(filter_frame, placeholder="YYYY-MM-DD")
        self._date_to.grid(row=2, column=3, padx=(4, 12), pady=4, sticky="w")

        # Auto Sync row
        auto_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        auto_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=12, pady=(4, 8))

        ctk.CTkLabel(
            auto_frame, text="⏰ Auto Sync:", font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 8))

        self._interval_var = ctk.StringVar(value="60 phút")
        self._interval_dropdown = ctk.CTkOptionMenu(
            auto_frame,
            variable=self._interval_var,
            values=["15 phút", "30 phút", "60 phút", "3 giờ", "6 giờ"],
            width=100,
            height=28,
            font=ctk.CTkFont(size=12),
        )
        self._interval_dropdown.pack(side="left", padx=(0, 8))

        self._auto_sync_switch = ctk.CTkSwitch(
            auto_frame,
            text="Bật",
            font=ctk.CTkFont(size=12),
            command=self._handle_auto_sync_toggle,
            width=60,
        )
        self._auto_sync_switch.pack(side="left", padx=(0, 16))

        # Sync Now button
        self._sync_btn = ctk.CTkButton(
            auto_frame,
            text="🔄 Sync Now",
            width=120,
            height=32,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._handle_sync,
        )
        self._sync_btn.pack(side="right")

        row += 1

        # --- Progress Bar ---
        self._progress = SyncProgressBar(self)
        self._progress.grid(row=row, column=0, sticky="ew", padx=16, pady=(0, 4))

        row += 1

        # --- Notes List ---
        notes_frame = ctk.CTkFrame(self)
        notes_frame.grid(row=row, column=0, sticky="nsew", padx=16, pady=(0, 4))
        notes_frame.grid_columnconfigure(0, weight=1)
        notes_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            notes_frame,
            text="📝 Ghi chú đã sync",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 4))

        self._notes_scroll = ctk.CTkScrollableFrame(
            notes_frame,
            label_text="",
        )
        self._notes_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self._notes_scroll.grid_columnconfigure(0, weight=1)

        self._note_count_label = ctk.CTkLabel(
            notes_frame,
            text="0 notes",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        self._note_count_label.grid(row=0, column=0, sticky="e", padx=12, pady=(8, 4))

        row += 1

        # --- Status Bar ---
        self._status_bar = StatusBar(self)
        self._status_bar.grid(row=row, column=0, sticky="ew")

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Chọn thư mục lưu ghi chú")
        if folder:
            self._folder_var.set(folder)
            self._on_folder_change(folder)

    def _get_interval_minutes(self) -> int:
        mapping = {
            "15 phút": 15,
            "30 phút": 30,
            "60 phút": 60,
            "3 giờ": 180,
            "6 giờ": 360,
        }
        return mapping.get(self._interval_var.get(), 60)

    def _handle_auto_sync_toggle(self):
        enabled = bool(self._auto_sync_switch.get())
        interval = self._get_interval_minutes()
        self._on_auto_sync_toggle(enabled, interval)

    def _handle_sync(self):
        self._on_sync()

    def set_folder(self, path: str):
        self._folder_var.set(path)

    def set_labels(self, labels: list[str]):
        """Update tag dropdown with available labels."""
        options = ["Tất cả"] + labels
        self._tag_dropdown.configure(values=options)
        self._tag_var.set("Tất cả")

    def get_selected_labels(self) -> Optional[list[str]]:
        """Get currently selected labels for filtering."""
        val = self._tag_var.get()
        if val == "Tất cả":
            return None
        return [val]

    def get_date_from(self) -> Optional[datetime]:
        return self._date_from.get_date()

    def get_date_to(self) -> Optional[datetime]:
        return self._date_to.get_date()

    def set_syncing(self, syncing: bool):
        if syncing:
            self._sync_btn.configure(state="disabled", text="⏳ Đang sync...")
        else:
            self._sync_btn.configure(state="normal", text="🔄 Sync Now")

    def update_progress(self, text: str, current: int, total: int):
        self._progress.update_progress(text, current, total)

    def reset_progress(self):
        self._progress.reset()

    def update_notes_list(self, notes: list[dict]):
        """Refresh the notes list display."""
        # Clear existing
        for widget in self._notes_scroll.winfo_children():
            widget.destroy()

        self._note_count_label.configure(text=f"{len(notes)} notes")

        for i, note in enumerate(notes):
            row_frame = ctk.CTkFrame(
                self._notes_scroll,
                height=36,
                corner_radius=6,
            )
            row_frame.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
            row_frame.grid_columnconfigure(1, weight=1)

            # Pin indicator
            pin = "📌 " if note.get("pinned") else "📝 "

            # Title
            ctk.CTkLabel(
                row_frame,
                text=f"{pin}{note['title']}",
                font=ctk.CTkFont(size=12),
                anchor="w",
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 0))

            # Meta row
            meta_parts = []
            if note.get("updated"):
                try:
                    dt = note["updated"]
                    if isinstance(dt, datetime):
                        meta_parts.append(dt.strftime("%Y-%m-%d %H:%M"))
                    else:
                        meta_parts.append(str(dt)[:16])
                except Exception:
                    pass

            if note.get("labels"):
                meta_parts.append("🏷️ " + ", ".join(note["labels"]))

            ctk.CTkLabel(
                row_frame,
                text="  |  ".join(meta_parts) if meta_parts else "",
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w",
            ).grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 4))

    def update_status(self, text: str):
        self._status_bar.set_status(text)

    def update_sync_info(self, text: str):
        self._status_bar.set_sync_info(text)
