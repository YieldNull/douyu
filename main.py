import sys
import logging
from danmu.douyu.danmu import schedule


def excepthook(tp, value, traceback):
    logging.exception("Uncaught exception:", exc_info=(tp, value, traceback))


sys.excepthook = excepthook

if __name__ == '__main__':
    schedule(pcount=int(sys.argv[1]), pages=int(sys.argv[2]))
