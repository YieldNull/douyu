import json
from common.mq import ParserConsumer, StreamProducer
from common.parser import ParserStorage
from live import get_logger


class Consumer(object):

    def __init__(self, storage):
        self.producer = StreamProducer(get_logger('StreamProducer'))
        self.storage = storage

    def on_msg(self, msg):
        self.storage.store(msg)
        self.producer.send(StreamProducer.ROUTE_STREAM + msg['roomID'], json.dumps(msg))


if __name__ == '__main__':
    import sys

    consumer = Consumer(ParserStorage(sys.argv[1]))

    p = ParserConsumer(get_logger('ParserConsumer'), msg_handler=consumer.on_msg)
    p.start()
