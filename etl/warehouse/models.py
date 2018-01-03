from etl import BaseModel, db
from peewee import IntegerField, PrimaryKeyField, ForeignKeyField, CharField, SQL


class User(BaseModel):
    user_key = PrimaryKeyField()
    user_id = IntegerField(unique=True)
    name = CharField()
    level = IntegerField()

    class Meta:
        db_table = 'dw_dim_user'


class Room(BaseModel):
    room_key = PrimaryKeyField()
    room_id = IntegerField(unique=True)
    name = CharField()
    anchor = CharField()

    class Meta:
        db_table = 'dw_dim_room'


class Hour(BaseModel):
    hour_key = PrimaryKeyField()
    hour = IntegerField()

    class Meta:
        db_table = 'dw_dim_hour'


class Date(BaseModel):
    date_key = PrimaryKeyField()
    year = IntegerField()
    month = IntegerField()
    week = IntegerField()
    day = IntegerField()
    day_of_week = IntegerField()

    class Meta:
        db_table = 'dw_dim_date'


class DanmuFact(BaseModel):
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    amount = IntegerField()

    class Meta:
        db_table = 'dw_fact_danmu'


class GiftFact(BaseModel):
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_gift'


class RoomHourlyStatFact(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    user_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    danmu_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    gift_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    income_amount = IntegerField(constraints=[SQL('DEFAULT 0')])

    class Meta:
        db_table = 'dw_fact_room_stat_hourly'


class RoomDailyStatFact(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    user_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    danmu_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    gift_amount = IntegerField(constraints=[SQL('DEFAULT 0')])
    income_amount = IntegerField(constraints=[SQL('DEFAULT 0')])

    class Meta:
        db_table = 'dw_fact_room_stat_daily'


if __name__ == '__main__':
    db.create_tables([User, Room, Hour, Date, DanmuFact, GiftFact, RoomHourlyStatFact, RoomDailyStatFact])
