import asyncio

from danmu.msg import RegexParser
from etl.msg import parse_raw
from etl.msg.storage import AsyncRDSStorage, RDSStorage
from etl.msg.models import db
from peewee_async import Manager


async def parse_file(file, storage):
    parser = RegexParser()

    with open(file, 'r', encoding='utf-8', buffering=1024 * 1024 * 10) as f:
        for line in f:
            try:
                print(line)
                msg = parse_raw(parser, line)
                if msg:
                    await storage.store(msg)
                    # storage.store(msg)
            except PermissionError as e:
                print(repr(e))


if __name__ == '__main__':
    import sys
    import time

    loop = asyncio.get_event_loop()

    manager = Manager(db, loop=loop)

    start = time.time()
    loop.run_until_complete(parse_file(sys.argv[1], AsyncRDSStorage(manager)))
    # parse_file(sys.argv[1], RDSStorage())
    end = time.time()

    print(end - start)

    # 365 async
    # 535 sync
    # 270 async delete badge
    # 160 async delete badge using redis
