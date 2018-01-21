#!/usr/bin/env bash

dir=$(dirname "$0")
dest=$1
urls=$2
date=$3

mkdir -p "$dest"

mkdir "$dest/splits"
mkdir "$dest/results-tmp"

while read -u 10 url; do
    echo "downloading $url"
    wget -q $url &
done 10<"$urls"

wait
echo "finish downloading"

while read -u 10 url; do
    bz=`basename $url`

    echo "extracting $bz"
    tar xvf $bz --strip-components=3 &

done 10<"$urls"

wait
echo "finish extracting"

while read -u 10 url; do
    bz=`basename $url`
    name="${bz%.*}"

    echo "splitting $name"
    split -a 4 -l 100000 $name "$dest/splits/${name%.*}" &

done 10<"$urls"

wait
echo "finish splitting"

while read -u 10 url; do
    bz=`basename $url`
    name="${bz%.*}"

    rm $bz
    rm $name
done 10<"$urls"

python3 "$dir/raw2rds.py" "$dest/splits" "$dest/results-tmp"

find "$dest/results-tmp" -name "*$date*_text.txt" | xargs cat >> $dest/"$date"_text.txt
find "$dest/results-tmp" -name "*$date*_gift.txt" | xargs cat >> $dest/"$date"_gift.txt
find "$dest/results-tmp" -name "*$date*_u2u.txt" | xargs cat >> $dest/"$date"_u2u.txt
find "$dest/results-tmp" -name "*$date*_uenter.txt" | xargs cat >> $dest/"$date"_uenter.txt
find "$dest/results-tmp" -name "*$date*_new_user.txt" | xargs cat >> $dest/"$date"_new_user.txt

rm -rf "$dest/splits"
rm -rf "$dest/results-tmp"