import redis


class RedisClient(object):

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def save_room(self, id_, rid):
        self.client.set('r{}'.format(rid), id_)

    def get_room(self, rid):
        return self.client.get('r{}'.format(rid))

    def save_user(self, id_, name):
        self.client.set('u{}'.format(name), id_)

    def get_user(self, name):
        return self.client.get('u{}'.format(name))

    def save_gift_normal(self, id_, name):
        self.client.set('gn{}'.format(name), id_)

    def get_gift_normal(self, name):
        return self.client.get('gn{}'.format(name))

    def save_gift_super(self, id_, name):
        self.client.set('gs{}'.format(name), id_)

    def get_gift_super(self, name):
        return self.client.get('gs{}'.format(name))

    def save_gift_u2u(self, id_, name):
        self.client.set('gu{}'.format(name), id_)

    def get_gift_u2u(self, name):
        return self.client.get('gu{}'.format(name))
