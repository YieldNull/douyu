from scrapy import Item, Field


class RoomItem(Item):
    TYPE_LIVE = 1
    TYPE_CATE = 2

    rtype = Field()
    cid = Field()
    rid = Field()
    img = Field()
    cate = Field()
    cateUrl = Field()
    online = Field()
    roomName = Field()
    nickName = Field()


class CateItem(Item):
    cid = Field()
    name = Field()
    url = Field()
    img = Field()


class CateCountItem(Item):
    cid = Field()
    roomCount = Field()
