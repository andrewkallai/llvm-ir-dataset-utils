"""main function takes a bitcode filename as argment and prints the function analysis properties counts for that file.

If a valid bitcode file is provided as argument, the counts will be printed using llvm_ir_dataset_utils.compile_time_analysis_tools.write_ir_counts
If "/dev/null" is provided as argument, the Hugging Face IR dataset will be loaded and the loop will attempt to obtain the names of the function analysis properties field names from the first file by index.
"""
from llvm_ir_dataset_utils.util.bitcode_module import get_fields_total_counts
import argparse
from datasets import load_dataset, parallel


def main() -> None:
  parser = argparse.ArgumentParser(
      description="Process a bitcode file and print field counts.")
  parser.add_argument(
      'filename', type=str, help="Path to the bitcode (.bc) file.")
  filename = parser.parse_args().filename
  if (filename == "/dev/null"):
    with parallel.parallel_backend('spark'):
      dataset = load_dataset('llvm-ml/ComPile', split='train', num_proc=2)
    for i in range(0, dataset.num_rows):
      bc_file = dataset[i]["content"]
      output = get_fields_total_counts(bc_file, names=True)
      if (output != None):
        print(', '.join(output))
        break
  else:
    print(', '.join(get_fields_total_counts(open(filename, "rb").read())))


if __name__ == '__main__':
  main()
