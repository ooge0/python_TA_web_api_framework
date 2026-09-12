"""
Package includes method for reading configuration
"""
import os
from configparser import ConfigParser

from config.logger_config import get_logger

logger = get_logger()


def read_configuration(category, key):
    """
    Method retrieves data (key) for specific category from 'config.ini' file

    :return: Value from 'config.ini'
    """
    # Get the directory of the current file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the config file
    config_path = os.path.join(base_dir, "../config/config.ini")

    config = ConfigParser()
    try:
        config.read(config_path)
        return config.get(category, key)
    except Exception as e:
        logger.error(f"Read configuration error: {e}")

