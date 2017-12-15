import redis


class RedisClient(object):
    CHANNEL_TEMP_RID = 'danmu.rid.temporary'

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def listen_temporary_rid(self):
        pubsub = self.client.pubsub()
        pubsub.subscribe([self.CHANNEL_TEMP_RID])
        return pubsub.listen()

    def publish_temporary_rid(self, rid):
        self.client.publish(self.CHANNEL_TEMP_RID, rid)
