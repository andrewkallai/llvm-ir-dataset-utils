BATCH=$(($SIZE/$SLURM_ARRAY_TASK_MAX))
I=$((${SLURM_ARRAY_TASK_ID}*${BATCH}+1+${START}))
STOP=$(($I+${BATCH}-1))
if [ $SLURM_ARRAY_TASK_ID -eq $SLURM_ARRAY_TASK_MAX ]; then
  STOP=$(($I+${SIZE}%$BATCH-1))
fi
cd $TMPDIR
mkdir -p ir_bc_files/ps_$I/${TYPE}
cd ir_bc_files/ps_$I/${TYPE}
mkdir -p bc_files instruction_counts perf_stat_files \
textseg_sizes object_files
eval tar --extract --file=${STORAGE}${TYPE}/${TYPE}_bc_files.tar \
bc_files/file{$I..$STOP}.bc
cd $TMPDIR/ir_bc_files/ps_$I
make -f ${BATCH_PATH}no_ignore_error_makefile \
-j 64 lang="${TYPE}" begin="$I" \
end="$STOP"
mkdir -p ${STORAGE}${TYPE}/ps_$I
 > ${STORAGE}${TYPE}/ps_$I/text_segments.csv

 > ${STORAGE}${TYPE}/ps_$I/instructions.csv

eval cat ${TYPE}/textseg_sizes/textseg{$I..$STOP}.csv \
>> ${STORAGE}${TYPE}/ps_$I/text_segments.csv
eval cat ${TYPE}/instruction_counts/inst{$I..$STOP}.csv \
>> ${STORAGE}${TYPE}/ps_$I/instructions.csv
cd ..
rm -r ps_$I

