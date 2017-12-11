import logging
import pymongo
from metaspider.items import RoomItem, CateItem, CateCountItem
from metaspider.spiders.metadata import LiveSpider
from danmu.redis import RedisClient


class MetadataPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.logger = logging.getLogger('MetadataPL')
        self.online = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient(self.mongo_uri)
        self.mongo_db = self.mongo_client[self.mongo_db]

    def close_spider(self, spider):
        if spider.name == LiveSpider.name:
            self.mongo_db['room'].update_many({}, {'$set': {'isOnline': False}})
            self.mongo_db['room'].update_many({'rid': {'$in': list(self.online)}}, {'$set': {'isOnline': True}})

            sorted_rids = [doc['rid'] for doc in
                           self.mongo_db['room']
                               .find(filter={'isOnline': True}, projection=['rid'], sort=[('online', -1)])]

            redis_client = RedisClient()
            redis_client.save_online_rid(sorted_rids)

        self.mongo_client.close()

    def process_item(self, item, spider):

        if isinstance(item, CateCountItem):
            self.mongo_db['cate'].update_one({'cid': item['cid']},
                                             {'$set': {'roomCount': item['roomCount']}},
                                             upsert=True)
        else:
            d = dict(item)
            if d.get('rtype', -1) == RoomItem.TYPE_LIVE:
                self.online.add(d['rid'])

            if isinstance(item, RoomItem):
                d.pop('rtype')

                self.mongo_db['room'].update_one({'rid': item['rid']}, {"$set": d}, upsert=True)
                self.logger.debug('Got room %s-%s' % (item['rid'], item['roomName']))
            else:
                self.mongo_db['cate'].update_one({'cid': item['cid']}, {"$set": d}, upsert=True)
                self.logger.debug('Got cate %s-%s' % (item['cid'], item['name']))

        return item
