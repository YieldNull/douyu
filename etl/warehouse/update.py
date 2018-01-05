import csv
import pandas as pd
from etl.warehouse.models import *
from etl.warehouse.dims import store_gift


def update_user(path):
    df = pd.read_csv(path, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, names=['user', 'name', 'level'])

    for index, row in df.iterrows():
        uid = int(row['user'])
        name = row['name']
        try:
            level = int(row['level'])
        except:  # \t in name
            level = 0

        User.create(user_key=uid, user_id=uid, name=name, level=level)


def update_gift(path):
    store_gift(path)


if __name__ == '__main__':
    import sys

    update_gift(sys.argv[1])

    if len(sys.argv) > 2:
        update_user(sys.argv[2])
