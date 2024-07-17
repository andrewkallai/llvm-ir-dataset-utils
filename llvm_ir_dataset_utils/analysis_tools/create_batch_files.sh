#!/bin/bash

STORAGE="/lustre/schandra_crpl/users/3302/ir_bc_files/"
BATCH_PATH="/home/3302/hf_py_code/compile/codes/batch_jobs/makefile_dir/"

lang=("c" "cpp" "julia" "rust" "swift")
array1=(0 31653 87225 144641 353700)
sizes=(31653 55572 57416 209059 49051)

length=${#lang[@]}

for (( i=0; i<$length; i++ ))
do
  js="${lang[$i]}_batch.sh"
  cp job_template.sh $js
  echo "#SBATCH --output=${STORAGE}${lang[$i]}/job_results/slurm-%A_%a.out" >> $js
  
  echo "#SBATCH --error=${STORAGE}${lang[$i]}/job_results/slurm-%A_%a.out" >> $js
  
  echo "START=${array1[$i]}" >> $js
  echo "TYPE=${lang[$i]}" >> $js
  echo "SIZE=${sizes[$i]}" >> $js
  echo "STORAGE=${STORAGE}" >> $js
  echo "BATCH_PATH=${BATCH_PATH}" >> $js
  cat batch_main_body.sh >> $js
  chmod 744 $js
done

