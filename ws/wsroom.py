from mq import MsgConsumer
import sys


def handler(doc):
    print(doc['rid'], doc)


if __name__ == '__main__':
    cons = MsgConsumer(sys.argv[1], handler)
    cons.start()
