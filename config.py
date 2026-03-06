"""
GKeepSync - Configuration Manager
Quản lý config JSON: token, sync settings, output folder.
"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "GKeepSync"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "email": "",
    "master_token": "",
    "output_folder": str(Path.home() / "Documents" / "GKeepSync"),
    "auto_sync_enabled": False,
    "auto_sync_interval_minutes": 60,
    "filter_labels": [],
    "filter_date_from": "",
    "filter_date_to": "",
    "last_sync_time": "",
    "note_id_mapping": {},
    "window_geometry": "900x650",
    "nlm_sync_enabled": False,
    "nlm_notebook_id": "",
}


class Config:
    """Singleton config manager."""

    _instance = None
    _data: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Load config from JSON file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self._data = {**DEFAULT_CONFIG, **json.load(f)}
            except (json.JSONDecodeError, IOError):
                self._data = DEFAULT_CONFIG.copy()
        else:
            self._data = DEFAULT_CONFIG.copy()

    def save(self):
        """Save config to JSON file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value):
        self._data[key] = value

    def get_output_folder(self) -> Path:
        folder = Path(self._data.get("output_folder", DEFAULT_CONFIG["output_folder"]))
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @property
    def has_credentials(self) -> bool:
        return bool(self._data.get("email")) and bool(self._data.get("master_token"))
