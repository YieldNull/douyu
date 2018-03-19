import pika
import json
import logging
from common.parser import RegexParser
from pika.exceptions import ConnectionClosed


class RawProducer(object):
    EXCHANGE = 'danmu.raw'
    QUEUE_NAME = 'danmu.queue.raw'
    ROUTE_PARSER = 'parser'

    def __init__(self, logger: logging.Logger, host='localhost', port=5672):
        self.host = host
        self.port = port
        self.logger = logger
        self.conn = None
        self.channel = None

        self.connect()

    def connect(self):
        try:
            self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
            self.channel = self.conn.channel()

            self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')
            self.channel.queue_declare(queue=self.QUEUE_NAME)

            self.channel.queue_bind(exchange=self.EXCHANGE,
                                    queue=self.QUEUE_NAME,
                                    routing_key=self.ROUTE_PARSER)
        except ConnectionClosed:
            self.channel = None

    def send(self, msg):
        try:
            if self.channel is not None:
                self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTE_PARSER, body=msg)
        except Exception as e:
            self.logger.warning('Error in publish RawProducer msg. Reconnecting... %s' % (repr(e)))
            self.close()
            self.connect()

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                self.logger.warning('Error in closing RawProducer connection %s' % (repr(e)))


class EmotProducer(object):
    EXCHANGE = 'danmu.emot'
    QUEUE_NAME = 'danmu.queue.emot'
    ROUTE_PARSER = 'parser'

    def __init__(self, logger: logging.Logger, host='localhost', port=5672):
        self.host = host
        self.port = port
        self.logger = logger
        self.conn = None
        self.channel = None

        self.connect()

    def connect(self):
        try:
            self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
            self.channel = self.conn.channel()

            self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')
            self.channel.queue_declare(queue=self.QUEUE_NAME)

            self.channel.queue_bind(exchange=self.EXCHANGE,
                                    queue=self.QUEUE_NAME,
                                    routing_key=self.ROUTE_PARSER)
        except ConnectionClosed:
            self.channel = None

    def send(self, msg):
        try:
            if self.channel is not None:
                self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTE_PARSER, body=msg)
        except Exception as e:
            self.logger.warning('Error in publish EmotProducer msg. Reconnecting... %s' % (repr(e)))
            self.close()
            self.connect()

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                self.logger.warning('Error in closing EmotProducer connection %s' % (repr(e)))


class StreamProducer(object):
    EXCHANGE = 'amq.topic'  # use build-in exchange for Web STOMP

    ROUTE_STREAM = 'stream.room.'

    def __init__(self, logger: logging.Logger, host='localhost', port=5672):
        self.host = host
        self.port = port
        self.logger = logger
        self.conn = None
        self.channel = None

        self.connect()

    def connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.conn.channel()

    def send(self, route, msg):
        try:
            self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)
        except Exception as e:
            self.logger.warning('Error in publish StreamProducer msg. Reconnecting... %s' % (repr(e)))
            self.close()
            self.connect()

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                self.logger.warning('Error in closing StreamProducer connection %s' % (repr(e)))


class ParserConsumer(object):

    def __init__(self, logger: logging.Logger, msg_handler=None, host='localhost', port=5672):

        self.host = host
        self.port = port
        self.logger = logger
        self.conn = None
        self.channel = None

        self.parser = RegexParser()
        self.msg_handler = msg_handler
        self.closed = False

        self.connect()

    def connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=RawProducer.EXCHANGE, exchange_type='direct')

        self.channel.queue_declare(queue=RawProducer.QUEUE_NAME)

        self.channel.queue_bind(exchange=RawProducer.EXCHANGE,
                                queue=RawProducer.QUEUE_NAME,
                                routing_key=RawProducer.ROUTE_PARSER)

        self.channel.basic_consume(self._callback, queue=RawProducer.QUEUE_NAME, no_ack=True)

    def start(self):
        while True:
            try:
                self.channel.start_consuming()
            except Exception as e:
                if not self.closed:
                    self.logger.warning('Error in ParserConsumer consuming. Reconnecting %s' % (repr(e)))
                    self.close(False)
                    self.connect()

    def close(self, force=True):
        if force:
            self.closed = True

        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                self.logger.warning('Error in closing ParserConsumer connection %s' % (repr(e)))

    def _callback(self, ch, method, properties, body):
        doc = json.loads(body.decode('utf-8'))
        try:
            msg = self.parser.parse(doc['raw'])

            if msg['type'] != 'other':
                msg.update({'roomID': doc['rid'], 'time': doc['ts']})

                if self.msg_handler is not None:
                    self.msg_handler(msg)
        except Exception as e:
            self.logger.warning('Error in ParserConsumer %s' % (repr(e)))
