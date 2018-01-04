from etl import BaseModel, db
from peewee import IntegerField, PrimaryKeyField, ForeignKeyField, CharField, SQL


class User(BaseModel):
    user_key = IntegerField(primary_key=True)
    user_id = IntegerField()
    name = CharField(index=True)
    level = IntegerField()

    class Meta:
        db_table = 'dw_dim_user'


class Room(BaseModel):
    room_key = PrimaryKeyField()
    room_id = IntegerField()
    name = CharField(null=True)
    anchor = CharField(null=True)

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
    day = IntegerField()
    weekday = IntegerField()

    class Meta:
        db_table = 'dw_dim_date'


class UserRoomHourlyStat(BaseModel):
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_user_room_hourly'


class RoomHourlyTopUser(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_room_top_user_hourly'


class RoomDailyTopUser(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_room_top_user_daily'


class SiteHourlyTopUser(BaseModel):
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_site_top_user_hourly'


class SiteDailyTopUser(BaseModel):
    user_key = ForeignKeyField(User, to_field=User.user_key, db_column='user_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    dcount = IntegerField()
    gcount = IntegerField()
    expense = IntegerField()

    class Meta:
        db_table = 'dw_fact_site_top_user_daily'


class RoomHourlyStat(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = IntegerField()

    class Meta:
        db_table = 'dw_fact_room_hourly'


class RoomDailyStat(BaseModel):
    room_key = ForeignKeyField(Room, to_field=Room.room_key, db_column='room_key')
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = IntegerField()

    class Meta:
        db_table = 'dw_fact_room_daily'


class SiteHourlyStat(BaseModel):
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    hour_key = ForeignKeyField(Hour, to_field=Hour.hour_key, db_column='hour_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = IntegerField()

    class Meta:
        db_table = 'dw_fact_site_hourly'


class SiteDailyStat(BaseModel):
    date_key = ForeignKeyField(Date, to_field=Date.date_key, db_column='date_key')
    ucount = IntegerField()
    ducount = IntegerField()
    gucount = IntegerField()
    dcount = IntegerField()
    gcount = IntegerField()
    income = IntegerField()

    class Meta:
        db_table = 'dw_fact_site_daily'


if __name__ == '__main__':
    db.create_tables([User, Room, Hour, Date,
                      RoomHourlyTopUser, RoomDailyTopUser, SiteHourlyTopUser, SiteDailyTopUser,
                      RoomHourlyStat, RoomDailyStat, SiteHourlyStat, SiteDailyStat], safe=True)
