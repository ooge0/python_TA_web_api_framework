"""
Read values from ``config/config.ini``.

The file is parsed once and cached. A missing section or key raises (it used to
be swallowed, so callers silently received ``None``).
"""
import os
from configparser import ConfigParser, NoOptionError, NoSectionError
from functools import lru_cache

from config.logger_config import get_logger

logger = get_logger()

_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.ini")
)


@lru_cache(maxsize=1)
def _load_config() -> ConfigParser:
    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(f"config file not found: {_CONFIG_PATH}")
    config = ConfigParser()
    config.read(_CONFIG_PATH, encoding="utf-8")
    return config


def read_configuration(category: str, key: str) -> str:
    """
    Return ``config[category][key]`` from ``config/config.ini``.

    Raises:
        NoSectionError / NoOptionError: if the section or key is absent.
    """
    try:
        return _load_config().get(category, key)
    except (NoSectionError, NoOptionError) as exc:
        logger.error(f"config.ini: {exc}")
        raise
