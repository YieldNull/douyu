import requests
from etl import settings


def notify(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        requests.post(
            settings.IFTTT_WEBHOOK,
            json={
                'value1': content
            })


if __name__ == '__main__':
    import sys

    notify(sys.argv[1])
