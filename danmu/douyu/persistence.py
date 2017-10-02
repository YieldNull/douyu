import time
import threading
import queue
from danmu import settings, get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from danmu.douyu.msg.protocol import Protocol


class Storage(object):
    def __init__(self, name):
        self.name = name

    def close(self):
        pass

    def store(self, doc):
        pass


class MongodbStorage(Storage):
    def __init__(self, name):
        super().__init__(name)

        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = self.client[settings.MONGODB_DATABASE]
        self.collection = database[settings.MONGODB_COLLECTION]

        self.protocol = Protocol()

        self.logger = get_logger(name)

    async def store(self, doc: dict):
        payload = doc['payload']

        if settings.MONGODB_PARSE_MSG:
            try:
                msg = self.protocol.unpack_payload(payload, len(payload))
                doc.pop('payload')
                doc.update(msg)
            except UnicodeDecodeError as e:
                self.logger.warning('Discard packet for ' + repr(e))
                return

        doc['payload'] = payload[:-1].decode('utf-8')

        self.logger.debug('Store ' + repr(doc))

        await self.collection.insert_one(doc)

    def close(self):
        self.client.close()


class FileStorage(Storage):
    def __init__(self, name):
        super().__init__(name)

        self.name = name
        self.date = ''
        self.fp = None
        self.thread = None
        self.jobs = queue.Queue()
        self.logger = get_logger(name)

    def handle_thread(self):
        while True:
            doc = self.jobs.get(block=True)

            date = time.strftime("%Y_%m_%d")
            if date != self.date:
                if self.fp is not None:
                    self.fp.close()
                self.date = date
                self.fp = open('{:s}_{:s}.txt'.format(self.name, self.date), 'a', encoding='utf-8')

            try:
                line = '{:s} {:f} {:s}\n'.format(doc['rid'], doc['timestamp'],
                                                 doc['payload'][:-1].decode('utf-8'))
            except UnicodeDecodeError as e:
                self.logger.warning(repr(e))
            self.fp.write(line)
            self.logger.debug('Store ' + line)

    def store(self, doc):
        if self.thread is None:
            self.thread = threading.Thread(target=self.handle_thread)
            self.thread.start()
        self.jobs.put(doc)

    def close(self):
        if self.fp is not None:
            self.fp.close()
