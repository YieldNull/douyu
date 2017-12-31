import logging
from danmu import settings


def get_logger(name, format_str=settings.LOGGING_BASIC_FORMATTER):
    logger = logging.getLogger(name)

    if not settings.LOGGING_USE_FILE:
        handler = logging.StreamHandler(settings.LOGGING_STREAM)
        handler.setFormatter(logging.Formatter(format_str))

        logger.addHandler(handler)
        logger.setLevel(settings.LOGGING_LEVEL)
    else:
        handler = logging.FileHandler(settings.LOGGING_FILE_NAME)
        handler.setFormatter(logging.Formatter(format_str))

        logger.addHandler(handler)
        logger.setLevel(settings.LOGGING_LEVEL)
    return logger
