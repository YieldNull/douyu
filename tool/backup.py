import os
import oss2
import time
import subprocess
import tempfile
import requests
from datetime import datetime, timedelta
from danmu import settings
from tool import settings as local

auth = oss2.Auth(local.OSS_KEY, local.OSS_SECRET)
bucket = oss2.Bucket(auth, local.OSS_ENDPOINT, local.OSS_BUCKET)

if __name__ == '__main__':

    date_str = time.strftime(settings.FILE_STORAGE_DATE_FORMAT)
    now = datetime.now().date()

    backed_up = []

    for filename in os.listdir(settings.FILE_STORAGE_REPOSITORY):
        if filename.endswith('.txt'):
            date = None
            try:
                date = datetime.strptime(filename[-4 - len(date_str):-4], settings.FILE_STORAGE_DATE_FORMAT).date()
            except ValueError:
                continue

            if date == now - timedelta(days=1):
                key = filename + '.bz2'

                print('Uploading to ' + key)

                temp = os.path.join(tempfile.gettempdir(), key)
                path = os.path.join(settings.FILE_STORAGE_REPOSITORY, filename)

                try:
                    r = subprocess.run(['tar', '-cjf', temp, path], cwd=settings.FILE_STORAGE_REPOSITORY)

                    if r.returncode == 0:
                        bucket.put_object_from_file(key, temp)

                        if local.DELETE_SRC:
                            os.remove(path)

                    backed_up.append(key)

                finally:
                    if os.path.isfile(temp):
                        os.remove(temp)

    if len(backed_up) > 0:
        requests.post(local.IFTTT_WEBHOOK,
                      json={
                          'value1': '<br/>'.join(backed_up)
                      })
