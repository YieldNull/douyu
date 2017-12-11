from scrapy import Item, Field


class RoomItem(Item):
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
