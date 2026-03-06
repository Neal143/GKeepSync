"""
GKeepSync - Logger
File-based logging with rotation.
"""

import logging
import os
from pathlib import Path

LOG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "GKeepSync" / "logs"


def setup_logger(name: str = "gkeepsync") -> logging.Logger:
    """Setup file + console logger."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler
    from logging.handlers import RotatingFileHandler

    fh = RotatingFileHandler(
        LOG_DIR / "gkeepsync.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# Global logger instance
logger = setup_logger()
