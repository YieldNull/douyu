from scrapy import Spider, Request
from metaspider.items import RoomItem, CateItem
import json


class LiveSpider(Spider):
    name = 'live'

    def start_requests(self):
        yield Request(url='https://www.douyu.com/gapi/rkc/directory/0_0/1',
                      headers={'Referer': 'https://www.douyu.com/directory/all',
                               'X-Requested-With': 'XMLHttpRequest'},
                      )

    def parse(self, response):
        payload = json.loads(response.body_as_unicode())

        if payload['code'] == 0:
            rt = payload['data']['rl']
            for item in rt:
                yield RoomItem(cid=str(item['cid2']), rid=str(item['rid']),
                               img=item['rs1'], cate=item['c2name'],
                               cateUrl=item['c2url'], online=item['ol'],
                               roomName=item['rn'], nickName=item['nn'])

        page = int(response.url[response.url.rindex('/') + 1:])
        page_count = payload['data']['pgcnt']

        if page < page_count:
            yield Request(url='%s/%d' % (response.url[:response.url.rindex('/')], page + 1),
                          headers={'Referer': response.url,
                                   'X-Requested-With': 'XMLHttpRequest'},
                          )


class CateSpider(LiveSpider):
    name = 'cate'

    def start_requests(self):
        yield Request(url='https://www.douyu.com/directory',
                      headers={'Referer': 'https://www.douyu.com'})

    def parse(self, response):
        for item in response.xpath('//ul[@id="live-list-contentbox"]/li'):
            name = item.xpath('./a/p/text()').extract_first()
            cid = item.xpath('./a/@data-tid').extract_first()
            url = item.xpath('./a/@href').extract_first()
            img = item.xpath('./a/img/@data-original').extract_first()

            yield CateItem(cid=str(cid), name=name, url=url, img=img)

            yield Request(url='https://www.douyu.com/gapi/rkc/directory/2_%s/1' % cid, callback=super().parse)
