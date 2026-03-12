"""
GKeepSync - Main Frame (Apple Light Theme)
Giao diß╗çn ch├¡nh sau login: folder picker, filters, sync controls, notes list, status bar.
"""

import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
from typing import Callable, Optional

# Import refactored views
from ui.views.home_view import HomeView
from ui.views.keep_view import KeepView
from ui.views.nlm_view import NLMView
from ui.views.sync_view import SyncView

class MainFrame(ctk.CTkFrame):
    """Main application frame after login. Coordinates between specific views."""

    def __init__(
        self,
        master,
        on_sync: Callable,
        on_auto_sync_toggle: Callable[[bool, int], None],
        on_folder_change: Callable[[str], None],
        on_logout: Callable,
        **kwargs,
    ):
        # Nß╗ün bao tr├╣m trß║»ng muß╗æt
        super().__init__(master, fg_color="#FFFFFF", **kwargs)

        self.on_sync = on_sync
        self._on_auto_sync_toggle = on_auto_sync_toggle
        self._on_folder_change = on_folder_change
        self.on_logout = on_logout

        # Additional optional callbacks
        self.on_filter_change: Optional[Callable[[], None]] = None
        
        # NLM Callbacks
        self._on_nlm_toggle: Optional[Callable[[bool], None]] = None
        self._on_nlm_id_change: Optional[Callable[[str], None]] = None
        self._on_nlm_login: Optional[Callable[[], None]] = None
        self._on_nlm_fetch_notebooks: Optional[Callable[[], None]] = None
        self._on_nlm_fetch_sources: Optional[Callable[[str], None]] = None

        self.grid_rowconfigure(1, weight=1) # Row 1 for content
        self.grid_columnconfigure(1, weight=1) # Column 1 for right area

        # Variables
        self._folder_var = ctk.StringVar()
        self._interval_var = ctk.StringVar(value="60 ph├║t")
        self._tag_var = ctk.StringVar(value="Tß║Ñt cß║ú")
        self._nlm_id_var = ctk.StringVar()

        self._build_sidebar()
        
        # Initialize sub-views. Note: views themselves need to be light theme compatible
        self.home_view = HomeView(
            self,
            folder_var=self._folder_var,
            interval_var=self._interval_var,
            on_browse_folder=self._browse_folder,
            on_auto_sync_toggle=self._handle_auto_sync_toggle
        )
        self.keep_view = KeepView(
            self,
            tag_var=self._tag_var,
            on_filter_change=self._handle_filter_change
        )
        self.nlm_view = NLMView(
            self,
            nlm_id_var=self._nlm_id_var,
            on_nlm_toggle=self._handle_nlm_toggle,
            on_nlm_id_change=self._handle_nlm_id_change,
            on_nlm_login=self._handle_nlm_login,
            on_nlm_fetch_notebooks=self._handle_nlm_fetch_notebooks
        )
        self.sync_view = SyncView(self)

        # Default frame
        self.select_frame_by_name("home")

    def _build_sidebar(self):
        # MacOS style sidebar: Light Gray background
        self._sidebar = ctk.CTkFrame(self, fg_color="#F5F5F7", corner_radius=0)
        self._sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self._sidebar.grid_rowconfigure(5, weight=1)

        # Title
        title_lbl = ctk.CTkLabel(
            self._sidebar, 
            text="GKeepSync", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1C1C1E"
        )
        title_lbl.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Utility for creating sidebar buttons
        def create_nav_btn(text, cmd):
            return ctk.CTkButton(
                self._sidebar,
                text=text,
                fg_color="transparent",
                text_color="#1C1C1E",
                hover_color="#E5E5EA",
                anchor="w",
                corner_radius=8,
                font=ctk.CTkFont(size=14),
                command=cmd,
                height=36
            )

        # Nav Buttons
        self._home_btn = create_nav_btn("≡ƒÅá  Trang chß╗º", lambda: self.select_frame_by_name("home"))
        self._home_btn.grid(row=1, column=0, padx=12, pady=4, sticky="ew")

        self._keep_btn = create_nav_btn("≡ƒô¥  Google Keep", lambda: self.select_frame_by_name("keep"))
        self._keep_btn.grid(row=2, column=0, padx=12, pady=4, sticky="ew")
        
        self._nlm_btn = create_nav_btn("≡ƒôô  NotebookLM", lambda: self.select_frame_by_name("nlm"))
        self._nlm_btn.grid(row=3, column=0, padx=12, pady=4, sticky="ew")

        self._sync_btn_nav = create_nav_btn("ΓÅ▒∩╕Å  Lß╗ïch sß╗¡ Sync", lambda: self.select_frame_by_name("sync"))
        self._sync_btn_nav.grid(row=4, column=0, padx=12, pady=4, sticky="ew")

        # Spacer taking up empty vertical space
        spacer = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        spacer.grid(row=5, column=0, sticky="nsew")

        # Sync Button (Action) at bottom
        self._sync_btn = ctk.CTkButton(
            self._sidebar,
            text="≡ƒöä  ─Éß╗ông bß╗Ö ngay",
            height=36,
            corner_radius=8,
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#007AFF",
            hover_color="#0056B3",
            text_color="#FFFFFF",
            command=self._handle_sync
        )
        self._sync_btn.grid(row=6, column=0, padx=12, pady=(0, 4), sticky="ew")

        # Logout at very bottom
        self._logout_btn = ctk.CTkButton(
            self._sidebar,
            text="≡ƒÜ¬  ─É─âng xuß║Ñt",
            fg_color="transparent",
            text_color="#FF3B30", # Apple Red
            hover_color="#FCECEB",
            anchor="w",
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_logout,
            height=36
        )
        self._logout_btn.grid(row=7, column=0, padx=12, pady=(5, 20), sticky="ew")

    def select_frame_by_name(self, name):
        # Update button colors (Active state like MacOS highlighted item)
        active_color = "#E5E5EA"
        for btn in [self._home_btn, self._keep_btn, self._nlm_btn, self._sync_btn_nav]:
            btn.configure(fg_color="transparent")

        # Hide all frames
        for view in [self.home_view, self.keep_view, self.nlm_view, self.sync_view]:
            view.grid_forget()

        # Show selected
        if name == "home":
            self.home_view.grid(row=1, column=1, sticky="nsew", padx=24, pady=0)
            self._home_btn.configure(fg_color=active_color)
        elif name == "keep":
            self.keep_view.grid(row=1, column=1, sticky="nsew", padx=24, pady=0)
            self._keep_btn.configure(fg_color=active_color)
        elif name == "nlm":
            self.nlm_view.grid(row=1, column=1, sticky="nsew", padx=24, pady=0)
            self._nlm_btn.configure(fg_color=active_color)
        elif name == "sync":
            self.sync_view.grid(row=1, column=1, sticky="nsew", padx=24, pady=0)
            self._sync_btn_nav.configure(fg_color=active_color)

    # ------------------------------------------------------------------
    # Actions & Interactions
    # ------------------------------------------------------------------

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Chß╗ìn th╞░ mß╗Ñc l╞░u ghi ch├║")
        if folder:
            self._folder_var.set(folder)
            self._on_folder_change(folder)

    def _get_interval_minutes(self) -> int:
        mapping = {
            "15 ph├║t": 15,
            "30 ph├║t": 30,
            "60 ph├║t": 60,
            "3 giß╗¥": 180,
            "6 giß╗¥": 360,
        }
        return mapping.get(self._interval_var.get(), 60)

    def _handle_auto_sync_toggle(self):
        enabled = bool(self.home_view._auto_sync_switch.get())
        interval = self._get_interval_minutes()
        self._on_auto_sync_toggle(enabled, interval)

    def _handle_sync(self):
        self.on_sync()

    def _handle_filter_change(self):
        if self.on_filter_change:
            self.on_filter_change()

    # NLM Handlers
    def _handle_nlm_toggle(self):
        enabled = bool(self.nlm_view.nlm_switch.get())
        if self._on_nlm_toggle:
            self._on_nlm_toggle(enabled)

    def _handle_nlm_id_change(self):
        nb_id = self._nlm_id_var.get().strip()
        if self._on_nlm_id_change:
            self._on_nlm_id_change(nb_id)

    def _handle_nlm_login(self):
        if self._on_nlm_login:
            self.nlm_view.nlm_login_btn.configure(state="disabled", text="─Éang login...")
            self._on_nlm_login()

    def set_nlm_login_state(self, is_disabled: bool, text: str):
        self.nlm_view.nlm_login_btn.configure(
            state="disabled" if is_disabled else "normal",
            text=text
        )

    def _handle_nlm_fetch_notebooks(self):
        if self._on_nlm_fetch_notebooks:
            self.nlm_view.fetch_nb_btn.configure(state="disabled", text="─Éang tß║úi...")
            # clear UI
            for w in self.nlm_view.nb_scroll.winfo_children():
                w.destroy()
            for w in self.nlm_view.src_scroll.winfo_children():
                w.destroy()
            self._on_nlm_fetch_notebooks()

    def set_nlm_notebooks(self, notebooks: list[dict], error: str = None):
        self.nlm_view.fetch_nb_btn.configure(state="normal", text="Tß║úi Notebooks")
        for w in self.nlm_view.nb_scroll.winfo_children():
            w.destroy()

        if error:
            ctk.CTkLabel(self.nlm_view.nb_scroll, text=error, text_color="#FF3B30", wraplength=200).pack(pady=20)
            return

        if not notebooks:
            ctk.CTkLabel(self.nlm_view.nb_scroll, text="Kh├┤ng t├¼m thß║Ñy Notebook n├áo.", text_color="#8E8E93").pack(pady=20)
            return

        for nb in notebooks:
            card = ctk.CTkFrame(self.nlm_view.nb_scroll, corner_radius=8, fg_color="#FFFFFF", border_width=1, border_color="#E5E5EA")
            card.pack(fill="x", pady=4, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            # Select button
            btn = ctk.CTkButton(
                card, 
                text=nb["title"], 
                anchor="w", 
                fg_color="transparent", 
                text_color="#1C1C1E",
                hover_color="#F5F5F7",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda id=nb["id"]: self._handle_select_notebook(id)
            )
            btn.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
            
            # ID label
            ctk.CTkLabel(card, text=f"ID: {nb['id'][:8]}...", font=ctk.CTkFont(size=11), text_color="#8E8E93").grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

    def _handle_select_notebook(self, nb_id: str):
        self._nlm_id_var.set(nb_id)
        self._handle_nlm_id_change()
        # Fetch sources
        if self._on_nlm_fetch_sources:
            for w in self.nlm_view.src_scroll.winfo_children():
                w.destroy()
            ctk.CTkLabel(self.nlm_view.src_scroll, text="ΓÅ│ ─Éang tß║úi sources...", text_color="#8E8E93").pack(pady=20)
            self._on_nlm_fetch_sources(nb_id)

    def set_nlm_sources(self, sources: list[dict], error: str = None):
        for w in self.nlm_view.src_scroll.winfo_children():
            w.destroy()

        if error:
            ctk.CTkLabel(self.nlm_view.src_scroll, text=error, text_color="#FF3B30", wraplength=200).pack(pady=20)
            return

        if not sources:
            ctk.CTkLabel(self.nlm_view.src_scroll, text="Notebook n├áy ch╞░a c├│ source n├áo.", text_color="#8E8E93").pack(pady=20)
            return

        for src in sources:
            card = ctk.CTkFrame(self.nlm_view.src_scroll, corner_radius=8, fg_color="#F5F5F7")
            card.pack(fill="x", pady=4, padx=4)
            
            title = src.get("title", "Untitled Source")
            ctk.CTkLabel(card, text=f"≡ƒôä {title}", anchor="w", font=ctk.CTkFont(weight="bold", size=13), text_color="#1C1C1E").pack(fill="x", padx=10, pady=(8, 2))
            
            doc_id = src.get("id", "")
            ctk.CTkLabel(card, text=f"ID: {doc_id}", font=ctk.CTkFont(size=11), text_color="#8E8E93", anchor="w").pack(fill="x", padx=10, pady=(0, 8))

    # ------------------------------------------------------------------
    # External API for App
    # ------------------------------------------------------------------

    def set_folder(self, path: str):
        self._folder_var.set(path)

    def set_labels(self, labels: list[str]):
        """Update tag dropdown with available labels."""
        options = ["Tß║Ñt cß║ú"] + labels
        self.keep_view.tag_dropdown.configure(values=options)
        self._tag_var.set("Tß║Ñt cß║ú")

    def get_selected_labels(self) -> Optional[list[str]]:
        """Get currently selected labels for filtering."""
        val = self._tag_var.get()
        if val == "Tß║Ñt cß║ú":
            return None
        return [val]

    def get_date_from(self) -> Optional[datetime]:
        return self.keep_view.date_from.get_date()

    def get_date_to(self) -> Optional[datetime]:
        return self.keep_view.date_to.get_date()

    def set_syncing(self, syncing: bool):
        if syncing:
            self._sync_btn.configure(state="disabled", text="ΓÅ│ Syncing...")
        else:
            self._sync_btn.configure(state="normal", text="≡ƒöä Sync")

    def update_progress(self, text: str, current: int, total: int):
        self.sync_view.progress.update_progress(text, current, total)

    def reset_progress(self):
        self.sync_view.progress.update_progress("Ready", 0, 1)

    def append_keep_log(self, title: str, status: str, msg: str, time_str: str):
        color = "#34C759" if status == "success" else "#FF3B30" if status == "error" else "#1C1C1E"
        log = f"[{time_str}] {title}: {msg}"
        lbl = ctk.CTkLabel(self.sync_view.keep_log_scroll, text=log, text_color=color, anchor="w", justify="left")
        lbl.pack(fill="x", padx=10, pady=2)

    def append_nlm_log(self, filename: str, status: str, msg: str, time_str: str):
        color = "#34C759" if status == "success" else "#FF3B30" if status == "error" else "#1C1C1E"
        log = f"[{time_str}] {filename}: {msg}"
        lbl = ctk.CTkLabel(self.sync_view.nlm_log_scroll, text=log, text_color=color, anchor="w", justify="left")
        lbl.pack(fill="x", padx=10, pady=2)

    def update_notes_list(self, notes: list[dict]):
        """Refresh the notes list display using a grid layout with Apple Cards."""
        # Clear existing
        for widget in self.keep_view.notes_scroll.winfo_children():
            widget.destroy()

        self.keep_view.note_count_label.configure(text=f"{len(notes)} notes")

        if not notes:
            ctk.CTkLabel(
                self.keep_view.notes_scroll,
                text="Kh├┤ng t├¼m thß║Ñy ghi ch├║ n├áo.\nH├úy thß╗¡ ─æß╗òi bß╗Ö lß╗ìc hoß║╖c Sync.",
                text_color="#8E8E93",
                justify="center",
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, columnspan=3, pady=60)
            return

        # 3 columns layout
        col = 0
        row = 0
        for i, note in enumerate(notes):
            # Card container Apple style
            card = ctk.CTkFrame(
                self.keep_view.notes_scroll,
                corner_radius=12,
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E5E5EA"
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
                text_color="#1C1C1E",
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
                text_color="#8E8E93",
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
                    text=f"≡ƒÅ╖ {tags}",
                    font=ctk.CTkFont(size=11),
                    text_color="#8E8E93"
                )
                tag_lbl.pack(side="left")
            
            date_lbl = ctk.CTkLabel(
                meta_frame,
                text="≡ƒôà Update", # Placeholder until real date is implemented
                font=ctk.CTkFont(size=11),
                text_color="#8E8E93"
            )
            date_lbl.pack(side="right")
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def update_status(self, text: str):
        if hasattr(self.home_view, 'status_bar'):
            self.home_view.status_bar.set_status(text)

    def update_sync_info(self, text: str):
        if hasattr(self.home_view, 'status_bar'):
            self.home_view.status_bar.set_sync_info(text)

