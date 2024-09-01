"""Script to write ir dataset files to a specified storage location.

In write_dataset_files_and_index_info, the index counts for each language are written to a file "indices.csv".
Then each bitcode file is written using available threads into a tar file corresponding to the IR language.


get_args
  Returns: argparse.Namespace
  Example usage: get_args()

write_dataset_files_and_index_info
  Returns: None
  Example usage: write_dataset_files_and_index_info("/tmp")
"""


def get_args():
  import argparse

  parser = argparse.ArgumentParser(
      description="Configure path to store bitcode files, and configure batch size."
  )
  parser.add_argument('storage', type=str, help='Path to the storage location.')
  parser.add_argument(
      '-b',
      '--batchsize',
      nargs='?',
      type=int,
      default=15000,
      help='Number of files to be written per pool of threads. Default value is 15000.'
  )
  return parser.parse_args()


def write_dataset_files_and_index_info(storage: str) -> None:
  from datasets import load_dataset, parallel
  from os import makedirs, listdir
  import threading
  import csv
  import tarfile
  from io import BytesIO
  from time import time

  def create_tar(dataset_subset, start_index: int, dir_name: str,
                 language: str):
    with tarfile.open(dir_name + '/' + language + '_bc_files.tar', 'a:') as tar:
      for x in enumerate((dataset_subset[i]["content"]
                          for i in range(0, dataset_subset.num_rows))):
        tarinfo = tarfile.TarInfo(name=f'bc_files/file{x[0]+1+start_index}.bc')
        file_obj = BytesIO(x[1])
        tarinfo.size = file_obj.getbuffer().nbytes
        tarinfo.mtime = time()
        tar.addfile(tarinfo, fileobj=file_obj)

  with parallel.parallel_backend('spark'):
    dataset = load_dataset('llvm-ml/ComPile', split='train', num_proc=2)

  lang_list: [str] = dataset["language"]
  langs = dataset.unique("language")
  file_indices: [dict] = []

  for i in range(0, len(langs)):
    start_index = lang_list.index(langs[i])
    if (i + 1 != len(langs)):
      end_index = lang_list.index(langs[i + 1])
    else:
      end_index = len(lang_list)
    file_indices.append({
        "language": langs[i],
        "start_index": start_index,
        "end_index": end_index
    })
    with open('indices.csv', mode='w', newline='') as file:
      writer = csv.DictWriter(
          file,
          fieldnames=["language", "start_index", "end_index"],
          dialect='unix',
          quoting=csv.QUOTE_NONE)
      writer.writeheader()
      writer.writerows(file_indices)

  threads = []
  for i in range(0, len(file_indices)):
    start_index = file_indices[i]["start_index"]
    end_index = file_indices[i]["end_index"]
    dir_name = f'{storage}/{file_indices[i]["language"]}'
    makedirs(dir_name, exist_ok=True)
    thread = threading.Thread(
        target=create_tar,
        args=(dataset.select(range(start_index, end_index)), start_index,
              dir_name, file_indices[i]["language"]))
    threads.append(thread)
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()


if __name__ == '__main__':
  args = get_args()
  write_dataset_files_and_index_info(storage=args.storage)
