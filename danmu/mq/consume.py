import pika
import json
from danmu.mq import RawProducer, StreamProducer
from danmu.msg import RegexParser


class ParserConsumer(object):
    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=RawProducer.EXCHANGE, exchange_type='direct')

        queue_name = 'danmu.queue.raw'
        self.channel.queue_declare(queue=queue_name, auto_delete=True)

        self.channel.queue_bind(exchange=RawProducer.EXCHANGE,
                                queue=queue_name,
                                routing_key=RawProducer.ROUTE_PARSER)

        self.channel.basic_consume(self.callback, queue=queue_name, no_ack=True)
        self.parser = RegexParser()

        self.producer = StreamProducer()

    def callback(self, ch, method, properties, body):
        doc = json.loads(body)
        try:
            msg = self.parser.parse(doc['raw'])

            if msg['type'] != 'other':
                msg.update({'rid': doc['rid'], 'ts': doc['ts']})
                self.producer.send(StreamProducer.ROUTE_STREAM + doc['rid'], json.dumps(msg))

                print(msg)
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
    ParserConsumer().start()
