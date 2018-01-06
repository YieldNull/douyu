import queue
import threading
import time
import os
from mq import ParserConsumer


class Storage(object):
    def __init__(self, repo):
        self.jobs = queue.Queue()

        self.repo = repo
        self.date = time.strftime('%Y_%m_%d')

        self._open_fds()

        self.thread = threading.Thread(target=self._handler_thread)
        self.thread.start()

    def handle(self, msg):
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


if __name__ == '__main__':
    import sys

    s = Storage(sys.argv[1])

    p = ParserConsumer(msg_handler=s.handle)
    p.start()
