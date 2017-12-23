from datetime import datetime

from etl.msg.models import *


class RDSStorage(object):
    def store(self, msg):
        _type = msg['type']

        msg['time'] = datetime.fromtimestamp(float(msg['time']))

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

    def _store_text(self, msg):
        user, _ = User.get_or_create(name=msg['username'])

        room, _ = Room.get_or_create(rid=int(msg['roomID']))

        broom, _ = Room.get_or_create(rid=int(msg['broomID']))

        if msg['badgename'] is None:
            badge_id = None
        else:
            badge, _ = Badge.get_or_create(room=broom.id, user=user.id, name=msg['badgename'])
            badge_id = badge.id

        TextDanmu.create(room=room.id, user=user.id, badge=badge_id, timestamp=msg['time'])

    def _store_normal_gift(self, msg):
        user, _ = User.get_or_create(name=msg['username'])

        room, _ = Room.get_or_create(rid=int(msg['roomID']))

        broom, _ = Room.get_or_create(rid=int(msg['broomID']))

        if msg['badgename'] is None:
            badge_id = None
        else:
            badge, _ = Badge.get_or_create(room=broom.id, user=user.id, name=msg['badgename'])
            badge_id = badge.id

        gift, _ = Gift.get_or_create(name=msg['giftID'], defaults={'type': Gift.TYPE_NORMAL})

        GiftDanmu.create(room=room.id, user=user.id, badge=badge_id, gift=gift.id, timestamp=msg['time'])

    def _store_super_gift(self, msg):
        if msg['roomID'] != msg['droomID']:  # dup filter
            return

        user, _ = User.get_or_create(name=msg['username'])

        room, _ = Room.get_or_create(rid=int(msg['roomID']))

        gift, _ = Gift.get_or_create(name=msg['giftname'], defaults={'type': Gift.TYPE_SUPER})

        GiftDanmu.create(room=room.id, user=user.id, gift=gift.id, timestamp=msg['time'])

    def _store_u2u(self, msg):
        room, _ = Room.get_or_create(rid=int(msg['roomID']))
        gift, _ = Gift.get_or_create(name=msg['pnm'], defaults={'type': Gift.TYPE_U2U})
        sender, _ = User.get_or_create(name=msg['username'])
        receiver, _ = User.get_or_create(name=msg['rusername'])

        U2UDanmu.create(room=room.id, sender=sender.id, receiver=receiver.id, gift=gift.id,
                        timestamp=msg['time'])

    def _store_uenter(self, msg):
        user, _ = User.get_or_create(name=msg['username'])
        room, _ = Room.get_or_create(rid=int(msg['roomID']))

        UEnterDanmu.create(room=room.id, user=user.id, timestamp=msg['time'])
