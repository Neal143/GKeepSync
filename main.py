"""
GKeepSync - Entry Point
Sync Google Keep notes to local Markdown files.
"""

import sys
import os

# Ensure the app directory is in path
if getattr(sys, 'frozen', False):
    # Running as compiled .exe
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, APP_DIR)

from app import GKeepSyncApp
from utils.logger import logger


def main():
    logger.info("GKeepSync starting...")
    try:
        app = GKeepSyncApp()
        app.mainloop()
    except Exception as e:
        logger.critical("Fatal error: %s", e, exc_info=True)
        raise
    finally:
        logger.info("GKeepSync shutting down.")


if __name__ == "__main__":
    main()
