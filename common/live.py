import redis


class RedisClient(object):
    ACC_DANMU = 'danmu:live:danmu'
    ACC_USER = 'danmu:live:user'
    ACC_GIFT = 'danmu:live:gift'
    ACC_INCOME = 'danmu:live:income'

    def __init__(self):
        self.client = redis.StrictRedis(decode_responses=True)

    def add_user(self, room, user):
        self.client.sadd('{:s}:{:s}'.format(self.ACC_USER, str(room)), user)

    def add_gift(self, room):
        self.client.incr('{:s}:{:s}'.format(self.ACC_GIFT, str(room)))

    def add_danmu(self, room):
        self.client.incr('{:s}:{:s}'.format(self.ACC_DANMU, str(room)))

    def add_income(self, room, income):
        self.client.incrby('{:s}:{:s}'.format(self.ACC_INCOME, str(room)), income)

    def get_user(self, room):
        size = self.client.scard('{:s}:{:s}'.format(self.ACC_USER, str(room)))
        return int(size)

    def get_gift(self, room):
        count = self.client.get('{:s}:{:s}'.format(self.ACC_GIFT, str(room)))
        return int(0 if count is None else count)

    def get_danmu(self, room):
        count = self.client.get('{:s}:{:s}'.format(self.ACC_DANMU, str(room)))
        return int(0 if count is None else count)

    def get_income(self, room):
        amount = self.client.get('{:s}:{:s}'.format(self.ACC_INCOME, str(room)))
        return int(0 if amount is None else amount)

    def clear_user(self, room):
        key = '{:s}:{:s}'.format(self.ACC_USER, str(room))
        size = self.client.scard(key)

        self.client.delete(key)
        return int(size)

    def clear_danmu(self, room):
        key = '{:s}:{:s}'.format(self.ACC_DANMU, str(room))

        count = self.client.get(key)

        self.client.delete(key)
        return int(0 if count is None else count)

    def clear_gift(self, room):
        key = '{:s}:{:s}'.format(self.ACC_GIFT, str(room))

        count = self.client.get(key)

        self.client.delete(key)
        return int(0 if count is None else count)

    def clear_income(self, room):
        key = '{:s}:{:s}'.format(self.ACC_INCOME, str(room))

        amount = self.client.get(key)

        self.client.delete(key)
        return int(0 if amount is None else amount)
