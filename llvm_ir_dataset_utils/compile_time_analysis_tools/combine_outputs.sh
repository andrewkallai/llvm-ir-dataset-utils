#!/bin/bash
set -o errexit
#Usage:
#./combine_outputs.sh <language> [storage]

if [ -z "$1" ]; then
  echo "Missing language argument."
  exit 1
else
  LANGUAGE="$1"
fi

if [ -z "$2" ]; then
  STORAGE="/tmp"
else
  STORAGE="$2"
fi


cd ${STORAGE}

echo "file, text_segment_size" \
  > ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv
echo "file, instructions" \
  > ${LANGUAGE}/results/${LANGUAGE}_instructions.csv
for ps in ${LANGUAGE}/ps_*; do 
  cat ${ps}/text_segments.csv \
    >> ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv
  cat ${ps}/instructions.csv \
    >> ${LANGUAGE}/results/${LANGUAGE}_instructions.csv
done
sort -nk1.5 ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv \
  -o ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv
sort -nk1.5 ${LANGUAGE}/results/${LANGUAGE}_instructions.csv \
  -o ${LANGUAGE}/results/${LANGUAGE}_instructions.csv
awk -F, 'NR==FNR{a[NR]=$1","$2; next} {print a[FNR], $2}' \
  OFS=, ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv \
  ${LANGUAGE}/results/${LANGUAGE}_instructions.csv \
  > ${LANGUAGE}/results/${LANGUAGE}_combined_results.csv
sed -n -i '/, ,/!p' ${LANGUAGE}/results/${LANGUAGE}_combined_results.csv
rm ${LANGUAGE}/results/${LANGUAGE}_instructions.csv \
  ${LANGUAGE}/results/${LANGUAGE}_text_segments.csv 
rm -r ${LANGUAGE}/ps_*

