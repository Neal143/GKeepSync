"""
GKeepSync - Google Keep Client
Wrapper cho gkeepapi: login, lấy notes, lọc theo label/thời gian.
"""

import gkeepapi
import gpsoauth
from datetime import datetime
from typing import Optional


class KeepClient:
    """Wrapper around gkeepapi for Google Keep access."""

    def __init__(self):
        self._keep = gkeepapi.Keep()
        self._logged_in = False
        self._email = ""

    @property
    def is_logged_in(self) -> bool:
        return self._logged_in

    def login(self, email: str, token_or_password: str) -> tuple[bool, str]:
        """
        Login with email + master token OR app password.
        Returns (success: bool, message: str)
        """
        try:
            token_or_password = token_or_password.replace(" ", "")
            master_token = token_or_password

            if not token_or_password.startswith("aas_et/"):
                # It's an app password, exchange it for a master token
                import hashlib
                android_id = hashlib.md5(email.encode()).hexdigest()[:16]
                result = gpsoauth.perform_master_login(email, token_or_password, android_id)
                if "Token" not in result:
                    self._logged_in = False
                    return False, "Sai Email hoặc App Password!"
                master_token = result["Token"]

            self._keep.authenticate(email, master_token)
            self._email = email
            self._logged_in = True
            return True, "Đăng nhập thành công!"
        except gkeepapi.exception.LoginException as e:
            self._logged_in = False
            return False, f"Lỗi đăng nhập: {e}"
        except Exception as e:
            self._logged_in = False
            return False, f"Lỗi không xác định: {e}"

    def resume(self, email: str, master_token: str) -> tuple[bool, str]:
        """
        Resume session with saved token (faster than full login).
        """
        try:
            self._keep.resume(email, master_token)
            self._email = email
            self._logged_in = True
            return True, "Đã kết nối lại thành công!"
        except Exception:
            # Fall back to full login
            return self.login(email, master_token)

    def sync(self) -> tuple[bool, str]:
        """Sync notes from server."""
        if not self._logged_in:
            return False, "Chưa đăng nhập!"
        try:
            self._keep.sync()
            return True, "Đã đồng bộ dữ liệu từ Google Keep."
        except Exception as e:
            return False, f"Lỗi sync: {e}"

    def get_labels(self) -> list[str]:
        """Get all label names."""
        if not self._logged_in:
            return []
        try:
            return sorted([label.name for label in self._keep.labels()])
        except Exception:
            return []

    def get_notes(
        self,
        labels: Optional[list[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        include_trashed: bool = False,
        include_archived: bool = False,
    ) -> list[dict]:
        """
        Get notes with optional filters.
        Returns list of note dicts with: id, title, text, labels, timestamps, type, items (for lists)
        """
        if not self._logged_in:
            return []

        try:
            self._keep.sync()
        except Exception:
            pass

        notes = []
        for note in self._keep.all():
            # Skip trashed/archived unless requested
            if note.trashed and not include_trashed:
                continue
            if note.archived and not include_archived:
                continue

            # Filter by labels
            if labels:
                note_labels = [l.name for l in note.labels.all()]
                if not any(lbl in note_labels for lbl in labels):
                    continue

            # Filter by date range
            note_time = note.timestamps.updated
            if date_from and note_time < date_from:
                continue
            if date_to and note_time > date_to:
                continue

            # Build note dict
            note_dict = {
                "id": note.id,
                "title": note.title or "Untitled",
                "text": note.text or "",
                "labels": [l.name for l in note.labels.all()],
                "created": note.timestamps.created,
                "updated": note.timestamps.updated,
                "type": note.__class__.__name__,
                "pinned": note.pinned,
                "color": str(note.color) if note.color else None,
            }

            # Handle list items (for checklist notes)
            if hasattr(note, "items"):
                note_dict["items"] = [
                    {"text": item.text, "checked": item.checked}
                    for item in note.items
                ]

            notes.append(note_dict)

        # Sort by updated time descending
        notes.sort(key=lambda n: n["updated"], reverse=True)
        return notes

    def get_master_token(self) -> Optional[str]:
        """Get the current master token for saving."""
        try:
            return self._keep.getMasterToken()
        except Exception:
            return None
