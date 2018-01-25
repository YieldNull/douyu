import pymongo
from etl.warehouse.models import Room, RoomCate, RoomCateMap
from etl import settings


def update_room():
    mongo = pymongo.MongoClient(settings.MONGO_URI)[settings.MONGO_DATABASE]
    for doc in mongo['room'].find():
        try:
            rc, created = RoomCate.get_or_create(cate_key=doc['cid'],
                                                 defaults={'cate_id': doc['cid'], 'name': doc['cate']})
            if (not created) and (rc.name != doc['cate']):
                RoomCate.update(name=doc['cate']).where(RoomCate.cate_key == doc['cid']).execute()

            r, created = Room.get_or_create(room_key=doc['rid'],
                                            defaults={'room_id': doc['rid'], 'name': doc['roomName'],
                                                      'anchor': doc['nickName']})

            if (not created) and (r.name != doc['roomName'] or r.anchor != doc['nickName']):
                Room.update(name=doc['roomName'], anchor=doc['nickName']).where(Room.room_key == doc['rid']).execute()

            rcm, created = RoomCateMap.get_or_create(room_key=doc['rid'], defaults={'cate_key': doc['cid']})
            if (not created) and (rcm.cate_key != int(doc['cid'])):
                # RoomCateMap.update(cate_key=doc['cid']).where(RoomCateMap.room_key == doc['rid']).execute()
                RoomCateMap.delete().where(RoomCateMap.room_key == doc['rid']).execute()
                RoomCateMap.insert(room_key=doc['rid'], cate_key=doc['cid'])

        except Exception as e:
            print('%s : %s' % (str(doc['rid']), repr(e)))


if __name__ == '__main__':
    update_room()
