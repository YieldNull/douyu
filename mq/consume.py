import pika
import json
from danmu.msg import RegexParser
from danmu import settings
from mq.produce import RawProducer, StreamProducer


class ParserConsumer(object):
    def __init__(self, host='localhost', port=5672, msg_handler=None):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=RawProducer.EXCHANGE, exchange_type='direct')

        queue_name = 'danmu.queue.raw'
        self.channel.queue_declare(queue=queue_name)

        self.channel.queue_bind(exchange=RawProducer.EXCHANGE,
                                queue=queue_name,
                                routing_key=RawProducer.ROUTE_PARSER)

        self.channel.basic_consume(self.callback, queue=queue_name, no_ack=True)
        self.parser = RegexParser()

        self.producer = StreamProducer()

        self.msg_handler = msg_handler

    def callback(self, ch, method, properties, body):
        doc = json.loads(body.decode('utf-8'))
        try:
            msg = self.parser.parse(doc['raw'])

            if msg['type'] != 'other':
                msg.update({'roomID': doc['rid'], 'time': doc['ts']})

                if self.msg_handler is not None:
                    self.msg_handler(msg)

                self.producer.send(StreamProducer.ROUTE_STREAM + doc['rid'], json.dumps(msg))

        except pika.exceptions.ConnectionClosed:
            print('Reconnect.....Producer')
            self.producer = StreamProducer()
        except Exception as e:
            print(repr(e))

    def start(self):
        self.channel.start_consuming()


class DanmuConsumer(object):
    """
    Unused. Use Web STOMP instead.
    http://www.rabbitmq.com/web-stomp.html
    https://www.rabbitmq.com/stomp.html
    """

    def __init__(self, rid: str, handler, host='localhost', port=5672):
        self.handler = handler

        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=StreamProducer.EXCHANGE, exchange_type='topic')

        result = self.channel.queue_declare()
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=StreamProducer.EXCHANGE,
                                queue=queue_name,
                                routing_key=StreamProducer.ROUTE_STREAM + rid)

        self.channel.basic_consume(self.callback, queue=queue_name, no_ack=True)

    def callback(self, ch, method, properties, body):
        doc = json.loads(body)
        self.handler(doc)

    def start(self):
        self.channel.start_consuming()


if __name__ == '__main__':
    ParserConsumer(host=settings.MQ_DISPATCHER_ADDRESS, port=settings.MQ_DISPATCHER_PORT).start()
