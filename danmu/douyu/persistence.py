from danmu import settings
from motor.motor_asyncio import AsyncIOMotorClient


class Storage(object):
    def __init__(self):
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.MONGODB_DATABASE]

        self.collection = database[settings.MONGODB_COLLECTION]

    async def store(self, doc):
        await self.collection.insert_one(doc)
