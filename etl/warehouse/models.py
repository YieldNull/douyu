from etl import BaseModel, db
from peewee import IntegerField, PrimaryKeyField, ForeignKeyField, CharField, CompositeKey, BigIntegerField, DateField

TOP_TYPE_DCOUNT = 1
TOP_TYPE_GCOUNT = 2
TOP_TYPE_EXPENSE = 3


class RoomCateMap(BaseModel):
    room_key = IntegerField(index=True)
    cate_key = IntegerField(index=True)

    class Meta:
        db_table = 'map_room_cate'
        primary_key = CompositeKey('room_key', 'cate_key')


class User(BaseModel):
    user_key = IntegerField(primary_key=True)
    user_id = IntegerField(unique=True)
    name = CharField(null=True)
    level = IntegerField(null=True)

    class Meta:
        db_table = 'dw_dim_user'


class Room(BaseModel):
    room_key = PrimaryKeyField()
    room_id = IntegerField(unique=True)
    name = CharField(null=True)
    anchor = CharField(null=True)

    class Meta:
        db_table = 'dw_dim_room'


class RoomCate(BaseModel):
    cate_key = PrimaryKeyField()
    cate_id = IntegerField(unique=True)
    name = CharField()

    class Meta:
        db_table = 'dw_dim_cate'


class Hour(BaseModel):
    hour_key = PrimaryKeyField()
    hour = IntegerField()

    class Meta:
        db_table = 'dw_dim_hour'


class Date(BaseModel):
    date_key = PrimaryKeyField()
    date = DateField()
    year = IntegerField()
    month = IntegerField()
    day = IntegerField()
    weekday = IntegerField()

    class Meta:
        db_table = 'dw_dim_date'


class RoomDailyTopUser(BaseModel):
    room = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    user = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = BigIntegerField()
    ttype = IntegerField()

    class Meta:
        db_table = 'dw_fact_room_top_user_daily'


class SiteDailyTopUser(BaseModel):
    user = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = BigIntegerField()
    ttype = IntegerField()

    class Meta:
        db_table = 'dw_fact_site_top_user_daily'


class RoomHourlyStat(BaseModel):
    room = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    cate = ForeignKeyField(RoomCate, to_field=RoomCate.cate_key, db_column='cate_key')
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = BigIntegerField()

    class Meta:
        db_table = 'dw_fact_room_hourly'


class RoomDailyStat(BaseModel):
    room = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    cate = ForeignKeyField(RoomCate, to_field=RoomCate.cate_key, db_column='cate_key')
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = BigIntegerField()

    class Meta:
        db_table = 'dw_fact_room_daily'


class SiteHourlyStat(BaseModel):
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = BigIntegerField()

    class Meta:
        db_table = 'dw_fact_site_hourly'


class SiteDailyStat(BaseModel):
    date = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = BigIntegerField()

    class Meta:
        db_table = 'dw_fact_site_daily'


if __name__ == '__main__':
    db.create_tables([User, Hour, Date, Room, RoomCate, RoomCateMap,
                      RoomDailyTopUser, SiteDailyTopUser,
                      RoomHourlyStat, RoomDailyStat, SiteHourlyStat, SiteDailyStat], safe=True)
