from llvm_ir_dataset_utils.util.bitcode_module import get_fields_total_counts
import argparse

parser = argparse.ArgumentParser(
    description="Process a bitcode file and print field counts.")
parser.add_argument('filename', type=str,
                    help="Path to the bitcode (.bc) file.")

print(', '.join(get_fields_total_counts(
    open(parser.parse_args().filename, "rb").read())))
