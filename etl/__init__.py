import logging
from peewee import Model
from etl import settings as conf
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(host=conf.MYSQL_HOST, port=conf.MYSQL_PORT,
                         user=conf.MYSQL_USER, password=conf.MYSQL_PASSWD,
                         database=conf.MYSQL_DB, charset='utf8mb4', max_connections=20)


class BaseModel(Model):
    class Meta:
        database = db


def get_logger(name, format_str=conf.LOGGING_BASIC_FORMATTER):
    logger = logging.getLogger(name)

    if len(logger.handlers) == 0:
        handler = logging.FileHandler(conf.LOGGING_FILE_NAME)
        handler.setFormatter(logging.Formatter(format_str))
        handler.setLevel(conf.LOGGING_LEVEL)

        logger.addHandler(handler)
        logger.setLevel(conf.LOGGING_LEVEL)

    return logger
