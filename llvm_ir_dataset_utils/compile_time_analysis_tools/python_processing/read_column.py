# -*- coding: ascii -*-
import csv


def open_and_load(lang: str, STORAGE: str = '/tmp') -> [int]:
    '''
    Function to read csv files containing text segment size and instruction counts data.
    '''
    textseg_data: [int] = []
    inst_data: [int] = []
    with open(STORAGE+lang+"_combined_results.csv", mode='r', newline='') as file:
        for x in csv.DictReader(file):
            textseg_data.append(int(x[" text_segment_size"]))

            inst_data.append(int(x[" instructions"]))
    return textseg_data, inst_data
