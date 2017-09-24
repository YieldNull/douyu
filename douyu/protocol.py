import socket
import struct
from douyu.msg_parser import DanmuParser, DanmuSemantics
from grako.exceptions import FailedParse


class MsgSemantics(DanmuSemantics):
    def __init__(self, user_input_keys=None):
        if user_input_keys is None:
            user_input_keys = ['txt']
        self.user_input_keys = user_input_keys
        self.parser = DanmuParser()

    def rec_parse(self, data):
        try:
            data = self.parser.parse(text=data, semantics=MsgSemantics())
        except FailedParse:
            if data.find('@A') > 0:
                data = self.rec_parse(data.replace('@A', '@').replace('@S', '/'))
        return data

    def start(self, ast):
        return ast

    def array(self, ast):
        if isinstance(ast[0], tuple):
            return dict(ast)
        else:
            return ast

    def item(self, ast):
        if not isinstance(ast[0], tuple):
            return self.rec_parse(ast[0])
        else:
            return ast[0]

    def pair(self, ast):
        key = ast[0]
        data = ast[2]

        if key not in self.user_input_keys:
            data = self.rec_parse(data)

        return key, data

    def data(self, ast):
        return ''.join(ast)

    def key(self, ast):
        return ''.join(ast)

    def char(self, ast):
        if ast == '@S':
            return '/'
        elif ast == '@A':
            return '@'
        else:
            return ast


class MsgParser(DanmuParser):
    def parse(self, text, rule_name='start', filename=None,
              buffer_class=None, semantics=MsgSemantics(), trace=False,
              whitespace=None, **kwargs):
        return super().parse(text, rule_name, filename, buffer_class, semantics, trace, whitespace, **kwargs)


class Douyu(object):
    def __init__(self):
        self.server_address = 'openbarrage.douyutv.com'
        self.server_port = 8601

        self.header_pseudo_size = 8
        self.header_size = 12
        self.header_fmt = '<IIHBB'

        self.msg_type_user = 689
        self.msg_type_server = 690

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.msg_parser = MsgParser()

    def login(self, room_id):
        self.socket.connect((self.server_address, self.server_port))
        self.send('type@=loginreq/roomid@={:d}/'.format(room_id))
        self.recv()
        self.send('type@=joingroup/rid@={:d}/gid@=-9999/'.format(room_id))
        self.recv()

    def send(self, payload):
        payload_len = len(payload)
        size = self.header_pseudo_size + payload_len + 1

        data = struct.pack(self.header_fmt + '{:d}sB'.format(payload_len),
                           size, size,
                           self.msg_type_user, 0, 0,
                           payload.encode('utf-8'), 0)

        self.socket.send(data)

    def recv(self):
        response = self.socket.recv(self.header_size)

        length, _, msg_type, _, _ = struct.unpack(self.header_fmt, response)

        assert msg_type == self.msg_type_server

        length = length - self.header_pseudo_size
        response = self.socket.recv(length)
        payload, zero = struct.unpack('{:d}sB'.format(length - 1), response)
        payload = payload.decode('utf-8')

        msg = self.msg_parser.parse(payload)

        print(msg)

        return msg


def parse():
    import codecs, sys

    parser = MsgParser()
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        line = f.readline()
        while line != "":
            try:
                print(parser.parse(text=line))
            except Exception:
                print(line)
            line = f.readline()


if __name__ == '__main__':
    t = Douyu()
    t.login(2124270)
