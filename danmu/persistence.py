import time
import threading
import queue
import json
from danmu.mq import RawProducer
from danmu import settings, get_logger


class Storage(object):
    def __init__(self, name):
        self.name = name

    def close(self):
        pass

    def store(self, doc):
        pass


class FileStorage(Storage):
    def __init__(self, name):
        super().__init__(name)

        self.name = name
        self.date = ''
        self.fp = None
        self.jobs = queue.Queue()
        self.logger = get_logger(name)

        self.producer = RawProducer(host=settings.MQ_PARSER_ADDRESS, port=settings.MQ_PARSER_PORT)

        self.thread = threading.Thread(target=self.handler_thread)
        self.thread.start()

    def handler_thread(self):
        while True:
            doc = self.jobs.get(block=True)

            date = time.strftime(settings.FILE_STORAGE_DATE_FORMAT)
            if date != self.date:
                if self.fp is not None:
                    self.fp.close()

                self.date = date
                filename = settings.FILE_STORAGE_NAME_FORMAT.format(name=self.name, date=self.date)
                self.fp = open(filename, 'a', encoding='utf-8')

            try:
                raw = doc['payload'][:-1].decode('utf-8')

                line = '{:s} {:f} {:s}\n'.format(doc['rid'], doc['timestamp'], raw)
                self.fp.write(line)
                self.logger.debug('Store ' + line)

                self.producer.send(route=RawProducer.ROUTE_PARSER,
                                   msg=json.dumps({'rid': doc['rid'], 'ts': doc['timestamp'], 'raw': raw}))

            except UnicodeDecodeError as e:
                self.logger.debug(repr(e))

    def store(self, doc):
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.handler_thread)
            self.thread.start()
            self.logger.warn("Working thread was dead. Restarting")

        self.jobs.put(doc)

    def close(self):
        if self.fp is not None:
            self.fp.close()
