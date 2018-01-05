#!/usr/bin/env bash

dir=$(dirname "$0")

gift=$1
repo=$2
export dest=$3
date=$4

mkdir -p $dest

spark-submit --class ETL --master "local[*]" "$dir/target/scala-2.11/danmuetl_2.11-1.0.jar" \
    "file://$gift" \
    "file://$repo" \
    "file://$dest/spark-tmp" $date

find "$dest/spark-tmp" -name '*.csv' | \
xargs -I {} bash -c 'export f={} && export d=`dirname $f` && export name=`basename $d` && mv $f $dest/$name.csv'


rm -rf  "$dest/spark-tmp"