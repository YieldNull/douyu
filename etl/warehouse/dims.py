import redis
import datetime
import pickle
from etl.warehouse.models import Date, Hour, User


def gen_date(insert=False):
    start = datetime.datetime(2017, 11, 1)
    end = datetime.datetime(2020, 1, 1)

    dates = {}

    dt = start
    key = 1
    while dt <= end:
        if insert:
            Date.create(year=dt.year, month=dt.month, day=dt.day, weekday=dt.isoweekday())

        dates[dt.strftime("%Y_%m_%d")] = key

        key += 1
        dt += datetime.timedelta(days=1)

    return dates


def gen_hour():
    for i in range(0, 24):
        Hour.create(hour=i)


def store_user():
    client = redis.StrictRedis(decode_responses=True)

    for key in client.scan_iter(match='u:*'):
        user_id, level = pickle.loads(client.get(key))

        User.create(user_key=user_id, user_id=user_id, name=key[2:], level=level)


if __name__ == '__main__':
    gen_date(True)
    gen_hour()

    store_user()
