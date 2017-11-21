import time
import asyncio
import logging
import os
import threading
from functools import reduce
from multiprocessing import Process, Pipe, Queue, cpu_count
from danmu import settings, get_logger
from danmu.douyu import indexing, persistence
from danmu.douyu.msg.protocol import Protocol
from danmu.douyu.persistence import Storage

logger = get_logger('Scheduler')


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
    def __init__(self, pname, rid: str, storage: Storage):
        self.server_address = settings.SERVER_ADDRESS
        self.server_port = settings.SERVER_PORT

        self.msg_type_user = 689
        self.msg_type_server = 690

        self.protocol = Protocol()

        self.reader = None
        self.writer = None

        self.rid = rid
        self.is_canceled = False

        logger = get_logger(pname, '%(asctime)s [%(name)s] %(levelname)s room:%(room)8s: %(message)s')
        logger = logging.LoggerAdapter(logger, {'room': self.rid})
        self.logger = logger

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


async def process_task(queue: Queue, room, loop):
    try:
        await room.listen(loop)
        room.logger.info('Task finished')
    except Exception as e:
        room.logger.warning('Quit room for ' + repr(e))
    finally:
        try:
            room.writer.close()
        except Exception as e:
            room.logger.warning('Error when closing writer. ' + repr(e))
        queue.put((os.getpid(), room.rid))


def process_main(wid, pipe: Pipe, queue: Queue):
    tasks = {}
    storage = getattr(persistence, settings.STORAGE_CLASS)('Storage-{:d}'.format(wid))

    def listen_pipe(looop):
        while True:
            is_pending, rid = pipe.recv()
            if is_pending:
                room = Room('Worker-{:d}'.format(wid), rid, storage)
                tasks[rid] = room
                asyncio.run_coroutine_threadsafe(process_task(queue, room, looop), looop)

                room.logger.info('Received task: {:s}'.format(rid))
            else:
                tasks[rid].logger.info('Canceling task')
                tasks[rid].is_canceled = True
                tasks[rid].writer.close()

    loop = asyncio.get_event_loop()

    threading.Thread(target=listen_pipe, args=(loop,)).start()

    loop.run_forever()


def schedule(pcount=cpu_count(), pages=1):
    pipes = {}
    tasks = {}

    queue = Queue()
    for wid in range(pcount):
        pipe, child_pipe = Pipe()
        p = Process(target=process_main, args=(wid, child_pipe, queue))
        p.start()

        pipes[p.pid] = pipe
        tasks[p.pid] = {
            'running': set(),
            'finished': set()
        }

    def listen_queue():
        while True:
            _pid, _rid = queue.get()
            logger.info('Task finished. pid:{:d} rid:{:s}'.format(_pid, _rid))

            pp = tasks[_pid]
            pp['running'].remove(_rid)
            pp['finished'].add(_rid)

    threading.Thread(target=listen_queue, args=()).start()

    while True:
        logger.info('Fetching latest rooms...')

        targets = target_rooms(pages)

        pending = targets - reduce(lambda acc, x: acc | x[1]['running'], tasks.items(), set())

        for rid in pending:
            pid, _ = min(tasks.items(), key=lambda x: len(x[1]['running']))

            tasks[pid]['running'].add(rid)

            logger.info('Schedule task:{:s} to process:{:d}'.format(rid, pid))

            pipes[pid].send((True, rid))

        rooms = targets

        for pid, v in tasks.items():
            running = v['running']
            for rid in running - rooms:
                logger.info('Canceling task:{:s} in process:{:d}'.format(rid, pid))

                pipes[pid].send((False, rid))

            logger.info('pid:{:d} running:{:s} finished:{:s}'.format(pid, str(v['running']), str(v['finished'])))

        time.sleep(settings.INDEXING_PERIOD * 60)


def target_rooms(pages):
    target = set()

    for i in range(1, pages + 1):
        try:
            target.update(indexing.metadata(i))
        except Exception as e:
            logger.warning("Error in fetching:" + repr(e))

    logger.info("Targets Amount %d" % len(target))
    return target
