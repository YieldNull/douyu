import pymongo
from etl.warehouse.models import Room, RoomCate, RoomCateMap
from etl import settings


def update_room():
    mongo = pymongo.MongoClient(settings.MONGO_URI)[settings.MONGO_DATABASE]
    for doc in mongo['room'].find():
        RoomCate.insert(cate_key=doc['cid'], cate_id=doc['cid'], name=doc['cate']).upsert().execute()

        Room.insert(room_key=doc['rid'], room_id=doc['rid'], name=doc['roomName'],
                    anchor=doc['nickName']).upsert().execute()

        RoomCateMap.insert(room_key=doc['rid'], cate_key=doc['cid']).upsert().execute()


if __name__ == '__main__':
    update_room()
