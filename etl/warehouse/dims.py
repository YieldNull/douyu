import redis
import datetime
import pickle
import pandas as pd
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


def store_gift(path):
    client = redis.StrictRedis(decode_responses=True)

    data = []
    for key in client.scan_iter(match='g[ns]:*'):
        gift = key[3:]
        gid = client.get(key)

        gn = 0
        try:
            gn = int(gift)
        except:
            pass

        price = {
            0: 200000,  # super gift
            191: 1,  # 鱼丸
            192: 10,  # 赞
            702: 20,  # 续命
            705: 600,  # 办卡
            195: 10000,  # Egay
            196: 50000,  # 火箭
            1005: 200000,  # 超级火箭
        }.get(gn, 600)  # ￥6 for unknown gift

        data.append((gift, gid, price))
    pd.DataFrame(data).to_csv(path, header=['gift', 'gid', 'price'], sep='\t', index=False)


if __name__ == '__main__':
    # gen_date(True)
    # gen_hour()
    #
    # store_user()
    store_gift('gift_price.csv')
