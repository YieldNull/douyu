import redis
import pickle
from etl import settings


class RedisClient(object):

    def __init__(self, file_prefix):
        self.client = redis.StrictRedis(decode_responses=True)
        self.fd_user = open(file_prefix + '_new_user.txt', 'w', encoding='utf-8')

    def close(self):
        self.fd_user.close()

    def save_user(self, name, level):
        key = 'u:{}'.format(name)

        return self._incr_and_save(key,
                                   self._incr_user_id,
                                   lambda id_: pickle.dumps((id_, level)),
                                   lambda v: v[0],
                                   lambda id_: '%s\t%s\t%s' % (str(id_), key[2:], str(level)))

    def update_user(self, id_, name, level):
        return self.client.set('u:{}'.format(name), pickle.dumps((id_, level)))

    def get_user(self, name):
        r = self.client.get('u:{}'.format(name))
        return pickle.loads(r) if r is not None else None

    def save_gift_normal(self, name):
        key = 'gn:{}'.format(name)

        return self._incr_and_save(key,
                                   self._incr_gift_id,
                                   lambda id_: id_,
                                   lambda x: x)

    def get_gift_normal(self, name):
        return self.client.get('gn:{}'.format(name))

    def save_gift_super(self, name):
        key = 'gs:{}'.format(name)

        return self._incr_and_save(key,
                                   self._incr_gift_id,
                                   lambda id_: id_,
                                   lambda x: x)

    def get_gift_super(self, name):
        return self.client.get('gs:{}'.format(name))

    def save_gift_u2u(self, name):
        key = 'gu:{}'.format(name)

        return self._incr_and_save(key,
                                   self._incr_gift_id,
                                   lambda id_: id_,
                                   lambda x: x)

    def get_gift_u2u(self, name):
        return self.client.get('gu:{}'.format(name))

    def _incr_user_id(self):
        return self.client.incr('uid')

    def _incr_gift_id(self):
        return self.client.incr('gid')

    def _incr_room_id(self):
        return self.client.incr('rid')

    def _incr_and_save(self, key, func_incr, func_value, func_load, func_csv=None):
        id_ = func_incr()

        if self.client.setnx(key, func_value(id_)):
            if settings.SAVE_NEW_ITEM and func_csv is not None:
                self.fd_user.write('%s\n' % (func_csv(id_)))
            return id_
        else:
            return func_load(self.client.get(key))
