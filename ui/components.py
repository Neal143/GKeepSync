"""
GKeepSync - Reusable UI Components
Date picker, status bar, notification toast.
"""

import customtkinter as ctk
from datetime import datetime, date
from typing import Callable, Optional
from ui.themes.colors import MaterialColors


class DateEntry(ctk.CTkFrame):
    """Simple date entry widget (YYYY-MM-DD)."""

    def __init__(self, master, placeholder: str = "YYYY-MM-DD", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=130,
            height=32,
            font=ctk.CTkFont(size=13),
            fg_color=MaterialColors.BG_CARD,
            border_color=MaterialColors.BORDER_INPUT,
            text_color=MaterialColors.TEXT_MAIN
        )
        self._entry.pack(side="left")

    def get_date(self) -> Optional[datetime]:
        """Parse the date string, return datetime or None."""
        text = self._entry.get().strip()
        if not text:
            return None
        try:
            return datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            return None

    def set_date(self, d: str):
        self._entry.delete(0, "end")
        self._entry.insert(0, d)

    def clear(self):
        self._entry.delete(0, "end")


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing application info."""

    def __init__(self, master, **kwargs):
        # Using a slight grey background for the generic status bar
        super().__init__(master, height=36, corner_radius=0, fg_color=MaterialColors.BG_CONTENT, border_width=1, border_color=MaterialColors.BORDER_LIGHT, **kwargs)

        self._status_label = ctk.CTkLabel(
            self,
            text="Chưa kết nối",
            font=ctk.CTkFont(size=12),
            text_color=MaterialColors.TEXT_MAIN,
            anchor="w",
        )
        self._status_label.pack(side="left", padx=12, pady=4)

        self._nlm_status_label = ctk.CTkLabel(
            self,
            text=" | NotebookLM: ❌",
            font=ctk.CTkFont(size=12),
            text_color=MaterialColors.ERROR,
            anchor="w",
        )
        self._nlm_status_label.pack(side="left", padx=0, pady=4)

        self._sync_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=MaterialColors.TEXT_MUTED,
            anchor="e",
        )
        self._sync_label.pack(side="right", padx=12, pady=4)

    def set_status(self, text: str):
        self._status_label.configure(text=text)

    def set_nlm_status(self, logged_in: bool):
        if logged_in:
            self._nlm_status_label.configure(text=" | NotebookLM: ✅", text_color=MaterialColors.SUCCESS)
        else:
            self._nlm_status_label.configure(text=" | NotebookLM: ❌", text_color=MaterialColors.ERROR)

    def set_sync_info(self, text: str):
        self._sync_label.configure(text=text)


class NotificationToast(ctk.CTkFrame):
    """Floating notification toast using MaterialColors."""

    def __init__(self, master, message: str, toast_type: str = "info", duration: int = 4000):
        colors = {
            "success": MaterialColors.SUCCESS,
            "error": MaterialColors.ERROR,
            "info": MaterialColors.PRIMARY,
            "warning": "#f39c12", # Hardcoded warning if needed, though rarely used in Apple design
        }
        fg = colors.get(toast_type, colors["info"])

        super().__init__(
            master,
            fg_color=fg,
            corner_radius=8,
            border_width=0
        )

        icons = {"success": "✅", "error": "❌", "info": "ℹ️", "warning": "⚠️"}

        ctk.CTkLabel(
            self,
            text=f" {icons.get(toast_type, 'ℹ️')}  {message}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF",
        ).pack(padx=20, pady=12)

        # Auto-dismiss
        self.after(duration, self._dismiss)

    def _dismiss(self):
        try:
            self.destroy()
        except Exception:
            pass


class SyncProgressBar(ctk.CTkFrame):
    """Progress bar for sync operations."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=MaterialColors.TEXT_MAIN, anchor="w"
        )
        self._label.pack(fill="x", padx=4, pady=(4, 0))

        self._bar = ctk.CTkProgressBar(
            self, 
            height=6, 
            corner_radius=3,
            progress_color=MaterialColors.PRIMARY,
            fg_color=MaterialColors.BORDER_LIGHT
        )
        self._bar.pack(fill="x", padx=4, pady=(2, 4))
        self._bar.set(0)

    def update_progress(self, text: str, current: int, total: int):
        if total > 0:
            self._bar.set(current / total)
        self._label.configure(text=text)

    def reset(self):
        self._bar.set(0)
        self._label.configure(text="")
