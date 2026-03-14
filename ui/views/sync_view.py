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

        # --- Summary Banner ---
        self.summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.summary_frame.grid_columnconfigure((0,1,2,3), weight=1)

        def create_stat_card(parent, title, value='0', color=MaterialColors.TEXT_MAIN):
            card = ctk.CTkFrame(parent, fg_color=MaterialColors.BG_CARD, corner_radius=8, border_width=1, border_color=MaterialColors.BORDER_LIGHT)
            lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="bold"), text_color=MaterialColors.TEXT_MUTED)
            lbl_title.pack(pady=(8, 0))
            lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
            lbl_val.pack(pady=(0, 8))
            return card, lbl_val

        self.card_total, self.lbl_total = create_stat_card(self.summary_frame, "📦 TỔNG SỐ", color=MaterialColors.PRIMARY)
        self.card_total.grid(row=0, column=0, padx=5, sticky="ew")

        self.card_success, self.lbl_success = create_stat_card(self.summary_frame, "✅ THÀNH CÔNG", color=MaterialColors.SUCCESS)
        self.card_success.grid(row=0, column=1, padx=5, sticky="ew")

        self.card_skipped, self.lbl_skipped = create_stat_card(self.summary_frame, "⚪ BỎ QUA", color=MaterialColors.SKIPPED)
        self.card_skipped.grid(row=0, column=2, padx=5, sticky="ew")

        self.card_error, self.lbl_error = create_stat_card(self.summary_frame, "❌ LỖI", color=MaterialColors.ERROR)
        self.card_error.grid(row=0, column=3, padx=5, sticky="ew")

        # --- DataGrid Area ---
        grid_pane = ctk.CTkFrame(self, fg_color="transparent")
        grid_pane.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        grid_pane.grid_columnconfigure(0, weight=1)
        grid_pane.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1) # Allow expansion

        # Header Row
        header_row = ctk.CTkFrame(grid_pane, fg_color=MaterialColors.BORDER_LIGHT, height=36, corner_radius=8)
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 4), padx=(4, 20)) # Pad right for scrollbar width compensation
        header_row.grid_propagate(False)
        header_row.pack_propagate(False)

        ctk.CTkLabel(header_row, text="Tên File", font=ctk.CTkFont(size=13, weight="bold"), text_color=MaterialColors.TEXT_MAIN, anchor="w").place(relx=0.02, rely=0.5, relwidth=0.38, anchor="w")
        ctk.CTkLabel(header_row, text="Tải từ Google Keep", font=ctk.CTkFont(size=13, weight="bold"), text_color=MaterialColors.TEXT_MAIN, anchor="w").place(relx=0.4, rely=0.5, relwidth=0.3, anchor="w")
        ctk.CTkLabel(header_row, text="Đẩy lên NotebookLM", font=ctk.CTkFont(size=13, weight="bold"), text_color=MaterialColors.TEXT_MAIN, anchor="w").place(relx=0.7, rely=0.5, relwidth=0.3, anchor="w")

        # Scrollable Grid Body
        self.grid_scroll = ctk.CTkScrollableFrame(
            grid_pane,
            fg_color=MaterialColors.BG_CARD,
            corner_radius=8,
            border_width=1,
            border_color=MaterialColors.BORDER_LIGHT
        )
        self.grid_scroll.grid(row=1, column=0, sticky="nsew")

        # State tracking
        self._file_rows = {} # filename -> dict of widgets and state
        self._stats = {"total": 0, "success": 0, "skipped": 0, "error": 0, "pending": 0}

    def _get_status_ui(self, status: str, msg: str) -> tuple[str, str]:
        if status == "success": return f"✅ {msg}", MaterialColors.SUCCESS
        if status == "skipped": return f"⚪ {msg}", MaterialColors.SKIPPED
        if status == "error": return f"❌ {msg}", MaterialColors.ERROR
        if status == "pending": return f"⏳ {msg}", MaterialColors.PENDING
        return f"❓ {msg}", MaterialColors.TEXT_MUTED

    def update_file_status(self, filename: str, service: str, status: str, msg: str, time_str: str):
        # Create row if it doesn't exist
        if filename not in self._file_rows:
            row_frame = ctk.CTkFrame(self.grid_scroll, fg_color="transparent", height=40)
            row_frame.pack(fill="x", pady=2, padx=4)
            row_frame.pack_propagate(False)

            # Checkered background for rows
            index = len(self._file_rows)
            if index % 2 != 0:
                row_frame.configure(fg_color="#F9F9FB")

            lbl_name = ctk.CTkLabel(row_frame, text=filename, font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MAIN, anchor="w")
            lbl_name.place(relx=0.02, rely=0.5, relwidth=0.38, anchor="w")

            lbl_keep = ctk.CTkLabel(row_frame, text="—", font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MUTED, anchor="w")
            lbl_keep.place(relx=0.4, rely=0.5, relwidth=0.3, anchor="w")

            lbl_nlm = ctk.CTkLabel(row_frame, text="—", font=ctk.CTkFont(size=13), text_color=MaterialColors.TEXT_MUTED, anchor="w")
            lbl_nlm.place(relx=0.7, rely=0.5, relwidth=0.3, anchor="w")

            self._file_rows[filename] = {
                "frame": row_frame,
                "lbl_keep": lbl_keep,
                "lbl_nlm": lbl_nlm,
                "states": {"keep": "none", "nlm": "none"}
            }
            self._stats["total"] += 1

        row_data = self._file_rows[filename]
        ui_text, ui_color = self._get_status_ui(status, msg)

        # Truncate msg if too long so it doesn't overflow
        if len(msg) > 40:
            ui_text = ui_text[:40] + "..."

        if service == "keep":
            row_data["lbl_keep"].configure(text=ui_text, text_color=ui_color)
            row_data["states"]["keep"] = status
        elif service == "nlm":
            row_data["lbl_nlm"].configure(text=ui_text, text_color=ui_color)
            row_data["states"]["nlm"] = status

        # Sort to top if error or pending (UI Hoisting)
        if status in ("error", "pending"):
            # Pack order manipulation
            row_data["frame"].pack_forget()
            if self.grid_scroll.winfo_children():
                # Re-pack at the top
                row_data["frame"].pack(side="top", fill="x", pady=2, padx=4, before=self.grid_scroll.winfo_children()[0])
            else:
                row_data["frame"].pack(fill="x", pady=2, padx=4)
            # Highlight error rows briefly
            if status == "error":
                row_data["frame"].configure(fg_color="#FCECEB") # Light red
                self.after(2000, lambda rf=row_data["frame"]: rf.configure(fg_color="transparent"))

        self._recalc_stats()

    def _recalc_stats(self):
        success = 0
        skipped = 0
        error = 0
        for f, data in self._file_rows.items():
            st = data["states"]
            vals = list(st.values())
            if "error" in vals:
                error += 1
            elif "success" in vals:
                success += 1
            elif vals == ["skipped", "skipped"] or vals == ["skipped", "none"]:
                skipped += 1

        self.lbl_total.configure(text=str(self._stats["total"]))
        self.lbl_success.configure(text=str(success))
        self.lbl_skipped.configure(text=str(skipped))
        self.lbl_error.configure(text=str(error))

    def reset_grid(self):
        """Clear grid for fresh sync start."""
        for w in self.grid_scroll.winfo_children():
            w.destroy()
        self._file_rows.clear()
        self._stats = {"total": 0, "success": 0, "skipped": 0, "error": 0, "pending": 0}
        self._recalc_stats()

