#!/bin/bash
set -o errexit

#USAGE
#./create_batch_files.sh <STORAGE_PATH> <MAKEFILE_PATH>

if [ -z "$1" ]; then
  STORAGE="/tmp"
else
  STORAGE="$1"
fi
if [ -z "$2" ]; then
  MAKE_PATH=".."
else
  MAKE_PATH="$2"
fi

lang=()
start_ids=()
sizes=()

while IFS=',' read -r language start_index end_index; do
  lang+=($language)
  start_ids+=($start_index)
  sizes+=($((${end_index}-${start_index})))
done < <(tail -n +2 "../dataset_download/indices.csv")

length=${#lang[@]}

for (( i=0; i<$length; i++ ))
do
  js="${lang[$i]}_batch.sh"
  cp job_template.sh $js
  echo "#SBATCH --output=${STORAGE}/${lang[$i]}/job_results/slurm-%A_%a.out" >> $js

  echo "#SBATCH --error=${STORAGE}/${lang[$i]}/job_results/slurm-%A_%a.out" >> $js

  echo "START=${start_ids[$i]}" >> $js
  echo "TYPE=${lang[$i]}" >> $js
  echo "SIZE=${sizes[$i]}" >> $js
  echo "STORAGE=${STORAGE}" >> $js
  echo "MAKE_PATH=${MAKE_PATH}" >> $js
  cat batch_main_body.sh >> $js
  chmod 744 $js
done

