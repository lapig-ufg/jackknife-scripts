#!/bin/bash
#
#SBATCH --job-name=bfast_brazil
#SBATCH --output=out_bfast_brazil/bfast_brazil-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-10
#SBATCH --ntasks=1

# --array=1-3731
# Size is 21592, 18660
#	 -->  21591, 18659

# Rscript COL_OFFSET(max 18659) ROW_OFFSET COL_SIZE ROW_SIZE(max 21591)
# Rscript run.R 18659 1 1 21591

hostname

N_ROWS_PER_NODE=5

COL_OFFSET=1
ROW_OFFSET=1
COL_SIZE=1
ROW_SIZE=21591

# COL_SIZE=1

START_N_COL_OFFSET=$(( ($SLURM_ARRAY_TASK_ID-1)*$N_ROWS_PER_NODE + $COL_OFFSET ))

END_NUM=$(( $SLURM_ARRAY_TASK_ID * $N_ROWS_PER_NODE ))

echo "This is task $SLURM_ARRAY_TASK_ID, which will do runs $START_N_COL_OFFSET to $END_NUM"

for (( run=$START_N_COL_OFFSET; run<=END_NUM; run++ )); do
  echo This is SLURM task $SLURM_ARRAY_TASK_ID, run number $run

  echo "$run $ROW_OFFSET $COL_SIZE $ROW_SIZE"

done


# Rscript run_bfast_brazil.R $COL_OFFSET $ROW_OFFSET $COL_SIZE $ROW_SIZE

# wait