import json
import queue

import os
import threading

import time

from common.mq import ParserConsumer, StreamProducer
from common.parser import MsgCsvStorage
from live import get_logger


class Consumer(object):

    def __init__(self, repo):
        self.producer = StreamProducer(get_logger('StreamProducer'))

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

        self.producer.send(StreamProducer.ROUTE_STREAM + msg['roomID'], json.dumps(msg))

    def _handler_thread(self):
        while True:
            date = time.strftime('%Y_%m_%d')
            if date != self.date:
                self.date = date
                self.storage.close()
                self.storage = MsgCsvStorage(os.path.join(self.repo, self.date))

            msg = self.jobs.get(block=True)

            self.storage.store(msg)


if __name__ == '__main__':
    import sys

    consumer = Consumer(sys.argv[1])

    p = ParserConsumer(get_logger('ParserConsumer'), msg_handler=consumer.on_msg)
    p.start()
