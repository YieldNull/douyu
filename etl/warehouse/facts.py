import os
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor
from etl.warehouse.dims import gen_date
from etl.warehouse.models import *
from etl import get_logger


class RDS(object):
    def __init__(self, repo, date):
        self.repo = repo
        self.date = date
        self.executor = ThreadPoolExecutor(10)
        self.dates = gen_date()

        self.logger = get_logger("ETL-FACT")

    def store(self):
        futures = []
        futures.append(self.executor.submit(self._store_top_user, is_site=False))
        futures.append(self.executor.submit(self._store_top_user, is_site=True))

        futures.append(self.executor.submit(self._store_stat, is_site=False, is_daily=False))
        futures.append(self.executor.submit(self._store_stat, is_site=False, is_daily=True))
        futures.append(self.executor.submit(self._store_stat, is_site=True, is_daily=False))
        futures.append(self.executor.submit(self._store_stat, is_site=True, is_daily=True))

        self.executor.shutdown(wait=True)

        for fu in futures:
            exp = fu.exception()
            if exp is not None:
                self.logger.warning(repr(exp))

    def _store_top_user(self, is_site):
        date_str = self.date.strftime("%Y_%m_%d")

        d = {'order_by_dcount': TOP_TYPE_DCOUNT,
             'order_by_gcount': TOP_TYPE_GCOUNT,
             'order_by_expense': TOP_TYPE_EXPENSE,
             }

        time_type = 'daily'
        target_type = 'site' if is_site else 'room'

        for suffix, ttype in d.items():
            fname = '%s_%s_top_user_%s_%s.csv' % (date_str, target_type, time_type, suffix)
            df = pd.read_csv(os.path.join(self.repo, fname))

            for index, row in df.iterrows():
                try:
                    date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                    user_key = row['user']
                    # User.get_or_create(user_key=user_key, defaults={'user_id': user_key})

                    dcount = row['dcount']
                    gcount = row['gcount']
                    expense = row['expense']

                    if is_site:
                        SiteDailyTopUser.create(user=user_key, date=date_key,
                                                dcount=dcount, gcount=gcount, expense=expense, ttype=ttype)
                    else:
                        room, _ = Room.get_or_create(room_key=row['room'], room_id=row['room'])
                        room_key = room.room_key

                        RoomDailyTopUser.create(room=room_key, user=user_key,
                                                date_key=date_key,
                                                dcount=dcount, gcount=gcount, expense=expense, ttype=ttype)
                except Exception:
                    self.logger.exception('{} index:{} {}'.format(fname, index, repr(row)))

    def _store_stat(self, is_site, is_daily):
        date_str = self.date.strftime("%Y_%m_%d")

        time_type = 'daily' if is_daily else 'hourly'
        target_type = 'site' if is_site else 'room'

        fname = '%s_%s_%s.csv' % (date_str, target_type, time_type)
        df = pd.read_csv(os.path.join(self.repo, fname))

        for index, row in df.iterrows():
            try:

                date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                ucount = row['ucount']
                ducount = row['ducount']
                gucount = row['gucount']
                dcount = row['dcount']
                gcount = row['gcount']
                income = row['income']

                if is_site:
                    if is_daily:
                        SiteDailyStat.create(date=date_key,
                                             ucount=ucount, ducount=ducount, gucount=gucount,
                                             dcount=dcount, gcount=gcount, income=income)
                    else:
                        hour_key = row['hour'] + 1
                        SiteHourlyStat.create(date=date_key, hour=hour_key,
                                              ucount=ucount, ducount=ducount, gucount=gucount,
                                              dcount=dcount, gcount=gcount, income=income)

                else:
                    room, _ = Room.get_or_create(room_key=row['room'], room_id=row['room'])
                    room_key = room.room_key

                    try:
                        cate_map = RoomCateMap.get(RoomCateMap.room_key == int(row['room']))
                    except:
                        self.logger.warning('ROOM NOT RECORDED! {} index:{} {}'.format(fname, index, row['room']))
                        continue

                    cate_key = cate_map.cate_key

                    if is_daily:
                        RoomDailyStat.create(room=room_key, date=date_key, cate=cate_key,
                                             ucount=ucount, ducount=ducount, gucount=gucount,
                                             dcount=dcount, gcount=gcount, income=income)
                    else:
                        hour_key = row['hour'] + 1

                        RoomHourlyStat.create(room=room_key, cate=cate_key,
                                              date=date_key, hour=hour_key,
                                              ucount=ucount, ducount=ducount, gucount=gucount,
                                              dcount=dcount, gcount=gcount, income=income)
            except Exception:
                self.logger.exception('{} index:{} {}'.format(fname, index, repr(row)))


if __name__ == '__main__':
    import sys

    print("Parsing %s" % sys.argv[2])
    rds = RDS(sys.argv[1], datetime.datetime.strptime(sys.argv[2], "%Y_%m_%d"))
    rds.store()
