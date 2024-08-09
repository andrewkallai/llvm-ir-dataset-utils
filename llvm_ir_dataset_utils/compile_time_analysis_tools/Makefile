SHELL := /bin/bash

WILD := $(shell echo {$(begin)..$(end)})

ifneq ($(CC), clang)
  $(warning WARNING: SETTING CC TO clang OR clang++)
  override CC := clang
  ifeq ($(lang), cpp)
  override CC := clang++ 
  endif
endif

all: $(WILD) 

$(WILD):
	@perf stat --no-big-num -e instructions:u -o \
		$(lang)/perf_stat_files/file$@.txt \
		$(CC) -O3 -c $(lang)/bc_files/file$@.bc \
		-o $(lang)/object_files/file$@.o
	@instruct=$$(awk '/instructions/ {print $$1}' \
		$(lang)/perf_stat_files/file$@.txt); \
		echo "file$@, $$instruct" >> $(lang)/instruction_counts/inst$@.csv
	@size=$$(llvm-size $(lang)/object_files/file$@.o | awk 'NR==2 {print $$1}'); \
		echo "file$@, $$size" >> $(lang)/textseg_sizes/textseg$@.csv

