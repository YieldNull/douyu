import logging
from etl.msg.models import *
from etl.msg.cache import RedisClient


class TextStorage(object):
    def __init__(self, file_prefix):

        self.file_prefix = file_prefix
        self.logger = logging.getLogger('TextStorage-%s' % self.file_prefix)

        self.redis = RedisClient()

        self.fd_text = open(self.file_prefix + '_text.txt', 'w', buffering=1024 * 128, encoding='utf-8')
        self.fd_gift = open(self.file_prefix + '_gift.txt', 'w', buffering=1024 * 128, encoding='utf-8')
        self.fd_uenter = open(self.file_prefix + '_uenter.txt', 'w', buffering=1024 * 128, encoding='utf-8')
        self.fd_u2u = open(self.file_prefix + '_u2u.txt', 'w', buffering=1024 * 128, encoding='utf-8')

    def store(self, msg):
        try:
            _type = msg['type']

            msg['time'] = int(float(msg['time']))  # datetime.fromtimestamp(float(msg['time']))

            if _type == 'chatmsg':
                self._store_text(msg)
            elif _type == 'dgb':
                self._store_normal_gift(msg)
            elif _type == 'spbc':
                self._store_super_gift(msg)
            elif _type == 'gpbc':
                self._store_u2u(msg)
            elif _type == 'uenter':
                self._store_uenter(msg)
        except Exception as e:
            self.logger.exception("\nError in storing msg:%s\n" % repr(msg))

    def close(self):
        self.fd_text.close()
        self.fd_gift.close()
        self.fd_uenter.close()
        self.fd_u2u.close()

    def _store_text(self, msg):
        user = self.get_or_create(User, name=msg['username'], defaults={'level': int(msg['userlevel'])})
        room = self.get_or_create(Room, rid=int(msg['roomID']))

        self.create_danmu(TextDanmu, room=room, user=user, timestamp=msg['time'])

    def _store_normal_gift(self, msg):
        user = self.get_or_create(User, name=msg['username'], defaults={'level': int(msg['userlevel'])})
        room = self.get_or_create(Room, rid=int(msg['roomID']))

        gift = self.get_or_create(Gift, name=msg['giftID'], defaults={'type': Gift.TYPE_NORMAL})

        self.create_danmu(GiftDanmu, room=room, user=user, gift=gift, timestamp=msg['time'])

    def _store_super_gift(self, msg):
        if msg['roomID'] != msg['droomID']:  # dup filter
            return

        user = self.get_or_create(User, name=msg['username'])
        room = self.get_or_create(Room, rid=int(msg['roomID']))
        gift = self.get_or_create(Gift, name=msg['giftname'], defaults={'type': Gift.TYPE_SUPER})

        self.create_danmu(GiftDanmu, room=room, user=user, gift=gift, timestamp=msg['time'])

    def _store_u2u(self, msg):
        room = self.get_or_create(Room, rid=int(msg['roomID']))
        gift = self.get_or_create(Gift, name=msg['pnm'], defaults={'type': Gift.TYPE_U2U})
        sender = self.get_or_create(User, name=msg['username'])
        receiver = self.get_or_create(User, name=msg['rusername'])

        self.create_danmu(U2UDanmu, room=room, sender=sender, receiver=receiver,
                          gift=gift, timestamp=msg['time'])

    def _store_uenter(self, msg):

        user = self.get_or_create(User, name=msg['username'])
        room = self.get_or_create(Room, rid=int(msg['roomID']))

        self.create_danmu(UEnterDanmu, room=room, user=user, timestamp=msg['time'])

    def create_danmu(self, model, **kwargs):
        if model == TextDanmu:
            fd = self.fd_text
        elif model == GiftDanmu:
            fd = self.fd_gift
        elif model == U2UDanmu:
            fd = self.fd_u2u
        else:
            fd = self.fd_uenter

        fd.write('%s\n' % ('\t'.join([str(v) for v in kwargs.values()])))

    def get_or_create(self, model, defaults=None, **kwargs):

        def aux(key, func_load, func_save):
            _id = func_load(kwargs[key])

            if _id is not None:
                return _id
            else:
                return func_save(kwargs[key])

        if model == User:
            result = self.redis.get_user(kwargs['name'])
            if result is not None:
                id_, level = result
                new_level = defaults.get('level', 0) if defaults is not None else 0
                if new_level > level:  # update level
                    self.redis.update_user(id_, kwargs['name'], new_level)
                return id_
            else:
                return self.redis.save_user(kwargs['name'], defaults.get('level', 0) if defaults is not None else 0)
        elif model == Room:
            return aux('rid', self.redis.get_room, self.redis.save_room)
        else:
            if defaults['type'] == Gift.TYPE_NORMAL:
                return aux('name', self.redis.get_gift_normal, self.redis.save_gift_normal)
            elif defaults['type'] == Gift.TYPE_SUPER:
                return aux('name', self.redis.get_gift_super, self.redis.save_gift_super)
            else:
                return aux('name', self.redis.get_gift_u2u, self.redis.save_gift_u2u)
