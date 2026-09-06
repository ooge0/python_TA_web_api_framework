"""
loguru configuration.

The file sink path is anchored to the project root (not the current working
directory) and the ``TA_LOG_DIR`` env var can override it.
"""
import os

from loguru import logger

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR = os.environ.get("TA_LOG_DIR", os.path.join(_PROJECT_ROOT, "resources", "logger_output"))

logger.add(
    os.path.join(_LOG_DIR, "logfile.log"),
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level: <8} {name}:{function}:{line} - {message}",
    rotation="10 MB",
    retention=5,
    enqueue=True,  # safe under pytest-xdist
)


def get_logger():
    """Return the shared loguru logger."""
    return logger
