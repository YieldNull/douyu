import logging
import danmu.settings


def get_logger(name, format_str=settings.LOGGING_BASIC_FORMATTER):
    logger = logging.getLogger(name)

    if len(logger.handlers) == 0:
        handler = logging.StreamHandler(settings.LOGGING_STREAM)
        handler.setFormatter(
            logging.Formatter(format_str))

        logger.addHandler(handler)
        logger.setLevel(settings.LOGGING_LEVEL)

    return logger
