import struct


class Protocol(object):
    TYPE_CLIENT = 689
    TYPE_SERVER = 690

    def __init__(self):
        self.header_pseudo_size = 8
        self.header_size = 12
        self.header_fmt = '<IIHBB'

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
