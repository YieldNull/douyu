from danmu.douyu.msg.protocol import MsgParser


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
    parse()
