import customtkinter as ctk
import os
import json

CONFIG_FILE = "config.json"

class ConfigManager:
    @staticmethod
    def load_config():
        """Đọc config từ file hoặc trả về default nếu file không tồn tại."""
        default_config = {
            "email": "",
            "master_token": "",
            "sync_folder": "",
            "auto_sync_interval": "Off",
            "nlm_auto_upload": False,
            "active_notebook_id": ""
        }
        
        if not os.path.exists(CONFIG_FILE):
            return default_config
            
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge with default to ensure all keys exist
                for k, v in default_config.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config

    @staticmethod
    def save_config(config_data):
        """Lưu config xuống disk."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    @staticmethod
    def update_key(key, value):
        config = ConfigManager.load_config()
        config[key] = value
        return ConfigManager.save_config(config)
