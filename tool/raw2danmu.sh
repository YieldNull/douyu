#!/usr/bin/env bash

while read -u 10 url; do
    wget -q $url
    bz=`basename $url`
    tar xvf $bz --strip-components=3
    name="${bz%.*}"
    ./raw2danmu.py $name danmu.txt
    rm $bz
    rm $name
done 10<urls.txt