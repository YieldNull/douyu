import json
import queue
import os
import threading
import time
import csv
import pandas as pd
import schedule
from common.mq import ParserConsumer, StreamProducer, EmotProducer, LiveAccProducer
from common.parser import MsgCsvStorage
from common.live import RedisClient
from live import get_logger, settings


class AccManager(object):
    def __init__(self, gift_path):
        df = pd.read_csv(gift_path, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE,
                         header=1, names=['gift', 'gid', 'price'])
        self.price_map = dict()

        for _, row in df.iterrows():
            self.price_map[row['gift']] = int(row['price'])

        self.redis = RedisClient()
        self.producer = LiveAccProducer(get_logger('AccManager'))
        self.rooms = set()

    def update_acc(self, msg):
        mtype = msg['type']
        room = msg['roomID']
        self.rooms.add(room)

        self.redis.add_user(room, msg['username'])

        if mtype == 'chatmsg':
            self.redis.add_danmu(room)
        elif mtype == 'dgb':
            self.redis.add_gift(room)

            price = self.price_map.get(msg['giftID'], 600)
            self.redis.add_income(room, price)
        elif mtype == 'spbc':
            self.redis.add_gift(room)

            price = self.price_map.get(msg['giftname'], 600)
            self.redis.add_income(room, price)

    def scheduled(self, interval):
        def job():
            for room in self.rooms.copy():
                users = self.redis.clear_user(room)
                danmu = self.redis.clear_danmu(room)
                gift = self.redis.clear_gift(room)
                income = self.redis.clear_income(room)

                msg = {
                    'time': int(time.time()),
                    'user': users,
                    'danmu': danmu,
                    'gift': gift,
                    'income': income
                }

                self.producer.send(room, json.dumps(msg))

                if room == '288016':
                    print('Room:{:s} User:{:d} Danmu:{:d} Gift:{:d} Income:{:d}'.format(
                        room, users, danmu, gift, income))

        def run_threaded(job_func):
            job_thread = threading.Thread(target=job_func)
            job_thread.start()

        def poll():
            while True:
                schedule.run_pending()
                time.sleep(interval * 0.9)

        schedule.every(interval).seconds.do(run_threaded, job)
        threading.Thread(target=poll).start()


class Consumer(object):

    def __init__(self, repo, acc_manager):
        self.producer = EmotProducer(get_logger('EmotProducer'))
        self.acc_manager = acc_manager

        self.date = time.strftime('%Y_%m_%d')

        self.storage = MsgCsvStorage(os.path.join(repo, self.date))

        self.jobs = queue.Queue()

        self.repo = repo

        self.thread = threading.Thread(target=self._handler_thread)
        self.thread.start()

    def on_msg(self, msg):
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self._handler_thread)
            self.thread.start()

        self.jobs.put(msg)

        self.producer.send(json.dumps(msg))

    def _handler_thread(self):
        while True:
            date = time.strftime('%Y_%m_%d')
            if date != self.date:
                self.date = date
                self.storage.close()
                self.storage = MsgCsvStorage(os.path.join(self.repo, self.date))

            msg = self.jobs.get(block=True)

            self.storage.store(msg)
            self.acc_manager.update_acc(msg)


if __name__ == '__main__':
    import sys

    acc_manager = AccManager(settings.GIFT_PATH)
    acc_manager.scheduled(1)

    consumer = Consumer(sys.argv[1], acc_manager)

    p = ParserConsumer(get_logger('ParserConsumer'), msg_handler=consumer.on_msg)
    p.start()
