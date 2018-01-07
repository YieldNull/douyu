import common
from danmu import settings


def get_logger(name, format_str=settings.LOGGING_BASIC_FORMATTER):
    return common.get_logger(name,
                             level=settings.LOGGING_LEVEL,
                             file_name=settings.LOGGING_FILE_NAME,
                             sep_warning=True,
                             format_str=format_str)
