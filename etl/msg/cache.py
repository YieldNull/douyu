import redis
import pickle


class RedisClient(object):

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def save_room(self, id_, rid):
        return self.client.set('r{}'.format(rid), id_)

    def get_room(self, rid):
        return self.client.get('r{}'.format(rid))

    def save_user(self, id_, name, level):
        return self.client.set('u{}'.format(name), pickle.dumps((id_, level)))

    def get_user(self, name):
        return pickle.loads(self.client.get('u{}'.format(name)))

    def save_gift_normal(self, id_, name):
        return self.client.set('gn{}'.format(name), id_)

    def get_gift_normal(self, name):
        return self.client.get('gn{}'.format(name))

    def save_gift_super(self, id_, name):
        return self.client.set('gs{}'.format(name), id_)

    def get_gift_super(self, name):
        return self.client.get('gs{}'.format(name))

    def save_gift_u2u(self, id_, name):
        return self.client.set('gu{}'.format(name), id_)

    def get_gift_u2u(self, name):
        return self.client.get('gu{}'.format(name))

    def incr_user_id(self):
        return self.client.incr('uid')

    def incr_gift_id(self):
        return self.client.incr('gid')

    def incr_room_id(self):
        return self.client.incr('rid')
