import re
import logging
import queue
import threading
import time
import os


class RegexParser(object):
    __author__ = 'LEO'

    usrN = re.compile('username@=([^\/]+)\/')  # 用户名
    nN = re.compile('nn@=([^\/]+)\/')  # 用户昵称
    content = re.compile('txt@=([^\/]+)\/')  # 弹幕内容
    brid = re.compile('brid@=([0-9]+)\/')  # 徽章房间
    type = re.compile('type@=([^\/]+)\/')  # 数据类型
    giftId = re.compile('gfid@=([0-9]+)\/')  # 礼物类型
    ulevel = re.compile('level@=([0-9]+)\/')  # 用户等级
    contentColor = re.compile('col@=([0-9])\/')  # 弹幕颜色
    noblelv = re.compile('nl@=([0-9]+)\/')  # 贵族等级
    badgenn = re.compile('bnn@=([^\/]+)\/')  # 徽章昵称
    badgelv = re.compile('bl@=([0-9]+)\/')  # 徽章等级
    biggift = re.compile('bg@=([0-9])\/')  # 大礼物
    sendGiftUser = re.compile('snk@=([^\/]+)\/')  # 派送礼物的用户名,指派送给用户
    getGiftUser = re.compile('dnk@=([^\/]+)\/')  # 获得礼物的用户名
    getPnm = re.compile('pnm@=([^\/]+)\/')
    sendGift2Anchor = re.compile('sn@=([^\/]+)\/')  # 赠送礼物的用户名，指赠送给主播
    dn = re.compile('dn@=([^\/]+)\/')  # 获赠礼物主播
    drid = re.compile('drid@=([0-9]+)\/')
    giftName = re.compile('gn@=([^\/]+)\/')  # 礼物名字,一般是火箭或者飞机

    def __init__(self):
        self.methodDict = {'chatmsg': self.getInfoFromMsg,
                           'dgb': self.getGiftInfo,
                           'uenter': self.getSpecialUser,
                           'gpbc': self.getGiftUser2User,
                           'spbc': self.getSuperGift
                           }
        # self.dict = {}

    def __getMsgType(self, msg):
        return self.type.search(msg).group(1)

    def __getUserName(self, msg):
        return self.usrN.search(msg).group(1)

    def __getBrid(self, msg):
        return self.brid.search(msg).group(1)

    def __getNickName(self, msg):
        return self.nN.search(msg).group(1)

    def __getContent(self, msg):
        return self.content.search(msg).group(1)

    def __getGiftType(self, msg, giftdict=None):
        if giftdict is None:
            return self.giftId.search(msg).group(1)

    def __getUserLv(self, msg):
        return self.ulevel.search(msg).group(1)

    def __getNobleLv(self, msg):
        return self.noblelv.search(msg).group(1)

    def __getBadgeName(self, msg):
        if self.badgenn.search(msg) is not None:
            return self.badgenn.search(msg).group(1)
        else:
            return None

    def __getBadgelv(self, msg):
        return self.badgelv.search(msg).group(1)

    def __getSendGiftUser(self, msg):
        return self.sendGiftUser.search(msg).group(1)

    def __getGiftUser(self, msg):
        return self.getGiftUser.search(msg).group(1)

    def __getSendGift2Anchor(self, msg):
        return self.sendGift2Anchor.search(msg).group(1)

    def __getPnm(self, msg):
        return self.getPnm.search(msg).group(1)

    def __getDn(self, msg):
        return self.dn.search(msg).group(1)

    def __getdrid(self, msg):
        return self.drid.search(msg).group(1)

    def __getGiftName(self, msg):
        return self.giftName.search(msg).group(1)

    '''
    type:chatmsg

    '''

    def getInfoFromMsg(self, msg, type):
        if (msg is None):
            return
        name = self.__getNickName(msg)
        content = self.__getContent(msg)
        userlevel = self.__getUserLv(msg)
        # noblelv=self.__getNobleLv(msg)
        badgename = self.__getBadgeName(msg)
        badgelevel = self.__getBadgelv(msg)
        brid = self.__getBrid(msg)
        # self.dict[name] = [content, userlevel, badgename, badgelevel, time]
        # logging.info('{}:{}'.format(name, content))
        return {'username': name, 'content': content, 'userlevel': userlevel,
                'badgename': badgename if badgename else '',
                'badgelv': badgelevel if badgelevel else '0', 'broomID': brid, 'type': type}

    '''
    type:uenter

    '''

    def getSpecialUser(self, msg, type):
        if (msg is None):
            return
        name = self.__getNickName(msg)
        userlevel = self.__getUserLv(msg)
        return {'username': name, 'userlevel': userlevel, 'type': type}

    '''
    type:dgb

    '''

    def getGiftInfo(self, msg, type):
        if (msg is None):
            return
        name = self.__getNickName(msg)
        giftId = self.__getGiftType(msg)
        userlevel = self.__getUserLv(msg)
        badgename = self.__getBadgeName(msg)
        badgelevel = self.__getBadgelv(msg)
        brid = self.__getBrid(msg)
        return {'username': name, 'userlevel': userlevel, 'giftID': giftId,
                'badgename': badgename if badgename else '',
                'badgelv': badgelevel if badgelevel else '0',
                'broomID': brid, 'type': type}

    '''
    type:spbc

    '''

    def getSuperGift(self, msg, type):
        if (msg is None):
            return
        name = self.__getSendGift2Anchor(msg)
        giftname = self.__getGiftName(msg)
        aname = self.__getDn(msg)
        drid = self.__getdrid(msg)
        return {'username': name, 'giftname': giftname, 'aname': aname, 'droomID': drid, 'type': type}

    '''
    type:gpbc

    '''

    def getGiftUser2User(self, msg, type):
        if (msg is None):
            return

        # Todo
        sname = self.__getSendGiftUser(msg)
        rname = self.__getGiftUser(msg)
        pnm = self.__getPnm(msg)
        return {'username': sname, 'rusername': rname, 'pnm': pnm, 'type': type}

    '''
    other

    '''

    def getOther(self, msg):
        if msg is None:
            return
        return {'other': msg, 'type': 'other'}

    def parse(self, msg: str):
        if (msg is None):
            return
        # print(msg)
        # print(self.__getMsgType(msg))
        type = self.__getMsgType(msg)
        if type in self.methodDict:
            return self.methodDict.get(type)(msg, type)
        else:
            return self.getOther(msg)


class ParserStorage(object):
    def __init__(self, repo):
        self.jobs = queue.Queue()

        self.repo = repo
        self.date = time.strftime('%Y_%m_%d')

        self._open_fds()

        self.thread = threading.Thread(target=self._handler_thread)
        self.thread.start()

    def store(self, msg):
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self._handler_thread)
            self.thread.start()
            # self.logger.warn("Working thread was dead. Restarting")

        job = self._store_msg(msg)
        self.jobs.put(job)

    def close(self):
        self._safe_close(self.fp_text)
        self._safe_close(self.fp_gift)
        self._safe_close(self.fp_sgift)
        self._safe_close(self.fp_u2u)
        self._safe_close(self.fp_uenter)

    def _safe_close(self, fd):
        if fd is not None:
            try:
                fd.close()
            except:
                pass

    def _open_fds(self):
        prefix = os.path.join(self.repo, self.date)

        self.fp_text = open(prefix + '_text.txt', 'a', encoding='utf-8', buffering=1024 * 64)
        self.fp_gift = open(prefix + '_gift.txt', 'a', encoding='utf-8', buffering=1024 * 64)
        self.fp_sgift = open(prefix + '_sgift.txt', 'a', encoding='utf-8', buffering=1024 * 64)
        self.fp_u2u = open(prefix + '_u2u.txt', 'a', encoding='utf-8', buffering=1024 * 64)
        self.fp_uenter = open(prefix + '_uenter.txt', 'a', encoding='utf-8', buffering=1024 * 64)

    def _handler_thread(self):
        while True:
            date = time.strftime('%Y_%m_%d')
            if date != self.date:
                self.date = date
                self.close()
                self._open_fds()

            mtype, line = self.jobs.get(block=True)
            if mtype == 'chatmsg':
                self.fp_text.write('%s\n' % line)
            elif mtype == 'dgb':
                self.fp_gift.write('%s\n' % line)
            elif mtype == 'spbc':
                self.fp_sgift.write('%s\n' % line)
            elif mtype == 'gpbc':
                self.fp_u2u.write('%s\n' % line)
            elif mtype == 'uenter':
                self.fp_uenter.write('%s\n' % line)

    def _store_msg(self, msg):
        mtype = msg['type']

        if mtype == 'chatmsg':
            return mtype, self._store_text(msg)
        elif mtype == 'dgb':
            return mtype, self._store_gift(msg)
        elif mtype == 'spbc':
            return mtype, self._store_super_gift(msg)
        elif mtype == 'gpbc':
            return mtype, self._store_u2u(msg)
        elif mtype == 'uenter':
            return mtype, self._store_uenter(msg)
        return 'other', None

    def _store_text(self, msg):
        return '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
            str(int(msg['time'])), msg['roomID'],
            msg['username'].replace('\t', ''), msg['userlevel'],
            msg['badgename'].replace('\t', ''), msg['badgelv'],
            msg['broomID'], msg['content'].replace('\n', '').replace('\r', '')
        )

    def _store_gift(self, msg):
        return '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
            str(int(msg['time'])), msg['roomID'],
            msg['username'].replace('\t', ''), msg['userlevel'],
            msg['badgename'].replace('\t', ''), msg['badgelv'],
            msg['broomID'], msg['giftID'].replace('\t', '')
        )

    def _store_super_gift(self, msg):
        return '%s\t%s\t%s\t%s\t%s\t%s' % (
            str(int(msg['time'])), msg['roomID'],
            msg['droomID'], msg['username'].replace('\t', ''),
            msg['giftname'].replace('\t', ''), msg['aname'].replace('\t', '')
        )

    def _store_u2u(self, msg):
        return '%s\t%s\t%s\t%s\t%s' % (
            str(int(msg['time'])), msg['roomID'],
            msg['username'].replace('\t', ''), msg['rusername'].replace('\t', ''),
            msg['pnm'].replace('\t', '')
        )

    def _store_uenter(self, msg):
        return '%s\t%s\t%s\t%s' % (
            str(int(msg['time'])), msg['roomID'],
            msg['username'].replace('\t', ''), msg['userlevel']
        )


def parse_raw(parser, line):
    first_space = line.find(' ')
    second_space = line.find(' ', first_space + 1)

    rid = line[:first_space]
    timestamp = line[first_space + 1:second_space]
    msg = line[second_space + 1:len(line) - 1]

    try:
        doc = parser.parse(msg)
    except AttributeError as e:
        return None

    doc.update({'roomID': rid, 'time': timestamp})

    return doc