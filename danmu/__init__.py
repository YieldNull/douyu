import logging
from danmu import settings


def get_logger(name, format_str=settings.LOGGING_BASIC_FORMATTER):
    logger = logging.getLogger(name)

    if len(logger.handlers) == 0:
        if not settings.LOGGING_USE_FILE:
            handler = logging.StreamHandler(settings.LOGGING_STREAM)
            handler.setFormatter(logging.Formatter(format_str))

            logger.addHandler(handler)
            logger.setLevel(settings.LOGGING_LEVEL)
        else:
            handler = logging.FileHandler(settings.LOGGING_FILE_NAME)
            handler.setFormatter(logging.Formatter(format_str))
            handler.setLevel(settings.LOGGING_LEVEL)

            logger.addHandler(handler)
            logger.setLevel(settings.LOGGING_LEVEL)

            handler = logging.FileHandler('%s_WARNING.log' % settings.LOGGING_FILE_NAME)
            handler.setFormatter(logging.Formatter(format_str))
            handler.setLevel(logging.WARNING)

            logger.addHandler(handler)

    return logger
