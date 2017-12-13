import math
import pymongo
import hashlib
import time
import requests

from flask import Flask, render_template, jsonify, abort, url_for
from settings import MONGO_DATABASE, MONGO_URI, PAGINATE_BY

app = Flask(__name__)

mongo_db = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/room/<string:rid>')
def live(rid):
    c = mongo_db['room'].find({'rid': rid, 'isOnline': True}).count()
    if c == 0:
        abort(404)

    return render_template('room.html', rid=rid)


@app.route('/cate/')
def cate_index():
    return render_template('cateAll.html')


@app.route('/cate/<string:cid>')
def cate_detail(cid):
    count = mongo_db['cate'].find({'cid': cid}).count()
    if count < 0:
        abort(404)

    return render_template('cate.html', cid=cid)


@app.route('/api/live/<int:page>')
def api_live(page):
    count = mongo_db['room'].find({'isOnline': True}).count()
    page_cnt = math.ceil(count / PAGINATE_BY)

    if page < 0 or page > page_cnt:
        return jsonify({'code': 1, 'msg': 'No such page'})

    meta = []
    for doc in mongo_db['room'].find({'isOnline': True}) \
            .sort([('online', -1)]) \
            .skip((page - 1) * PAGINATE_BY) \
            .limit(PAGINATE_BY):
        doc.pop('_id')
        doc.pop('isOnline')
        doc['roomUrl'] = url_for('live', rid=doc['rid'])
        doc['cateUrl'] = '/cate/%s' % doc['cid']
        meta.append(doc)

    return jsonify({'page_cnt': page_cnt, 'data': meta, 'code': 0, 'msg': 'success'})


@app.route('/api/cate/<int:page>')
def api_cate(page):
    count = mongo_db['cate'].find({}).count()
    page_cnt = math.ceil(count / PAGINATE_BY)

    if page < 0 or page > page_cnt:
        return jsonify({'code': 1, 'msg': 'No such page'})

    cate = []
    for doc in mongo_db['cate'].find({}).sort([('roomCount', -1)]).skip((page - 1) * PAGINATE_BY).limit(PAGINATE_BY):
        doc.pop('_id')
        doc['url'] = '/cate/%s' % doc['cid']
        cate.append(doc)

    return jsonify({'page_cnt': page_cnt, 'data': cate, 'code': 0, 'msg': 'success'})


@app.route('/api/cate_room/<string:cid>/<int:page>')
def api_cate_room(cid, page):
    count = mongo_db['room'].find({'cid': cid, 'isOnline': True}).count()
    page_cnt = math.ceil(count / PAGINATE_BY)

    if page < 0 or page > page_cnt:
        return jsonify({'code': 1, 'msg': 'No such page'})

    meta = []
    for doc in mongo_db['room'] \
            .find({'cid': cid, 'isOnline': True}) \
            .sort([('online', -1)]) \
            .skip((page - 1) * PAGINATE_BY) \
            .limit(PAGINATE_BY):
        doc.pop('_id')
        doc.pop('isOnline')
        doc['roomUrl'] = url_for('live', rid=doc['rid'])
        doc['cateUrl'] = '/cate/%s' % doc['cid']
        meta.append(doc)

    return jsonify({'page_cnt': page_cnt, 'data': meta, 'code': 0, 'msg': 'success'})


@app.route('/api/stream/<int:rid>')
def api_stream(rid):
    def get_url(room_id):
        """
        https://github.com/soimort/you-get/blob/master/src/you_get/extractors/douyutv.py
        :param room_id: room id
        :return: FLV URL
        """
        api_url = "http://www.douyutv.com/api/v1/"
        args = "room/%s?aid=wp&client_sys=wp&time=%d" % (room_id, int(time.time()))
        auth_md5 = (args + "zNzMV1y4EMxOHS6I5WKm").encode("utf-8")
        auth_str = hashlib.md5(auth_md5).hexdigest()
        json_request_url = "%s%s&auth=%s" % (api_url, args, auth_str)


        # print(requests.get(json_request_url).content.decode('gb2312'))

        json_content = requests.get(json_request_url).json()
        data = json_content['data']
        server_status = json_content.get('error', 0)
        if server_status is not 0:
            raise ValueError("Server returned error:%s" % server_status)

        show_status = data.get('show_status')
        if show_status is not "1":
            raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

        return data.get('rtmp_url') + '/' + data.get('rtmp_live')

    return jsonify({'code': 0, 'msg': 'success', 'url': get_url(rid)})

    # try:
    #     return jsonify({'code': 0, 'msg': 'success', 'url': get_url(rid)})
    # except Exception as e:
    #     return jsonify({'code': 1, 'msg': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
