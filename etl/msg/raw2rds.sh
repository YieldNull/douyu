#!/usr/bin/env bash

mkdir results

while read -u 11 date; do
    mkdir "./splits"
    mkdir "./results-tmp"

    while read -u 10 url; do
        echo $url
        wget -q $url
        bz=`basename $url`
        tar xvf $bz --strip-components=3
        name="${bz%.*}"
        split -l 10000 $name "./splits/${name%.*}"

        rm $bz
        rm $name
    done 10<"$date".txt

    $1 "./splits" "./results-tmp"

    find "./results-tmp" -name "*$date*_text.txt" | xargs cat >> ./results/"$date"_text.txt
    find "./results-tmp" -name "*$date*_gift.txt" | xargs cat >> ./results/"$date"_gift.txt
    find "./results-tmp" -name "*$date*_u2u.txt" | xargs cat >> ./results/"$date"_u2u.txt
    find "./results-tmp" -name "*$date*_uenter.txt" | xargs cat >> ./results/"$date"_uenter.txt

    rm -rf "./splits"
    rm -rf "./results-tmp"
done 11<dates.txt