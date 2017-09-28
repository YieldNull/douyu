import time
import asyncio
import logging
import sys
from multiprocessing import Process, cpu_count
from douyu.protocol import Protocol
from douyu.spider.persistence import Storage
from douyu.spider import indexing


class Counter(object):
    def __init__(self, logger, logging_period):
        self.counter_all = 0
        self.counter_period = 0
        self.counter_time = time.time()

        self.logger = logger
        self.logging_period = logging_period * 60

    def incr(self):
        self.counter_all += 1
        self.counter_period += 1

        now = time.time()

        if now - self.counter_time > self.logging_period:
            self.counter_time = now
            self.logger.info('Received {:d} items. {:d} items/min'.format(
                self.counter_all, int(self.counter_period * 60 / self.logging_period)))
            self.counter_period = 0


class Room(object):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('%(asctime)s [%(name)s] %(levelname)s pid-%(process)d room:%(room)8s: %(message)s'))

    logger = logging.getLogger('ROOM')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    def __init__(self, rid: str):
        self.server_address = 'openbarrage.douyutv.com'
        self.server_port = 8601

        self.msg_type_user = 689
        self.msg_type_server = 690

        self.protocol = Protocol()

        self.reader = None
        self.writer = None

        self.rid = rid

        logger = logging.LoggerAdapter(self.logger, {'room': self.rid})

        self.logger = logger
        self.storage = Storage()
        self.counter = Counter(self.logger, 2)

    async def listen(self):
        self.reader, self.writer = await asyncio.open_connection(self.server_address, self.server_port)
        await self.send('type@=loginreq/roomid@={:s}/'.format(self.rid))

        await self.recv()

        await self.send('type@=joingroup/rid@={:s}/gid@=-9999/'.format(self.rid))
        await self.recv()

        self.logger.info('logged in')

        heartbeat = time.time()
        while True:
            if not await self.recv():
                break

            now = time.time()
            if now - heartbeat > 45:
                self.logger.debug('heartbeat')
                heartbeat = now
                await self.send('type@=mrkl/')

    async def logout(self):
        await self.send('type@=logout/')

    async def send(self, payload):
        self.writer.write(self.protocol.pack(Protocol.TYPE_CLIENT, payload))
        await self.writer.drain()

    async def recv(self):
        try:
            header = await self.reader.readexactly(self.protocol.header_size)
        except asyncio.streams.IncompleteReadError as e:
            self.logger.warning('Quit room for ' + repr(e))
            return False

        msg_type, payload_length = self.protocol.unpack_header(header)

        assert msg_type == Protocol.TYPE_SERVER

        payload = await self.reader.readexactly(payload_length)

        try:
            msg = self.protocol.unpack_payload(payload, payload_length)
        except:
            return False

        self.logger.debug(str(msg))

        msg['rid'] = self.rid
        msg['timestamp'] = time.time()

        await self.storage.store(msg)

        self.counter.incr()

        if msg['type'] == 'rss' and msg.get('ss', -1) == 0:
            return False
        return True


def listen_rooms(rids):
    assert len(rids) > 0

    loop = asyncio.get_event_loop()

    tasks = [Room(rid).listen() for rid in rids]

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def listen_using_multi_process(pcount=cpu_count()):
    rids = indexing.metadata()
    n = int(len(rids) / pcount)
    available = len(rids) - n * pcount

    index = 0
    chunks = []
    for length in map(lambda x: n + 1 if x < available else n, range(0, pcount)):
        chunks.append(rids[index:index + length])
        index += length

    processes = [Process(target=listen_rooms, args=(rids,)) for rids in chunks]

    [p.start() for p in processes]
    [p.join() for p in processes]
