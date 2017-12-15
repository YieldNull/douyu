import time
import asyncio
import os
import threading
from functools import reduce
from multiprocessing import Process, Pipe, Queue, cpu_count
from danmu import settings, get_logger, persistence
from danmu.spider import indexing
from danmu.msg import Protocol
from danmu.persistence import Storage
from danmu.redis import RedisClient

"""
https://yieldnull.com/blog/f9a25fe711158017f5bf82b0ab41f3dcd114bc7a/
"""


class Counter(object):
    def __init__(self, _logger, logging_period):
        self.counter_all = 0
        self.counter_period = 0
        self.counter_time = time.time()

        self.logger = _logger
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
    server_address = settings.SERVER_ADDRESS
    server_port = settings.SERVER_PORT
    msg_type_user = 689
    msg_type_server = 690

    def __init__(self, pname, rid: str, storage: Storage):

        self.protocol = Protocol()

        self.reader = None
        self.writer = None

        self.rid = rid
        self.is_canceled = False

        _logger = get_logger(pname, '%(asctime)s [%(name)s] %(levelname)s room:%(room)8s: %(message)s')
        _logger = logging.LoggerAdapter(_logger, {'room': self.rid})
        self.logger = _logger

        self.storage = storage
        self.counter = Counter(self.logger, settings.COUNTER_PERIOD)

    async def listen(self, loop):
        self.reader, self.writer = await asyncio.open_connection(self.server_address, self.server_port, loop=loop)
        await self.send('type@=loginreq/roomid@={:s}/'.format(self.rid))

        await self.recv()

        await self.send('type@=joingroup/rid@={:s}/gid@=-9999/'.format(self.rid))
        await self.recv()

        self.logger.info('logged in')

        heartbeat = time.time()
        while True:
            if self.is_canceled:
                return
            try:
                await self.recv()
            except UnicodeDecodeError as e:
                self.logger.warning(repr(e))

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
        header = await self.reader.readexactly(self.protocol.header_size)

        msg_type, payload_length = self.protocol.unpack_header(header)

        assert msg_type == Protocol.TYPE_SERVER

        payload = await self.reader.readexactly(payload_length)

        msg = {'rid': self.rid, 'timestamp': time.time(), 'payload': payload}

        if settings.STORAGE_ASYNC:
            await self.storage.store(msg)
        else:
            self.storage.store(msg)

        self.counter.incr()


class Scheduler(object):
    def __init__(self):
        self.pipes = {}
        self.tasks = {}

        self.queue = Queue()
        self.workers = {}  # pid:wid

        self.logger = get_logger('Scheduler', format_str='%(asctime)s [%(name)s] %(levelname)s : %(message)s')

        self.redis = RedisClient()

    def process_main(self, wid, pipe: Pipe, queue: Queue):
        tasks = {}
        storage = getattr(persistence, settings.STORAGE_CLASS)('Storage-{:d}'.format(wid))

        def listen_pipe(looop):
            while True:
                is_pending, rid = pipe.recv()
                if is_pending:
                    room = Room('Worker-{:d}'.format(wid), rid, storage)
                    tasks[rid] = room
                    asyncio.run_coroutine_threadsafe(self.process_task(queue, room, looop), looop)

                    room.logger.info('Received task')
                else:
                    tasks[rid].logger.info('Canceling task')
                    tasks[rid].is_canceled = True
                    tasks[rid].writer.close()
                    tasks.pop(rid)

        loop = asyncio.get_event_loop()

        threading.Thread(target=listen_pipe, args=(loop,)).start()

        loop.run_forever()

    @staticmethod
    async def process_task(queue: Queue, room, loop):
        normal = True
        try:
            await room.listen(loop)
            room.logger.info('Task finished')
        except Exception as e:
            room.logger.warning('Quit room for ' + ("Canceled" if room.is_canceled else repr(e)))
            normal = room.is_canceled or False
        finally:
            try:
                room.writer.close()
            except Exception as e:
                room.logger.warning('Error when closing writer. ' + repr(e))
            queue.put((os.getpid(), room.rid, normal))

    def listen_queue(self):
        while True:
            pid, rid, normal = self.queue.get()
            self.logger.info('Task finished(normally:{:}). Worker-{:d} rid:{:s}.'
                             .format(str(normal), self.workers[pid], rid))

            pp = self.tasks[pid]
            pp['running'].remove(rid)
            # pp['finished'].add(rid)

            if not normal:
                self.logger.info('Reschedule failed task rid:{:s}'.format(rid))
                self.spawn_tasks([rid])

    def listen_redis(self):
        for item in self.redis.listen_temporary_rid():
            if item['type'] == 'message':
                rid = item['data']
                self.logger.info('Got task from redis. room:{:s}'.format(rid))
                self.spawn_tasks([rid])

    def spawn_tasks(self, targets):
        pending = set(targets) - reduce(lambda acc, x: acc | x[1]['running'], self.tasks.items(), set())

        for rid in pending:
            pid, _ = min(self.tasks.items(), key=lambda x: len(x[1]['running']))

            self.tasks[pid]['running'].add(rid)

            self.logger.info('Schedule task:{:s} to Worker-{:d}'.format(rid, self.workers[pid]))

            self.pipes[pid].send((True, rid))

    def schedule(self, pcount=cpu_count(), pages=1):
        threading.Thread(target=self.listen_queue, args=()).start()
        threading.Thread(target=self.listen_redis, args=()).start()

        for wid in range(pcount):
            pipe, child_pipe = Pipe()
            p = Process(target=self.process_main, args=(wid, child_pipe, self.queue))
            p.start()

            self.pipes[p.pid] = pipe
            self.tasks[p.pid] = {
                'running': set(),
                # 'finished': set()
            }
            self.workers[p.pid] = wid

        while True:
            self.logger.info('Fetching latest rooms...')

            targets = indexing.target_rids(pages)

            self.spawn_tasks(targets)

            rooms = targets

            for pid, v in self.tasks.items():
                running = v['running']
                for rid in running - rooms:
                    self.logger.info('Canceling task:{:s} in Worker-{:d}'.format(rid, self.workers[pid]))

                    self.pipes[pid].send((False, rid))

                # logger.info('pid:{:d} running:{:s} finished:{:s}'.format(pid, str(v['running']), str(v['finished'])))
                self.logger.info('Worker-{:d} running:{:s}'.format(self.workers[pid], str(v['running'])))

            time.sleep(settings.INDEXING_PERIOD * 60)


if __name__ == '__main__':
    import sys
    import logging


    def excepthook(tp, value, traceback):
        logging.exception("Uncaught exception:", exc_info=(tp, value, traceback))


    sys.excepthook = excepthook

    s = Scheduler()
    s.schedule(pcount=int(sys.argv[1]), pages=int(sys.argv[2]))
