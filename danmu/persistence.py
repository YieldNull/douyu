import time
import threading
import queue
from danmu import settings, get_logger, msg
from danmu.msg import Protocol
from motor.motor_asyncio import AsyncIOMotorClient


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
        self.parser = getattr(msg, settings.PARSER_CLASS)()

        self.logger = get_logger(name)

    async def store(self, doc: dict):
        payload = doc['payload']

        if settings.MONGODB_PARSE_MSG:
            try:
                message = self.protocol.unpack_payload(self.parser, payload)
                doc.pop('payload')
                doc.update(message)
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
                line = '{:s} {:f} {:s}\n'.format(doc['rid'], doc['timestamp'],
                                                 doc['payload'][:-1].decode('utf-8'))
            except UnicodeDecodeError as e:
                self.logger.debug(repr(e))
            self.fp.write(line)
            self.logger.debug('Store ' + line)

    def store(self, doc):
        if self.thread is None:
            self.thread = threading.Thread(target=self.handler_thread)
            self.thread.start()
        self.jobs.put(doc)

    def close(self):
        if self.fp is not None:
            self.fp.close()
