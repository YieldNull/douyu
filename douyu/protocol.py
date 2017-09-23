from douyu.msg_parser import DanmuParser, DanmuSemantics
from grako.exceptions import FailedParse


class MySemantics(DanmuSemantics):
    def __init__(self, user_input_keys=None):
        if user_input_keys is None:
            user_input_keys = ['txt']
        self.user_input_keys = user_input_keys

    def rec_parse(self, data):
        parser = DanmuParser()
        try:
            data = parser.parse(text=data, semantics=MySemantics())
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


class MyParser(DanmuParser):
    def parse(self, text, rule_name='start', filename=None,
              buffer_class=None, semantics=MySemantics(), trace=False,
              whitespace=None, **kwargs):
        return super().parse(text, rule_name, filename, buffer_class, semantics, trace, whitespace, **kwargs)


if __name__ == '__main__':
    import codecs, sys

    parser = MyParser()
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        line = f.readline()
        while line != "":
            try:
                print(parser.parse(text=line))
            except Exception:
                print(line)
            line = f.readline()
