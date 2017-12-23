from peewee import Model, MySQLDatabase, CharField, IntegerField, \
    DateTimeField, PrimaryKeyField, ForeignKeyField, SQL
from etl import settings as conf

db = MySQLDatabase(host=conf.MYSQL_HOST, port=conf.MYSQL_PORT,
                   user=conf.MYSQL_USER, password=conf.MYSQL_PASSWD,
                   database=conf.MYSQL_DB, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class Room(BaseModel):
    id = PrimaryKeyField()
    rid = IntegerField(unique=True)


class Gift(BaseModel):
    TYPE_NORMAL = 1
    TYPE_SUPER = 2
    TYPE_U2U = 3

    id = PrimaryKeyField()
    name = CharField(unique=True)
    type = IntegerField()


class User(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)


class Badge(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='badges')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='badges')
    name = CharField()

    class Meta:
        constraints = [SQL('CONSTRAINT UC_name UNIQUE (roomId, userId, name)')]


class TextDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='textDanmu')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='textDanmu')
    badge = ForeignKeyField(Badge, to_field=Badge.id, db_column='badgeId', related_name='textDanmu', null=True)
    timestamp = DateTimeField()


class GiftDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='gifts')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='gifts')
    badge = ForeignKeyField(Badge, to_field=Badge.id, db_column='badgeId', related_name='gifts', null=True)
    gift = ForeignKeyField(Gift, to_field=Gift.id, db_column='giftId', related_name='gifts')
    timestamp = DateTimeField()


class UEnterDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='uenter')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='uenter')
    timestamp = DateTimeField()


class U2UDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='u2uDanmu')
    sender = ForeignKeyField(User, to_field=User.id, db_column='senderId', related_name='u2uDanmu_sender')
    receiver = ForeignKeyField(User, to_field=User.id, db_column='receiverId', related_name='u2uDanmu_receiver')
    gift = ForeignKeyField(Gift, to_field=Gift.id, db_column='giftId', related_name='u2uDanmu')
    timestamp = DateTimeField()


if __name__ == '__main__':
    db.create_tables([Room, User, Gift, Badge, TextDanmu, GiftDanmu, UEnterDanmu, U2UDanmu], safe=True)
