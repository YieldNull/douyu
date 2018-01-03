#!/usr/bin/env bash

while read -u 10 date; do
    spark-submit --class ETL --master "local[*]" target/scala-2.11/danmuetl_2.11-1.0.jar \
    file:///Users/junjie/Downloads/etl/rdb/gift_with_price.csv \
    file:///Users/junjie/Downloads/etl/trans \
    file:///Users/junjie/Downloads/etl/spark $date

    find /Users/junjie/Downloads/etl/spark -name '*.csv' | \
    xargs -I {} bash -c 'export f={} && export d=`dirname $f` && mv $f $d.csv && rm -rf $d'
done 10<dates.txt