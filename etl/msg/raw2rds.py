import os
import sys
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from common.parser import RegexParser, parse_raw
from etl.msg.storage import TextStorage


def parse_file(path, repo):
    parser = RegexParser()
    storage = TextStorage(os.path.join(repo, os.path.splitext(os.path.basename(path))[0]))

    with open(path, 'r', encoding='utf-8', buffering=1024 * 128) as f:
        for line in f:
            msg = parse_raw(parser, line)
            if msg and msg.get('type', 'other') != 'other':
                storage.store(msg)
    storage.close()


def parse_files(pths, repo, workers):
    thread_executor = ThreadPoolExecutor(max_workers=workers)
    for path in pths:
        thread_executor.submit(parse_file, path, repo)
    thread_executor.shutdown(wait=True)


if __name__ == '__main__':
    dir_ = sys.argv[1]
    repository = sys.argv[2]

    process_max_workers = sys.argv[3] if len(sys.argv) > 3 else multiprocessing.cpu_count()
    thread_max_workers = sys.argv[4] if len(sys.argv) > 4 else 20

    start = time.time()
    executor = ProcessPoolExecutor(max_workers=process_max_workers)

    paths = [os.path.join(dir_, name) for name in os.listdir(dir_)]


    def chunks(l, n):
        c = [[] for _ in range(n)]
        index = 0

        for item in l:
            c[index].append(item)
            index += 1
            if index >= n:
                index = 0
        return c


    for split in chunks(paths, process_max_workers):
        executor.submit(parse_files, split, repository, thread_max_workers)
    executor.shutdown(wait=True)
    end = time.time()

    print(end - start)
