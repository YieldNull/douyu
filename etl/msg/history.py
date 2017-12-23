from danmu.msg import RegexParser
from etl.msg import parse_raw
from etl.msg.storage import RDSStorage


def parse_file(file):
    parser = RegexParser()
    storage = RDSStorage()

    with open(file, 'r', encoding='utf-8', buffering=1024 * 1024 * 10) as f:
        for line in f:
            try:
                msg = parse_raw(parser, line)
                if msg:
                    storage.store(msg)
            except Exception as e:
                print(repr(e))


if __name__ == '__main__':
    import sys

    parse_file(sys.argv[1])
