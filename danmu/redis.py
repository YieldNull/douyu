import redis
import json


class RedisClient(object):
    KEY_DANMU_META = 'danmu.meta'

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def save_meta(self, data):
        self.client.set(self.KEY_DANMU_META, json.dumps(data))

    def load_meta(self):
        return json.loads(self.client.get(self.KEY_DANMU_META))
