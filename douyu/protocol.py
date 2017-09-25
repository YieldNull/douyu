import asyncio
import struct
import time
import os
from grako.exceptions import FailedParse
from douyu.msg_parser import DanmuParser, DanmuSemantics
from douyu.persistence import Storage


class MsgSemantics(DanmuSemantics):
    def __init__(self, user_input_keys=None):
        if user_input_keys is None:
            user_input_keys = ['txt']
        self.user_input_keys = user_input_keys
        self.parser = DanmuParser()

    def rec_parse(self, data):
        try:
            data = self.parser.parse(text=data, semantics=MsgSemantics())
        except FailedParse:
            if data.find('@A') > 0:
                data = self.rec_parse(data.replace('@A', '@').replace('@S', '/'))
        return data

    def start(self, ast):
        return ast

    def array(self, ast):
        if isinstance(ast[0], tuple):
            return dict(ast)
        else:
            return ast

    def item(self, ast):
        if not isinstance(ast[0], tuple):
            return self.rec_parse(ast[0])
        else:
            return ast[0]

    def pair(self, ast):
        key = ast[0]
        data = ast[2]

        if key not in self.user_input_keys:
            data = self.rec_parse(data)

        return key, data

    def data(self, ast):
        return ''.join(ast)

    def key(self, ast):
        return ''.join(ast)

    def char(self, ast):
        if ast == '@S':
            return '/'
        elif ast == '@A':
            return '@'
        else:
            return ast


class MsgParser(DanmuParser):
    def parse(self, text, rule_name='start', filename=None,
              buffer_class=None, semantics=MsgSemantics(), trace=False,
              whitespace=None, **kwargs):
        return super().parse(text, rule_name, filename, buffer_class, semantics, trace, whitespace, **kwargs)


class Room(object):
    def __init__(self, rid):
        self.server_address = 'openbarrage.douyutv.com'
        self.server_port = 8601

        self.header_pseudo_size = 8
        self.header_size = 12
        self.header_fmt = '<IIHBB'

        self.msg_type_user = 689
        self.msg_type_server = 690

        self.msg_parser = MsgParser()

        self.reader = None
        self.writer = None

        self.rid = rid

        self.storage = Storage()

    async def listen(self, loop):
        self.reader, self.writer = await asyncio.open_connection(self.server_address, self.server_port, loop=loop)

        await self.send('type@=loginreq/roomid@={:d}/'.format(self.rid))
        await self.recv()

        await self.send('type@=joingroup/rid@={:d}/gid@=-9999/'.format(self.rid))
        await self.recv()

        heartbeat = time.time()
        while True:
            await self.recv()

            now = time.time()
            if now - heartbeat > 45:
                heartbeat = now
                await self.send('type@=mrkl/')

    async def logout(self):
        await self.send('type@=logout/')

    async def send(self, payload):
        print('PID:{:d} ROOM:{:d} {:s}'.format(os.getpid(), self.rid, payload))

        payload_len = len(payload)
        size = self.header_pseudo_size + payload_len + 1

        data = struct.pack(self.header_fmt + '{:d}sB'.format(payload_len),
                           size, size,
                           self.msg_type_user, 0, 0,
                           payload.encode('utf-8'), 0)
        self.writer.write(data)
        await self.writer.drain()

    async def recv(self):

        response = await self.reader.readexactly(self.header_size)

        length, _, msg_type, _, _ = struct.unpack(self.header_fmt, response)

        assert msg_type == self.msg_type_server
        length = length - self.header_pseudo_size
        response = await self.reader.readexactly(length)

        payload, zero = struct.unpack('{:d}sB'.format(length - 1), response)
        payload = payload.decode('utf-8')

        msg = self.msg_parser.parse(payload)

        await self.storage.store(msg)

        return msg


def listen_rooms(rids):
    loop = asyncio.get_event_loop()

    tasks = [loop.create_task(Room(rid).listen(loop)) for rid in rids]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    from multiprocessing import Process, cpu_count

    rids = [
        2250040,
        2124270,
        70231,
        226855,
        1811143,
        3125893,
        65962,
        70231,
        921393,
        274874,
        2014101,
        3250449,
        1432054,
        2670580,
        829815,
        2152273
    ]

    n = int(len(rids) / cpu_count() / 2)
    chunks = [rids[i:i + n] for i in range(0, len(rids), n)]

    processes = [Process(target=listen_rooms, args=(rids,)) for rids in chunks]
    [p.start() for p in processes]
    [p.join() for p in processes]
