import logging
import pymongo
from metaspider.items import RoomItem, CateItem


class MetadataPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.logger = logging.getLogger('MetadataPL')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, RoomItem):
            self.db['room'].update_one({'rid': item['rid']}, {"$set": dict(item)}, upsert=True)
            self.logger.info('Got room %s-%s' % (item['rid'], item['roomName']))
        elif isinstance(item, CateItem):
            self.db['cate'].update_one({'cid': item['cid']}, {"$set": dict(item)}, upsert=True)
            self.logger.info('Got cate %s-%s' % (item['cid'], item['name']))

        return item
