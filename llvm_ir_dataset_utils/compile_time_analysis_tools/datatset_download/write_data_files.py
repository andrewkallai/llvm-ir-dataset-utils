"""Script to write ir dataset files to a storage location.

First the index counts for each language are written to a file "indices.csv".
Then each bitcode file is written to the specified storage location, from which
the files can be written to a tar file.
"""

from datasets import load_dataset, parallel
from os import makedirs
import multiprocessing
import csv
import argparse

parser = argparse.ArgumentParser(
    description="Configure path to store bitcode files, and configure batch size.")
parser.add_argument('storage', type=str,
                    help='Path to the storage location.')
parser.add_argument('-b', '--batchsize', nargs='?', type=int, default=15000,
                    help='Number of files to be written per pool of threads. Default value is 15000.')
args = parser.parse_args()


def write_dataset_files_and_index_info() -> None:
    STORAGE: str = args.storage
    BATCH_SIZE: int = args.batchsize

    def write_file(index: [int], bytes_and_dir: (bytes, str)):
        filename = f'{bytes_and_dir[1]}/file{index+1}.bc'
        with open(filename, 'wb') as file:
            file.write(bytes_and_dir[0])

    with parallel.parallel_backend('spark'):
        dataset = load_dataset('llvm-ml/ComPile', split='train', num_proc=2)

    lang_list: [str] = dataset["language"]
    langs = dataset.unique("language")
    file_indices: [dict] = []

    for i in range(0, len(langs)):
        start_index = lang_list.index(langs[i])
        if (i+1 != len(langs)):
            end_index = lang_list.index(langs[i+1])
        else:
            end_index = len(lang_list)
        file_indices.append(
            {"language": langs[i], "start_index": start_index, "end_index": end_index})
        with open('indices.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "language", "start_index", "end_index"], dialect='unix', quoting=csv.QUOTE_NONE)
            writer.writeheader()
            writer.writerows(file_indices)

    pool = multiprocessing.pool.ThreadPool(
        processes=multiprocessing.cpu_count())

    for i in range(0, len(file_indices)):
        start_index = file_indices[i]["start_index"]
        end_index = file_indices[i]["end_index"]
        for j in range(start_index, end_index, BATCH_SIZE):
            dir_name = f'{STORAGE}/{file_indices[i]["language"]}/{j}_temp'
            makedirs(dir_name, exist_ok=True)
            bytes_enumeration = enumerate(
                [(bytes_item, dir_name) for bytes_item in dataset[j:j+BATCH_SIZE if (j+BATCH_SIZE <= end_index) else end_index]['content']], start=j)
            pool.starmap(write_file, bytes_enumeration)

    pool.close()


if __name__ == '__main__':
    write_dataset_files_and_index_info()
