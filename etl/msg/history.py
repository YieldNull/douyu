import asyncio
from concurrent.futures import ProcessPoolExecutor
from danmu.msg import RegexParser
from etl.msg import parse_raw
from etl.msg.storage import AsyncRDSStorage
from etl.msg.models import *
from peewee_async import Manager


def parse_file(path):
    async def parse():
        manager = Manager(db, loop=loop)
        parser = RegexParser()
        storage = AsyncRDSStorage(manager)

        await storage.connect(loop)

        with open(path, 'r', encoding='utf-8', buffering=1024 * 32) as f:
            counter = 0
            tasks = []

            for line in f:
                msg = parse_raw(parser, line)
                if msg:
                    counter += 1
                    tasks.append(asyncio.ensure_future(storage.store(msg)))
                if counter == 10:
                    await asyncio.gather(*tasks)
                    counter = 0
                    tasks = []

    loop = asyncio.get_event_loop()

    loop.run_until_complete(parse())


if __name__ == '__main__':
    db.create_tables([Room, User, Gift, TextDanmu, GiftDanmu, UEnterDanmu, U2UDanmu], safe=True)

    import os
    import sys
    import time

    max_workers = sys.argv[2] if len(sys.argv) > 2 else 10
    start = time.time()

    executor = ProcessPoolExecutor(max_workers=10)

    dir_ = sys.argv[1]

    for name in os.listdir(dir_):
        executor.submit(parse_file, os.path.join(dir_, name))
    executor.shutdown(wait=True)
    end = time.time()

    print(end - start)
