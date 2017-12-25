import redis
import aioredis


class RedisClient(object):

    def __init__(self):
        # self.client = redis.StrictRedis(decode_responses=True)
        self.client = None

    async def connect(self, loop):
        self.client = await aioredis.create_redis_pool(
            'redis://localhost',
            minsize=10, maxsize=50,
            encoding='utf-8',
            loop=loop)

    async def save_room(self, id_, rid):
        await self.client.set('r{}'.format(rid), id_)

    async def get_room(self, rid):
        return await self.client.get('r{}'.format(rid))

    async def save_user(self, id_, name):
        await self.client.set('u{}'.format(name), id_)

    async def get_user(self, name):
        return await self.client.get('u{}'.format(name))

    async def save_gift_normal(self, id_, name):
        await self.client.set('gn{}'.format(name), id_)

    async def get_gift_normal(self, name):
        return await self.client.get('gn{}'.format(name))

    async def save_gift_super(self, id_, name):
        await self.client.set('gs{}'.format(name), id_)

    async def get_gift_super(self, name):
        return await self.client.get('gs{}'.format(name))

    async def save_gift_u2u(self, id_, name):
        await self.client.set('gu{}'.format(name), id_)

    async def get_gift_u2u(self, name):
        return await self.client.get('gu{}'.format(name))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()


    async def foo():
        redis = RedisClient()
        await redis.connect(loop)
        u = await redis.get_user('~敬酒不吃~')
        print(u)


    loop.run_until_complete(foo())
