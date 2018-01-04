#!/usr/bin/env bash

mkdir -p "/Users/junjie/Downloads/etl/dest"

while read -u 10 date; do
    spark-submit --class ETL --master "local[*]" target/scala-2.11/danmuetl_2.11-1.0.jar \
    file:///Users/junjie/Downloads/etl/rdb/gift_with_price.csv \
    file:///Users/junjie/Downloads/etl/trans \
    file:///Users/junjie/Downloads/etl/spark $date

    find /Users/junjie/Downloads/etl/spark -name '*.csv' | \
    xargs -I {} bash -c 'export f={} && export d=`dirname $f` && export name=`basename $d` && mv $f /Users/junjie/Downloads/etl/dest/$name.csv && rm -rf $d'

    export PYTHONPATH=../../ && python3 ../warehouse/facts.py $date
done 10<dates.txt