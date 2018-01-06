#!/usr/bin/env bash

dir=$(dirname "$0")
repo=$1
date=$2

mkdir -p "$repo"

export PYTHONPATH="$dir/../"


rm -r "$repo/dates"
mkdir -p "$repo/dates"
python3 "$dir/../tool/lsoss.py" "$repo/dates" "$date"

bash "$dir/msg/raw2rds.sh" "$repo/parsed" "$repo/dates/$date.txt" "$date"

bash "$dir/spark/parse.sh" "$dir/gift.csv" "$repo/parsed" "$repo/etl" "$date"

python3 "$dir/warehouse/update.py" "$dir/gift.csv" "$repo/parsed/${date}_new_user.txt"

python3 "$dir/warehouse/facts.py" "$repo/etl" "$date"
