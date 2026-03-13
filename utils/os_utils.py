"""
os_utils.py - Quản lý khởi động cùng Windows.

Dùng Registry Run Key để khởi động tức thì.
Yêu cầu ứng dụng nằm trên ổ đĩa vật lý (C:, D:...) thay vì ổ ảo (như G: Google Drive)
để Windows gọi được file .exe ngay lập tức khi boot.
"""

import os
import sys
from utils.logger import logger
import winreg

APP_NAME = "GKeepSync"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def get_executable_path():
    """Return the executable path or python script path."""
    if getattr(sys, 'frozen', False):
        return f'"{sys.executable}" --startup'
    else:
        # If running from source, try to get absolute path to python.exe and main.py
        python_exe = sys.executable
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(script_dir, "main.py")
        return f'"{python_exe}" "{main_script}" --startup'


def _cleanup_old_task_scheduler_and_startup_folder():
    """Remove old Task Scheduler entry and Startup folder batch if they exist."""
    # Cleanup Task Scheduler
    try:
        import subprocess
        subprocess.run(
            ["schtasks", "/Delete", "/TN", "GKeepSync_AutoStart", "/F"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass

    # Cleanup Startup folder
    try:
        startup_folder = os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )
        bat_path = os.path.join(startup_folder, "GKeepSync_AutoStart.bat")
        if os.path.exists(bat_path):
            os.remove(bat_path)
    except Exception:
        pass


def enable_startup():
    """Add app to Windows startup via Registry."""
    try:
        # Dọn dẹp cách cũ nếu còn sót lại
        _cleanup_old_task_scheduler_and_startup_folder()

        app_path = get_executable_path()
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
        logger.info("Enabled Run on Startup via Registry")
        return True
    except Exception as e:
        logger.error(f"Failed to enable startup: {e}")
        return False


def disable_startup():
    """Remove app from Windows startup."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        try:
            winreg.DeleteValue(key, APP_NAME)
        except object:  # ignore missing key # FileNotFoundError doesn't always catch it on winreg
            pass  
        winreg.CloseKey(key)
        logger.info("Disabled Run on Startup from Registry")
        return True
    except Exception as e:
        logger.error(f"Failed to disable startup: {e}")
        return False


def check_startup_status():
    """Check if app is in Windows startup and paths match."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return value == get_executable_path()
        except object:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False
