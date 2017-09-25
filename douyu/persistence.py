import configparser
from motor.motor_asyncio import AsyncIOMotorClient


class Storage(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        client = AsyncIOMotorClient(config['mongodb']['url'])
        database = client[config['mongodb']['database']]

        self.collection = database[config['mongodb']['collection']]

    async def store(self, doc):
        await self.collection.insert_one(doc)
