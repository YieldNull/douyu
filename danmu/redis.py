import redis
import json


class RedisClient(object):
    KEY_ONLINE_RID = 'danmu.meta.online'

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def save_online_rid(self, rids: list):
        self.client.set(self.KEY_ONLINE_RID, json.dumps(rids))

    def load_online_rid(self) -> list:
        return json.loads(self.client.get(self.KEY_ONLINE_RID))
