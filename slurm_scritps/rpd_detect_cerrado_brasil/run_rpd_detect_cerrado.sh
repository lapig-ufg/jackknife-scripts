#!/bin/bash
#
#SBATCH --job-name=rpd_detect_cerrado
#SBATCH --output=out/rpd_detect_cerrado-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-2139
#SBATCH --ntasks=1

hostname

Rscript rpd_detect_cerrado.R $SLURM_ARRAY_TASK_ID

#echo "$SLURM_ARRAY_TASK_ID"

wait