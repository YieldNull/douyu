import peewee
import logging
from asyncio import ensure_future, gather
from datetime import datetime
from etl.msg.models import *
from etl.msg.cache import RedisClient


class AsyncRDSStorage(object):
    def __init__(self, manager):
        self.manager = manager
        self.logger = logging.getLogger('AsyncRDSStorage')
        self.redis = RedisClient()

    async def connect(self, loop):
        await self.redis.connect(loop)

    async def store(self, msg):
        try:
            _type = msg['type']

            msg['time'] = datetime.fromtimestamp(float(msg['time']))

            if _type == 'chatmsg':
                await self._store_text(msg)
            elif _type == 'dgb':
                await self._store_normal_gift(msg)
            elif _type == 'spbc':
                await self._store_super_gift(msg)
            elif _type == 'gpbc':
                await self._store_u2u(msg)
            elif _type == 'uenter':
                await self._store_uenter(msg)
        except Exception as e:
            self.logger.warning('%s:%s' % (repr(e), repr(msg)))

    async def _store_text(self, msg):
        user_task = ensure_future(self.get_or_create(User, name=msg['username'], ))

        room_task = ensure_future(self.get_or_create(Room, rid=int(msg['roomID'])))

        broom_task = ensure_future(self.get_or_create(Room, rid=int(msg['broomID'])))

        (user, _), (room, _), (broom, _) = await gather(user_task, room_task, broom_task)

        await self.manager.create(TextDanmu, room=room, user=user, timestamp=msg['time'])

    async def _store_normal_gift(self, msg):
        user_task = ensure_future(self.get_or_create(User, name=msg['username'], ))

        room_task = ensure_future(self.get_or_create(Room, rid=int(msg['roomID'])))

        broom_task = ensure_future(self.get_or_create(Room, rid=int(msg['broomID'])))

        gift_task = ensure_future(
            self.get_or_create(Gift, name=msg['giftID'], defaults={'type': Gift.TYPE_NORMAL}))

        (user, _), (room, _), (broom, _), (gift, _) = await gather(user_task, room_task, broom_task, gift_task)

        await self.manager.create(GiftDanmu, room=room, user=user, gift=gift, timestamp=msg['time'])

    async def _store_super_gift(self, msg):
        if msg['roomID'] != msg['droomID']:  # dup filter
            return

        user_task = ensure_future(self.get_or_create(User, name=msg['username']))

        room_task = ensure_future(self.get_or_create(Room, rid=int(msg['roomID'])))

        gift_task = ensure_future(
            self.get_or_create(Gift, name=msg['giftname'], defaults={'type': Gift.TYPE_SUPER}))

        (user, _), (room, _), (gift, _) = await gather(user_task, room_task, gift_task)

        await self.manager.create(GiftDanmu, room=room, user=user, gift=gift, timestamp=msg['time'])

    async def _store_u2u(self, msg):
        room_task = ensure_future(self.get_or_create(Room, rid=int(msg['roomID'])))
        gift_task = ensure_future(self.get_or_create(Gift, name=msg['pnm'], defaults={'type': Gift.TYPE_U2U}))
        sender_task = ensure_future(self.get_or_create(User, name=msg['username']))
        receiver_task = ensure_future(self.get_or_create(User, name=msg['rusername']))

        (room, _), (gift, _), (sender, _), (receiver, _) = await gather(room_task, gift_task, sender_task,
                                                                        receiver_task)

        await self.manager.create(U2UDanmu, room=room, sender=sender, receiver=receiver,
                                  gift=gift, timestamp=msg['time'])

    async def _store_uenter(self, msg):

        user_task = ensure_future(self.get_or_create(User, name=msg['username']))
        room_task = ensure_future(self.get_or_create(Room, rid=int(msg['roomID'])))

        (user, _), (room, _) = await gather(user_task, room_task)

        await self.manager.create(UEnterDanmu, room=room, user=user, timestamp=msg['time'])

    async def get_or_create(self, model, defaults=None, **kwargs):

        async def aux(key, func_load, func_save):
            id_ = await func_load(kwargs[key])
            if id_ is not None:
                return int(id_), False
            else:
                data = defaults or {}
                data.update({k: v for k, v in kwargs.items()
                             if not '__' in k})
                try:
                    row = (await self.manager.create(model, **data))
                    id_ = row.id
                    await func_save(id_, kwargs[key])
                    return id_, True
                except peewee.IntegrityError:
                    return (await self.manager.get(model, **kwargs)), False

        if model == Room:
            return await aux('rid', self.redis.get_room, self.redis.save_room)
        elif model == User:
            return await aux('name', self.redis.get_user, self.redis.save_user)
        else:
            if defaults['type'] == Gift.TYPE_NORMAL:
                return await aux('name', self.redis.get_gift_normal, self.redis.save_gift_normal)
            elif defaults['type'] == Gift.TYPE_SUPER:
                return await aux('name', self.redis.get_gift_super, self.redis.save_gift_super)
            else:
                return await aux('name', self.redis.get_gift_u2u, self.redis.save_gift_u2u)
