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
        self.executor.submit(self._store_room_top_user_hourly)
        self.executor.submit(self._store_room_top_user_daily)
        self.executor.submit(self._store_site_top_user_hourly)
        self.executor.submit(self._store_site_top_user_daily)
        self.executor.submit(self._store_room_stat_hourly)
        self.executor.submit(self._store_room_stat_daily)
        self.executor.submit(self._store_site_stat_hourly)
        self.executor.submit(self._store_site_stat_daily)
        self.executor.shutdown(wait=True)

    def _store_room_top_user_hourly(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_room_top_user_hourly.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                room, _ = Room.get_or_create(room_id=row['room'])

                user_key = row['user']
                room_key = room.room_key

                date_key = self.dates[self.date.strftime("%Y_%m_%d")]
                hour_key = row['hour'] + 1

                RoomHourlyTopUser.create(room_key=room_key, user_key=user_key,
                                         date_key=date_key, hour_key=hour_key,
                                         dcount=row['dcount'], gcount=row['gcount'],
                                         expense=row['expense'])
            except Exception:
                self.logger.exception("ROOM TOP USER HOURLY")

    def _store_room_top_user_daily(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_room_top_user_daily.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                room, _ = Room.get_or_create(room_id=row['room'])

                user_key = row['user']
                room_key = room.room_key

                date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                RoomDailyTopUser.create(room_key=room_key, user_key=user_key, date_key=date_key,
                                        dcount=row['dcount'], gcount=row['gcount'],
                                        expense=row['expense'])
            except Exception:
                self.logger.exception("ROOM TOP USER DAILY")

    def _store_site_top_user_hourly(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_site_top_user_hourly.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                user_key = row['user']
                date_key = self.dates[self.date.strftime("%Y_%m_%d")]
                hour_key = row['hour'] + 1

                SiteHourlyTopUser.create(user_key=user_key, date_key=date_key, hour_key=hour_key,
                                         dcount=row['dcount'], gcount=row['gcount'],
                                         expense=row['expense'])
            except Exception:
                self.logger.exception("SITE TOP USER HOURLY")

    def _store_site_top_user_daily(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_site_top_user_daily.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                user_key = row['user']
                date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                SiteDailyTopUser.create(user_key=user_key, date_key=date_key,
                                        dcount=row['dcount'], gcount=row['gcount'],
                                        expense=row['expense'])
            except Exception:
                self.logger.exception("SITE TOP USER DAILY")

    def _store_room_stat_hourly(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_room_hourly.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                room, _ = Room.get_or_create(room_id=row['room'])
                room_key = room.room_key

                date_key = self.dates[self.date.strftime("%Y_%m_%d")]
                hour_key = row['hour'] + 1

                RoomHourlyStat.create(room_key=room_key, date_key=date_key, hour_key=hour_key,
                                      ucount=row['ucount'], ducount=row['ducount'], gucount=row['gucount'],
                                      dcount=row['dcount'], gcount=row['gcount'], income=row['income'])
            except Exception:
                self.logger.exception("ROOM STAT HOURLY")

    def _store_room_stat_daily(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_room_daily.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                room, _ = Room.get_or_create(room_id=row['room'])
                room_key = room.room_key

                date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                RoomDailyStat.create(room_key=room_key, date_key=date_key,
                                     ucount=row['ucount'], ducount=row['ducount'], gucount=row['gucount'],
                                     dcount=row['dcount'], gcount=row['gcount'], income=row['income'])
            except Exception:
                self.logger.exception("ROOM STAT DAILY")

    def _store_site_stat_hourly(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_site_hourly.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                date_key = self.dates[self.date.strftime("%Y_%m_%d")]
                hour_key = row['hour'] + 1

                SiteHourlyStat.create(date_key=date_key, hour_key=hour_key,
                                      ucount=row['ucount'], ducount=row['ducount'], gucount=row['gucount'],
                                      dcount=row['dcount'], gcount=row['gcount'], income=row['income'])
            except Exception:
                self.logger.exception("SITE STAT HOURLY")

    def _store_site_stat_daily(self):
        df = pd.read_csv(os.path.join(self.repo, '%s_site_daily.csv' % self.date.strftime("%Y_%m_%d")))

        for index, row in df.iterrows():
            try:
                date_key = self.dates[self.date.strftime("%Y_%m_%d")]

                SiteDailyStat.create(date_key=date_key,
                                     ucount=row['ucount'], ducount=row['ducount'], gucount=row['gucount'],
                                     dcount=row['dcount'], gcount=row['gcount'], income=row['income'])
            except Exception:
                self.logger.exception("SITE STAT DAILY")


if __name__ == '__main__':
    import sys

    print("Parsing %s" % sys.argv[2])
    rds = RDS(sys.argv[1], datetime.datetime.strptime(sys.argv[2], "%Y_%m_%d"))
    rds.store()
