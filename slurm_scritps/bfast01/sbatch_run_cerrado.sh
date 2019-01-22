#!/bin/bash
#
#SBATCH --job-name=bfast_cerrado
#SBATCH --output=bfast_cerrado-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-100
#SBATCH --ntasks=1

# 3634 * 3 = 10902

COL_OFFSET=3500
ROW_OFFSET=6500
COL_SIZE=6
ROW_SIZE=100
#ROW_SIZE=9100

COL_OFFSET=$(( ($SLURM_ARRAY_TASK_ID-1)*COL_SIZE + $COL_OFFSET ))

Rscript run.R $COL_OFFSET $ROW_OFFSET $COL_SIZE $ROW_SIZE

wait