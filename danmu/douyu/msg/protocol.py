import struct
from grako.exceptions import FailedParse
from danmu.douyu.msg.msg_parser import DanmuParser, DanmuSemantics


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


class Protocol(object):
    TYPE_CLIENT = 689
    TYPE_SERVER = 690

    def __init__(self):
        self.header_pseudo_size = 8
        self.header_size = 12
        self.header_fmt = '<IIHBB'

        self.parser = MsgParser()

    def pack(self, msg_type: int, payload: str) -> bytes:
        payload_len = len(payload)
        size = self.header_pseudo_size + payload_len + 1

        return struct.pack(self.header_fmt + '{:d}sB'.format(payload_len),
                           size, size,
                           msg_type, 0, 0,
                           payload.encode('utf-8'), 0)

    def unpack_header(self, header: bytes) -> (int, int):
        length, _, msg_type, _, _ = struct.unpack(self.header_fmt, header)
        length = length - self.header_pseudo_size

        return msg_type, length

    def unpack_payload(self, payload: bytes, length: int) -> dict:
        payload, zero = struct.unpack_from('{:d}sB'.format(length - 1), payload)
        payload = payload.decode('utf-8')

        return self.parser.parse(payload)
