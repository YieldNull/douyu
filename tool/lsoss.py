import oss2
import re
import os
from tool import settings as local


def urls(out_file):
    auth = oss2.Auth(local.OSS_KEY, local.OSS_SECRET)
    bucket = oss2.Bucket(auth, local.OSS_ENDPOINT, local.OSS_BUCKET)

    with open(out_file, 'w', encoding='utf-8') as fout:
        for obj in bucket.list_objects(prefix='Storage', max_keys=1000).object_list:
            url = 'http://%s/%s' % (local.OSS_DOMAIN, obj.key)
            fout.write('%s\n' % url)


def urls_group_by_date(repo, today):
    if not os.path.exists(repo):
        os.makedirs(repo, exist_ok=True)

    auth = oss2.Auth(local.OSS_KEY, local.OSS_SECRET)
    bucket = oss2.Bucket(auth, local.OSS_ENDPOINT, local.OSS_BUCKET)

    dates = set()

    for obj in bucket.list_objects(prefix='Storage', max_keys=1000).object_list:
        date = re.search('.*?_(\w+).txt.bz', obj.key).group(1)

        if date == today or today is None:
            with open(os.path.join(repo, '%s.txt' % date), 'a', encoding='utf-8') as fout:
                url = 'http://%s/%s' % (local.OSS_DOMAIN, obj.key)
                fout.write('%s\n' % url)

            dates.add(date)

    with open(os.path.join(repo, 'dates.txt'), 'w', encoding='utf-8') as fout:
        for date in sorted(dates):
            fout.write('%s\n' % date)


if __name__ == '__main__':
    import sys

    urls_group_by_date(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
