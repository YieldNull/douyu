import pika


class RawProducer(object):
    EXCHANGE = 'danmu.raw'
    ROUTE_PARSER = 'parser'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')

    def send(self, route, msg):
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()


class StreamProducer(object):
    EXCHANGE = 'amq.topic'  # use build-in exchange for Web STOMP

    ROUTE_STREAM = 'stream.room.'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

    def send(self, route, msg):
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()


class MetaProducer(object):
    EXCHANGE = 'danmu.meta'

    ROUTE_HOTTEST = 'hottest'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

    def send(self, route, msg):
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()
