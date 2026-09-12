"""
Configuration for loguru(logger) instances
"""

from loguru import logger

logger.add("./resources/logger_output/logfile.log",
           level="DEBUG",
           format="{time:YYYY-MM-DD HH:mm:ss.SSSSSS} {level} {name}:{function}:{line} - {message}",
           rotation="10 MB")


def get_logger():
    """
    Retrieve the global logger instance.

    This function returns the pre-configured logger, which can be used for
    logging messages across the application. The logger should already be
    initialized with appropriate handlers and formatters elsewhere in the
    application.

    Returns:
        logging.Logger: The global logger instance used for logging messages.
    """
    return logger
