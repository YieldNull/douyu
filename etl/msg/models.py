from etl import BaseModel, db
from peewee import CharField, IntegerField, DateTimeField, PrimaryKeyField, ForeignKeyField


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
    # level = IntegerField()


class TextDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='textDanmu')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='textDanmu')
    timestamp = DateTimeField()


class GiftDanmu(BaseModel):
    id = PrimaryKeyField()
    room = ForeignKeyField(Room, to_field=Room.id, db_column='roomId', related_name='gifts')
    user = ForeignKeyField(User, to_field=User.id, db_column='userId', related_name='gifts')
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
    db.create_tables([Room, User, Gift, TextDanmu, GiftDanmu, UEnterDanmu, U2UDanmu], safe=True)
