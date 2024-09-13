from loguru import logger

logger.add("./resources/logger_output/logfile.log",
           level="DEBUG",
           format="{time:YYYY-MM-DD HH:mm:ss.SSSSSS} {level} {name}:{function}:{line} - {message}",
           rotation="10 MB")


def get_logger():
    return logger
