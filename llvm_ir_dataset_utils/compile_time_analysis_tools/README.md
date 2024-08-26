### This README describes how to use the following tools and files: 

- SLURM_files/batch_main_body.sh
- SLURM_files/create_batch_files.sh
- SLURM_files/job_template.sh
- Makefile
- combine_outputs.sh
- write_ir_counts.py

**create_batch_files.sh** must be provided a storage argument, temporary directory argument, and a path to the relevant makefile (where Makefile is). Other configurable args are the number of threads used by the make command in the batch scripts, and the maximum number of SLURM jobs which a user can have in the SLURM queue.
When executed, settings will be configured for batch job scripts which are created in the format [language_extension]_batch.sh.
The content of those scripts is a combination of **job_template.sh** (form SLURM config) and **batch_main_body.sh** (for the main execution).

**write_ir_counts.py** is automatically used by **Makefile** to generate IR features count data for each IR module being processed. These counts are made using using the function llvm_ir_dataset_utils.util.bitcode_module.get_fields_total_counts.

**combine_outputs.sh** takes two args: <language_extension> and <storage_location>. The script combines all the temporary result folders made in <storage_location>/<language_extension>/. It removes the folders and creates temporary files from which the final csv files are constructed for the given language.
Current data collected includes text segment size, user CPU instruction counts during compile time, IR feature counts sourced from LLVM function_analysis_properties, and maximum relative time pass names and percentage counts.
