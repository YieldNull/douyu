import time
import asyncio
import os
import logging
import sys
from douyu.protocol import Protocol
from douyu.spider.persistence import Storage


class Room(object):
    def __init__(self, rid):
        self.server_address = 'openbarrage.douyutv.com'
        self.server_port = 8601

        self.msg_type_user = 689
        self.msg_type_server = 690

        self.protocol = Protocol()

        self.reader = None
        self.writer = None

        self.rid = rid

        self.storage = Storage()

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(name)s] %(levelname)s pid-%(process)d room:%(room)8d: %(message)s'))

        logger = logging.getLogger('ROOM')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        class ContextFilter(logging.Filter):
            def __init__(self, rid, name=''):
                super().__init__(name)
                self.rid = rid

            def filter(self, record):
                record.room = self.rid
                return True

        logger.addFilter(ContextFilter(self.rid))

        self.logger = logger

    async def listen(self, loop):
        self.reader, self.writer = await asyncio.open_connection(self.server_address, self.server_port, loop=loop)

        await self.send('type@=loginreq/roomid@={:d}/'.format(self.rid))
        await self.recv()

        await self.send('type@=joingroup/rid@={:d}/gid@=-9999/'.format(self.rid))
        await self.recv()

        heartbeat = time.time()
        while True:
            if not await self.recv():
                break

            now = time.time()
            if now - heartbeat > 45:
                heartbeat = now
                await self.send('type@=mrkl/')

    async def logout(self):
        await self.send('type@=logout/')

    async def send(self, payload):
        self.logger.info(payload)

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

        payload = await  self.reader.readexactly(payload_length)
        msg = self.protocol.unpack_payload(payload, payload_length)

        self.logger.info(str(msg))

        await self.storage.store(msg)

        return True


def listen_rooms(rids):
    loop = asyncio.get_event_loop()

    tasks = [loop.create_task(Room(rid).listen(loop)) for rid in rids]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def listen_using_multi_process(rids):
    from multiprocessing import Process, cpu_count

    n = int(len(rids) / cpu_count())
    available = len(rids) - n * cpu_count()

    index = 0
    chunks = []
    for length in map(lambda x: n + 1 if x < available else n, range(0, cpu_count())):
        chunks.append(rids[index:index + length])
        index += length

    processes = [Process(target=listen_rooms, args=(rids,)) for rids in chunks]
    [p.start() for p in processes]
    [p.join() for p in processes]
