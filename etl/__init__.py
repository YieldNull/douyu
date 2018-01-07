import common
from peewee import Model
from etl import settings as conf
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(host=conf.MYSQL_HOST, port=conf.MYSQL_PORT,
                         user=conf.MYSQL_USER, password=conf.MYSQL_PASSWD,
                         database=conf.MYSQL_DB, charset='utf8mb4', max_connections=20)


class BaseModel(Model):
    class Meta:
        database = db


def get_logger(name):
    return common.get_logger(name, file_name=conf.LOGGING_FILE_NAME)
