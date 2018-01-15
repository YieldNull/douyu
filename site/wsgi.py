import math
import pymongo
import hashlib
import time
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, abort, url_for, request
from peewee import fn, SQL, JOIN

from settings import MONGO_DATABASE, MONGO_URI, PAGINATE_BY
from common.ws import RedisClient
from etl.warehouse.models import *

app = Flask(__name__)

mongo_db = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]
redis_client = RedisClient()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/room/<string:rid>')
def live(rid):
    c = mongo_db['room'].find({'rid': rid, 'isOnline': True}).count()
    if c == 0:
        abort(404)

    redis_client.publish_temporary_rid(rid)
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


@app.route('/ranking')
def ranking():
    return render_template('top.html')


@app.route('/totalStatistics')
def totalStatistics():
    return render_template('statistics.html')


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

        json_content = requests.get(json_request_url).json()
        data = json_content['data']
        server_status = json_content.get('error', 0)
        if server_status is not 0:
            raise ValueError("Server returned error:%s" % server_status)

        show_status = data.get('show_status')
        if show_status is not "1":
            raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

        return data.get('rtmp_url') + '/' + data.get('rtmp_live')

    try:
        return jsonify({'code': 0, 'msg': 'success', 'url': get_url(rid)})
    except Exception as e:
        return jsonify({'code': 1, 'msg': str(e)})


@app.route('/api/danmu/keepalive/<string:rid>')
def api_danmu_keep_alive(rid):
    c = mongo_db['room'].find({'rid': rid, 'isOnline': True}).count()
    if c == 0:
        return jsonify({'code': 1, 'msg': 'room is not online'})

    redis_client.publish_temporary_rid(rid)
    return jsonify({'code': 0, 'msg': 'success'})


@app.route('/api/stat/site/top/room/<string:date>')
def api_stat_site_top_room_at_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
    except ValueError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = RoomDailyStat.select(
        RoomDailyStat.room,
        RoomDailyStat.dcount, RoomDailyStat.gcount, RoomDailyStat.income,
        (RoomDailyStat.dcount * 100 + RoomDailyStat.income).alias('f')
    ).join(Date, on=(RoomDailyStat.date == Date.date_key)) \
        .where(Date.date == date) \
        .order_by(SQL('f').desc()) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'roomId': row.room.room_id,
            'roomName': row.room.name,
            'dcount': row.dcount,
            'gcount': row.gcount,
            'income': int(row.income / 100),
            'factor': int(row.f / 100),
            'order': order
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/top/room/<string:start>/<string:end>')
def api_stat_site_top_room_in_date_range(start, end):
    try:
        start = datetime.strptime(start, '%Y-%m-%d').date()
        end = datetime.strptime(end, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
    except ValueError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = RoomDailyStat.select(
        RoomDailyStat.room,
        RoomDailyStat.dcount, RoomDailyStat.gcount, RoomDailyStat.income,
        fn.SUM((RoomDailyStat.dcount * 100 + RoomDailyStat.income)).alias('f')
    ).join(Date, on=(RoomDailyStat.date == Date.date_key)) \
        .where((Date.date >= start) & (Date.date <= end)) \
        .group_by(RoomDailyStat.room) \
        .order_by(SQL('f').desc()) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'roomId': row.room.room_id,
            'roomName': row.room.name,
            'dcount': row.dcount,
            'gcount': row.gcount,
            'income': int(row.income / 100),
            'factor': int(row.f / 100),
            'order': order
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/top/cate/<string:date>')
def api_stat_site_top_cate_at_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
    except ValueError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = RoomDailyStat.select(
        RoomDailyStat.cate,
        fn.SUM(RoomDailyStat.dcount).alias('dsum'),
        fn.SUM(RoomDailyStat.gcount).alias('gsum'),
        fn.SUM(RoomDailyStat.income).alias('isum'),
        (fn.SUM(RoomDailyStat.dcount * 100) + fn.SUM(RoomDailyStat.income)).alias('f')
    ).join(Date, on=(RoomDailyStat.date == Date.date_key)) \
        .join(RoomCate, on=(RoomDailyStat.cate == RoomCate.cate_key)) \
        .where(Date.date == date) \
        .group_by(RoomDailyStat.cate) \
        .order_by(SQL('f').desc()) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'cateId': row.cate.cate_id,
            'cateName': row.cate.name,
            'dcount': row.dsum,
            'gcount': row.gsum,
            'income': int(row.isum / 100),
            'factor': int(row.f / 100),
            'order': order
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/top/cate/<string:start>/<string:end>')
def api_stat_site_top_cate_in_date_range(start, end):
    try:
        start = datetime.strptime(start, '%Y-%m-%d').date()
        end = datetime.strptime(end, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
    except ValueError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = RoomDailyStat.select(
        RoomDailyStat.cate,
        fn.SUM(RoomDailyStat.dcount).alias('dsum'),
        fn.SUM(RoomDailyStat.gcount).alias('gsum'),
        fn.SUM(RoomDailyStat.income).alias('isum'),
        (fn.SUM(RoomDailyStat.dcount * 100) + fn.SUM(RoomDailyStat.income)).alias('f')
    ).join(Date, on=(RoomDailyStat.date == Date.date_key)) \
        .join(RoomCate, on=(RoomDailyStat.cate == RoomCate.cate_key)) \
        .where((Date.date >= start) & (Date.date <= end)) \
        .group_by(RoomDailyStat.cate) \
        .order_by(SQL('f').desc()) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'cateId': row.cate.cate_id,
            'cateName': row.cate.name,
            'dcount': row.dsum,
            'gcount': row.gsum,
            'income': int(row.isum / 100),
            'factor': int(row.f / 100),
            'order': order
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/top/user/<string:date>/<ttype>')
def api_stat_site_top_user_at_date(date, ttype):
    tmap = {
        'danmu': TOP_TYPE_DCOUNT,
        'gift': TOP_TYPE_GCOUNT,
        'expense': TOP_TYPE_EXPENSE
    }

    order_by = {
        TOP_TYPE_DCOUNT: SiteDailyTopUser.dcount.desc(),
        TOP_TYPE_GCOUNT: SiteDailyTopUser.gcount.desc(),
        TOP_TYPE_EXPENSE: SiteDailyTopUser.expense.desc(),
    }

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
        ttype = tmap[ttype]
    except ValueError or KeyError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = SiteDailyTopUser.select() \
        .join(Date, on=(SiteDailyTopUser.date == Date.date_key)) \
        .where((Date.date == date) & (SiteDailyTopUser.ttype == ttype)) \
        .order_by(order_by[ttype]) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'user': row.user.name,
            'dcount': row.dcount,
            'gcount': row.gcount,
            'expense': row.expense,
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/top/user/<string:start>/<string:end>/<ttype>')
def api_stat_site_top_user_in_date_range(start, end, ttype):
    tmap = {
        'danmu': TOP_TYPE_DCOUNT,
        'gift': TOP_TYPE_GCOUNT,
        'expense': TOP_TYPE_EXPENSE
    }

    order_by = {
        TOP_TYPE_DCOUNT: SQL('davg').desc(),
        TOP_TYPE_GCOUNT: SQL('gavg').desc(),
        TOP_TYPE_EXPENSE: SQL('eavg').desc(),
    }

    try:
        start = datetime.strptime(start, '%Y-%m-%d').date()
        end = datetime.strptime(end, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 20))
        limit = limit if limit > 0 else 20
        ttype = tmap[ttype]
    except ValueError or KeyError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = SiteDailyTopUser.select(
        SiteDailyTopUser.user,
        fn.AVG(SiteDailyTopUser.dcount).alias('davg'),
        fn.AVG(SiteDailyTopUser.gcount).alias('gavg'),
        fn.AVG(SiteDailyTopUser.expense).alias('eavg')
    ).join(Date, on=(SiteDailyTopUser.date == Date.date_key)) \
        .where((Date.date >= start) & (Date.date <= end) & (SiteDailyTopUser.ttype == ttype)) \
        .group_by(SiteDailyTopUser.user) \
        .order_by(order_by[ttype]) \
        .limit(limit)

    payload = []
    order = 0
    for row in query:
        payload.append({
            'user': row.user.name,
            'dcount': row.davg,
            'gcount': row.gavg,
            'expense': row.eavg,
        })
        order += 1
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/site/hourly/<string:date>')
def api_stat_site_hourly(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = SiteHourlyStat.select() \
        .join(Date, on=(SiteHourlyStat.date == Date.date_key)) \
        .join(Hour, on=(SiteHourlyStat.hour == Hour.hour_key)) \
        .where(Date.date == date) \
        .order_by(Hour.hour)

    payload = []
    for row in query:
        payload.append({
            'hour': row.hour.hour,
            'ucount': row.ucount,
            'gucount': row.gucount,
            'ducount': row.ducount,
            'gcount': row.gcount,
            'dcount': row.dcount,
            'income': int(row.income / 100)
        })
    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/cate/hourly/<string:date>/<string:dim>')
def api_stat_cate_hourly(date, dim):
    dim_map = {
        'danmu': RoomHourlyStat.dcount,
        'gift': RoomHourlyStat.gcount,
        'income': RoomHourlyStat.income
    }

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        dim_model = dim_map[dim]
        limit = int(request.args.get('limit', 5))
        limit = limit if limit > 0 else 5
    except ValueError or KeyError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    sub_query = RoomHourlyStat.select(
        RoomHourlyStat.cate,
    ).join(Date, on=(RoomHourlyStat.date == Date.date_key)) \
        .where(Date.date == date) \
        .group_by(RoomHourlyStat.cate) \
        .order_by(fn.SUM(dim_model).desc()) \
        .limit(limit).alias('topc')

    query = RoomHourlyStat.select(
        RoomHourlyStat.hour,
        RoomHourlyStat.cate,
        fn.SUM(RoomHourlyStat.dcount).alias('dsum'),
        fn.SUM(RoomHourlyStat.gcount).alias('gsum'),
        fn.SUM(RoomHourlyStat.income).alias('isum')
    ).join(Hour, on=(RoomHourlyStat.hour == Hour.hour_key)) \
        .join(Date, on=(RoomHourlyStat.date == Date.date_key)) \
        .join(sub_query, on=(RoomHourlyStat.cate == sub_query.c.cate_key)) \
        .where((Date.date == date)) \
        .group_by(Hour.hour, RoomHourlyStat.cate) \
        .order_by(Hour.hour, RoomHourlyStat.cate)

    cates = {}
    for row in query:
        hours = cates.setdefault(row.cate.name, [{
            'hour': h,
            'gcount': 0,
            'dcount': 0,
            'income': 0
        } for h in range(24)])

        hours[row.hour.hour] = {
            'hour': row.hour.hour,
            'gcount': row.gsum,
            'dcount': row.dsum,
            'income': int(row.isum / 100)
        }

    def sum_aux(target):
        import functools
        return {
            'dcount': functools.reduce(lambda acc, a: acc + a['dcount'], target, 0),
            'gcount': functools.reduce(lambda acc, a: acc + a['gcount'], target, 0),
            'income': functools.reduce(lambda acc, a: acc + a['income'], target, 0)
        }

    payload = [{'cate': cate, 'data': data, 'total': sum_aux(data)} for cate, data in cates.items()]

    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/weekly/hourly/<string:date>')
def api_stat_weekly_hourly(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError or KeyError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = SiteHourlyStat.select() \
        .join(Date, on=(SiteHourlyStat.date == Date.date_key)) \
        .where((Date.date <= date) & (Date.date >= date - timedelta(days=6))) \
        .order_by(SiteHourlyStat.date)

    days = {}
    for row in query:
        hours = days.setdefault(datetime.strftime(row.date.date, '%Y-%m-%d'), [{
            'hour': h,
            'ucount': 0,
            'gucount': 0,
            'ducount': 0,
            'gcount': 0,
            'dcount': 0,
            'income': 0
        } for h in range(24)])

        hours[row.hour.hour] = {
            'hour': row.hour.hour,
            'ucount': row.ucount,
            'gucount': row.gucount,
            'ducount': row.ducount,
            'gcount': row.gcount,
            'dcount': row.dcount,
            'income': int(row.income / 100)
        }

    payload = [{'date': date,
                'weekday': datetime.strptime(date, '%Y-%m-%d').weekday(),
                'data': data, } for date, data in days.items()]

    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


@app.route('/api/stat/cate/daily/<string:date>')
def api_stat_site_cate_daily(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError or KeyError:
        return jsonify({'code': 1, 'msg': 'invalid request'})

    query = RoomHourlyStat.select(
        RoomHourlyStat.cate,
        fn.SUM(RoomHourlyStat.dcount).alias('dsum'),
        fn.SUM(RoomHourlyStat.gcount).alias('gsum'),
        fn.SUM(RoomHourlyStat.ucount).alias('usum'),
        fn.SUM(RoomHourlyStat.income).alias('isum'),
        fn.COUNT(fn.DISTINCT(RoomHourlyStat.room)).alias('rsum')
    ).join(Date, on=(RoomHourlyStat.date == Date.date_key)) \
        .where(Date.date == date) \
        .group_by(RoomHourlyStat.cate)

    payload = []
    for row in query:
        payload.append({
            'cate': row.cate.name,
            'income': row.isum,
            'ucount': row.usum,
            'gcount': row.gsum,
            'dcount': row.dsum,
            'rcount': row.rsum
        })

    return jsonify({'code': 0, 'msg': 'success', 'data': payload})


if __name__ == '__main__':
    app.run(debug=True)
