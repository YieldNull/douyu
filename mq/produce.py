import pika


class RawProducer(object):
    EXCHANGE = 'raw'
    ROUTE_PARSER = 'parser'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')

    def send(self, route, msg):
        print(msg)
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()


class MsgProducer(object):
    EXCHANGE = 'msg'

    ROUTE_STREAM = 'stream.room.'
    ROUTE_DB = 'db'
    ROUTE_ML = 'ml'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='topic')

    def send(self, route, msg):
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()


class MetaProducer(object):
    EXCHANGE = 'meta'

    ROUTE_HOTTEST = 'hottest'

    def __init__(self, host='localhost', port=5672):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.conn.channel()

    def send(self, route, msg):
        self.channel.basic_publish(exchange=self.EXCHANGE, routing_key=route, body=msg)

    def close(self):
        self.conn.close()
