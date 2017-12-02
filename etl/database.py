from peewee import MySQLDatabase, Model, CharField, IntegerField, TimestampField, TextField
from etl import settings as conf

db = MySQLDatabase(host=conf.MYSQL_HOST, port=conf.MYSQL_PORT,
                   user=conf.MYSQL_USER, password=conf.MYSQL_PASSWD,
                   database=conf.MYSQL_DB, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class ChatMsg(BaseModel):
    timestamp = TimestampField()
    username = CharField()
    user_level = IntegerField()
    badge_name = CharField()
    badge_level = IntegerField()
    room_id = CharField()
    broom_id = CharField()
    content = TextField()


class GiftMsg(BaseModel):
    timestamp = TimestampField()
    username = CharField()
    user_level = IntegerField()
    gift_id = IntegerField()
    badge_name = CharField()
    badge_level = IntegerField()
    room_id = CharField()
    broom_id = CharField()
    hits = IntegerField()


class SuperMsg(BaseModel):
    timestamp = TimestampField()
    username = CharField()
    gift_name = CharField()
    badge_name = CharField()
    badge_level = IntegerField()
    room_id = CharField()
    broom_id = CharField()
    hits = IntegerField()
