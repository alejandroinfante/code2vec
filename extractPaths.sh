#!/bin/bash
# database -- dataset -- target file name -- number of cores
PHARO_VM=PharoExtractor/pharo
TMP_NAME=`date +%s`
mkdir -p tmp/$TMP_NAME
FAIL=0

for i in `seq 1 $4`; do
	TMP_PATH[${i}]="tmp/${TMP_NAME}/${i}.tmp"
    $PHARO_VM --headless PharoExtractor/work.image extractFromDB $1 $2 $4 $i > ${TMP_PATH[${i}]} &
    pids[${i}]=$!
done

# wait for all pids
for pid in ${pids[*]}; do
    wait $pid || echo "Error on process $pid"
done

rm -f $3
touch $3

for tmp_file in ${TMP_PATH[*]}; do
	cat $tmp_file >> $3
done

rm -r tmp/$TMP_NAME