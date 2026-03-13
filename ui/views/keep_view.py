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

        # Note count label
        self.note_count_label = ctk.CTkLabel(
            filter_frame, text="0 notes", font=ctk.CTkFont(size=12), text_color=MaterialColors.TEXT_MUTED
        )
        self.note_count_label.pack(side="left", padx=(10, 0))

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

    def render_notes(self, notes: list[dict]):
        """Refresh the notes list display using a grid layout with Apple Cards."""
        # Clear existing
        for widget in self.notes_scroll.winfo_children():
            widget.destroy()

        self.note_count_label.configure(text=f"{len(notes)} notes")

        if not notes:
            ctk.CTkLabel(
                self.notes_scroll,
                text="Không tìm thấy ghi chú nào.\nHãy thay đổi bộ lọc hoặc Sync.",
                text_color=MaterialColors.TEXT_MUTED,
                justify="center",
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, columnspan=3, pady=60)
            return

        # 4 columns layout
        col = 0
        row = 0
        today = datetime.now().date()

        for i, note in enumerate(notes):
            # Check if updated today
            updated_dt = note.get("updated")
            is_today = False
            if updated_dt and hasattr(updated_dt, "date") and updated_dt.date() == today:
                is_today = True

            # Card container Material 3 style
            card = ctk.CTkFrame(
                self.notes_scroll,
                corner_radius=12,
                fg_color=MaterialColors.BG_CARD,
                border_width=2 if is_today else 1,
                border_color=MaterialColors.PRIMARY if is_today else MaterialColors.BORDER_LIGHT
            )
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            card.grid_propagate(False)

            # Title
            title = note.get("title", "")
            if not title:
                title = note.get("text", "")[:30] + "..."
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=MaterialColors.TEXT_MAIN,
                anchor="w",
                justify="left",
                wraplength=180
            ).pack(fill="x", padx=16, pady=(16, 4))
            
            # Content snippet
            text = note.get("text", "")
            snippet = text[:100] + "..." if len(text) > 100 else text
            ctk.CTkLabel(
                card,
                text=snippet,
                font=ctk.CTkFont(size=12),
                text_color=MaterialColors.TEXT_MUTED,
                anchor="nw",
                justify="left",
                wraplength=180,
                height=40
            ).pack(fill="x", padx=16, pady=0)

            # Metadata footer (tags, date)
            meta_frame = ctk.CTkFrame(card, fg_color="transparent")
            meta_frame.pack(fill="x", side="bottom", padx=16, pady=12)
            
            labels = note.get("labels", [])
            if labels:
                tags = ", ".join(labels)
                tag_lbl = ctk.CTkLabel(
                    meta_frame,
                    text=f"🏷 {tags}",
                    font=ctk.CTkFont(size=11),
                    text_color=MaterialColors.TEXT_MUTED
                )
                tag_lbl.pack(side="left")
            
            # Extract date from timestamps
            updated_dt = note.get("updated")
            date_text = "📅 Update"
            if updated_dt and hasattr(updated_dt, "strftime"):
                try:
                    date_text = f"📅 {updated_dt.strftime('%d/%m/%Y')}"
                except Exception:
                    pass

            date_lbl = ctk.CTkLabel(
                meta_frame,
                text=date_text,
                font=ctk.CTkFont(size=11),
                text_color=MaterialColors.TEXT_MUTED
            )
            date_lbl.pack(side="right")
            
            col += 1
            if col > 3: # 4 columns (0, 1, 2, 3)
                col = 0
                row += 1

