# -*- coding: ascii -*-
from datasets import load_dataset, parallel
import os
import multiprocessing
import csv
from sys import argv

# Usage:
# python write_data_files.py [STORAGE]

STORAGE: str
if len(argv) > 1:
    STORAGE = argv[1]
else:
    STORAGE = '/tmp'

lang_list: [str]
global j
global dir_name
j: int
dir_name: str
BATCH_SIZE: int = 15000
file_indices: [dict] = []


def write_file(index: [int], bytes_item: [bytes]):
    filename = f'{dir_name}/file{index+j+1}.bc'
    with open(filename, 'wb') as file:
        file.write(bytes_item)


with parallel.parallel_backend('spark'):
    dataset = load_dataset('llvm-ml/ComPile', split='train', num_proc=2)

lang_list = dataset["language"]
langs = dataset.unique("language")
pool = multiprocessing.pool.ThreadPool(processes=multiprocessing.cpu_count())

for i in range(0, len(langs)):
    start_index = lang_list.index(langs[i])
    if (i+1 != len(langs)):
        end_index = lang_list.index(langs[i+1])
    else:
        end_index = len(lang_list)
    file_indices.append(
        {"language": langs[i], "start_index": start_index, "end_index": end_index})
    for j in range(start_index, end_index, BATCH_SIZE):
        dir_name = os.path.join(STORAGE, f'{STORAGE}/{langs[i]}/{j}_temp')
        os.makedirs(dir_name, exist_ok=True)
        bytes_enumeration = enumerate(
            dataset[j:j+BATCH_SIZE if (j+BATCH_SIZE <= end_index) else end_index]['content'])
        pool.starmap(write_file, bytes_enumeration)

pool.close()

with open('indices.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=[
                            "language", "start_index", "end_index"], dialect='unix', quoting=csv.QUOTE_NONE)
    writer.writeheader()
    writer.writerows(file_indices)
