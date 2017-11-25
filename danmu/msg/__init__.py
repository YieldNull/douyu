class Parser(object):
    def parse(self, msg: str) -> dict:
        pass


from .protocol import Protocol
from .regex_parser import RegexParser
from .grako_parser import GrakoParser
