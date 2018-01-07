import common
from live import settings


def get_logger(name):
    return common.get_logger(name, file_name=settings.LOGGING_FILE)
