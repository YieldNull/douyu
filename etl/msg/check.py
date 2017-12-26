import pandas as pd


def check(prefix):
    gift = pd.read_csv('%s_gift.txt' % prefix, delimiter='\t', names=['room', 'user', 'gift', 'ts'])

    text = pd.read_csv('%s_text.txt' % prefix, delimiter='\t', names=['room', 'user', 'ts'])

    uenter = pd.read_csv('%s_uenter.txt' % prefix, delimiter='\t', names=['room', 'user', 'ts'])

    u2u = pd.read_csv('%s_u2u.txt' % prefix, delimiter='\t', names=['room', 'sender', 'receiver', 'gift', 'ts'])

    users = set()
    rooms = set()
    gifts = set()

    users.update(gift['user'].unique())
    users.update(text['user'].unique())
    users.update(uenter['user'].unique())
    users.update(u2u['sender'].unique())
    users.update(u2u['receiver'].unique())

    rooms.update(gift['room'].unique())
    rooms.update(text['room'].unique())
    rooms.update(uenter['room'].unique())
    rooms.update(u2u['room'].unique())

    gifts.update(gift['gift'].unique())
    gifts.update(u2u['gift'].unique())

    print(len(users))
    print(len(rooms))
    print(len(gifts))


if __name__ == '__main__':
    import sys

    check(sys.argv[1])
