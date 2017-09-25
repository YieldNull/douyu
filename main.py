from douyu.spider.danmu import listen_using_multi_process

if __name__ == '__main__':
    rids = [
        2250040,
        70231,
        2250040,
        98144,
        220185,
        1359374,
        274874,
        2014101,
        3250449,
        1432054,
        2670580,
        829815,
        2152273
    ]

    listen_using_multi_process(rids)
