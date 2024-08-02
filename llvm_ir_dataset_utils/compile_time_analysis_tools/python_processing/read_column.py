# -*- coding: ascii -*-
import csv

def open_and_load(lang: str)->[int]:
#  PREFIX:str="/home/3302/hf_py_code/compile/codes/results/"
  #PREFIX:str="/lustre/schandra_crpl/users/3302/ir_bc_files/"+lang+"/results/"
  PREFIX:str="/home/3302/hf_py_code/compile/csv_data/inst_scatterplots/"
  textseg_data: [int] = []
  inst_data: [int] = []
#  with open(PREFIX+lang+"_text_segments.csv", mode='r', newline='') as file:
  with open(PREFIX+lang+"_combined_results.csv", mode='r', newline='') as file:
    for x in csv.DictReader(file):
      textseg_data.append(int(x[" text_segment_size"]))
      
      inst_data.append(int(x[" instructions"]))
#  with open(PREFIX+lang+"_instructions.csv", mode='r', newline='') as file:
#    for x in csv.DictReader(file):
  return textseg_data, inst_data

