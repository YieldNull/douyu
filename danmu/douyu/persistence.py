from danmu import settings, get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from danmu.douyu.msg.protocol import Protocol


class Storage(object):
    def __init__(self, name):
        self.name = name

    def close(self):
        pass

    async def store(self, doc):
        pass


class MongodbStorage(Storage):
    def __init__(self, name):
        super().__init__(name)

        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = self.client[settings.MONGODB_DATABASE]
        self.collection = database[settings.MONGODB_COLLECTION]

        self.protocol = Protocol()

        self.logger = get_logger(name)
        self.logger.setLevel(settings.LOGGING_LEVEL)

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
