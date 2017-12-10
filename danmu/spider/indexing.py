import requests
from danmu import get_logger
from danmu.redis import RedisClient

logger = get_logger('MetaFetcher')

client = RedisClient()


def metadata(page=1):
    url = 'https://www.douyu.com/gapi/rkc/directory/0_0/{:d}'.format(page)
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Host': 'www.douyu.com',
        'Referer': 'https://www.douyu.com/directory/all',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }

    payload = requests.get(url, headers=headers).json()

    if payload['code'] != 0:
        return []
    else:
        rt = payload['data']['rl']

        client.save_meta([
            {
                'rid': str(item['rid']),
                'img': item['rs1'],
                'cate': item['c2name'],
                'cateUrl': item['c2url'],
                'online': item['ol'],
                'roomName': item['rn'],
                'nickName': item['nn']
            } for item in rt])

        return [str(item['rid']) for item in rt]


def target_rids(pages):
    target = set()

    for i in range(1, pages + 1):
        try:
            target.update(metadata(i))
        except Exception as e:
            logger.warning("Error in fetching:" + repr(e))

    logger.info("Targets Amount %d" % len(target))
    return target


if __name__ == '__main__':
    metadata()
