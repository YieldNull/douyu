#!/usr/bin/env python3

def extract(in_file, out_file):
    import re

    with open(out_file, 'a', encoding='utf-8', buffering=1024 * 1024 * 10) as fout:
        with open(in_file, 'r', encoding='utf-8', buffering=1024 * 1024 * 10) as fin:
            for line in fin:
                m = re.search('txt@=([^/]+)/', line)
                if m is not None:
                    fout.write('%s\n' % m.group(1))


def urls(out_file):
    import oss2
    from tool import settings as local

    auth = oss2.Auth(local.OSS_KEY, local.OSS_SECRET)
    bucket = oss2.Bucket(auth, local.OSS_ENDPOINT, local.OSS_BUCKET)

    with open(out_file, 'w', encoding='utf-8') as fout:
        for obj in bucket.list_objects(prefix='Storage', max_keys=1000).object_list:
            url = 'http://%s/%s' % (local.OSS_DOMAIN, obj.key)
            fout.write('%s\n' % url)


if __name__ == '__main__':
    import sys

    extract(sys.argv[1], sys.argv[2])

    print(sys.argv[1])
