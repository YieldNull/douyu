#!/usr/bin/env bash

dir=$(dirname "$0")
repo=$1
dest=$2
date=$3

mkdir -p "$dest"
mkdir "$dest/results-tmp"

declare -a types=("text" "gift" "sgift" "u2u" "uenter")

for type in "${types[@]}"
do
    echo "${repo}/${date}_${type}.txt"

    mkdir "$dest/splits"
    split -a 4 -l 20000 "${repo}/${date}_${type}.txt" "$dest/splits/${type}_${date}"
    python3 "$dir/msg2rds.py" "$dest/splits" "$dest/results-tmp" "${type}"
    rm -rf "$dest/splits"
done


find "$dest/results-tmp" -name "*$date*_text.txt" | xargs cat >> $dest/"$date"_text.txt
find "$dest/results-tmp" -name "*$date*_gift.txt" | xargs cat >> $dest/"$date"_gift.txt
find "$dest/results-tmp" -name "*$date*_u2u.txt" | xargs cat >> $dest/"$date"_u2u.txt
find "$dest/results-tmp" -name "*$date*_uenter.txt" | xargs cat >> $dest/"$date"_uenter.txt
find "$dest/results-tmp" -name "*$date*_new_user.txt" | xargs cat >> $dest/"$date"_new_user.txt

rm -rf "$dest/splits"
rm -rf "$dest/results-tmp"