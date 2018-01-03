from peewee import Model, MySQLDatabase
from etl import settings as conf

db = MySQLDatabase(host=conf.MYSQL_HOST, port=conf.MYSQL_PORT,
                   user=conf.MYSQL_USER, password=conf.MYSQL_PASSWD,
                   database=conf.MYSQL_DB, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db
