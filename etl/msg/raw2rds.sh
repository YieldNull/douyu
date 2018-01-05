#!/usr/bin/env bash

dir=$(dirname "$0")
dest=$1
urls=$2
date=$3

mkdir -p "$dest"

mkdir "$dest/splits"
mkdir "$dest/results-tmp"

while read -u 10 url; do
    echo $url
    wget -q $url
    bz=`basename $url`
    tar xvf $bz --strip-components=3
    name="${bz%.*}"
    split -l 10000 $name "$dest/splits/${name%.*}"

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