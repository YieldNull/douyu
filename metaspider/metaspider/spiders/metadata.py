import json
import logging
from scrapy import Spider, Request
from metaspider.items import RoomItem, CateItem, CateCountItem


class LiveSpider(Spider):
    name = 'live'
    logger = logging.getLogger('LiveSpider')

    def parse(self, response):
        pass

    def start_requests(self):
        yield Request(url='https://www.douyu.com/gapi/rkc/directory/0_0/1',
                      headers={'Referer': 'https://www.douyu.com/directory/all',
                               'X-Requested-With': 'XMLHttpRequest'},
                      meta={'rtype': RoomItem.TYPE_LIVE},
                      callback=self.parse_room
                      )

    def parse_room(self, response):
        url = response.url
        payload = json.loads(response.body_as_unicode())

        if payload['code'] == 0:
            items = payload['data']['rl']
            for item in items:
                yield RoomItem(rtype=response.meta['rtype'],
                               cid=str(item['cid2']), rid=str(item['rid']),
                               img=item['rs1'], cate=item['c2name'],
                               cateUrl=item['c2url'], online=item['ol'],
                               roomName=item['rn'], nickName=item['nn'])

            page = int(url[url.rindex('/') + 1:])
            page_count = payload['data']['pgcnt']

            if page < page_count:
                yield Request(url='%s/%d' % (url[:url.rindex('/')], page + 1),
                              headers={'Referer': response.url,
                                       'X-Requested-With': 'XMLHttpRequest'},
                              meta={'rtype': response.meta['rtype']},
                              callback=self.parse_room
                              )
            else:
                if response.meta['rtype'] == RoomItem.TYPE_CATE:
                    cid = url[url.rindex('_') + 1:url.rindex('/')]
                    yield CateCountItem(cid=cid, roomCount=max(0, page_count - 1) * 120 + len(items))
        else:
            self.logger.warning('Error in get %s: %s' % (response.url, payload))


class CateSpider(LiveSpider):
    name = 'cate'

    logger = logging.getLogger('CateSpider')

    def start_requests(self):
        yield Request(url='https://www.douyu.com/directory',
                      headers={'Referer': 'https://www.douyu.com'},
                      callback=self.parse_cate
                      )

    def parse_cate(self, response):
        for item in response.xpath('//ul[@id="live-list-contentbox"]/li'):
            name = item.xpath('./a/p/text()').extract_first()
            cid = item.xpath('./a/@data-tid').extract_first()
            url = item.xpath('./a/@href').extract_first()
            img = item.xpath('./a/img/@data-original').extract_first()

            yield CateItem(cid=str(cid), name=name, url=url, img=img)

            yield Request(url='https://www.douyu.com/gapi/rkc/directory/2_%s/1' % cid,
                          meta={'rtype': RoomItem.TYPE_CATE},
                          callback=self.parse_room
                          )
