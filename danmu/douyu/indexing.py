import requests
import re


def metadata(page=1):
    url = 'https://www.douyu.com/directory/all?page={:d}&isAjax=1'.format(page)
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Host': 'www.douyu.com',
        'Referer': 'https://www.douyu.com/directory/all',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }

    payload = requests.get(url, headers=headers).text
    return re.findall("(?<=' data-rid=')(\d+)", payload)


if __name__ == '__main__':
    metadata()
