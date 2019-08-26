#!/bin/bash
#
#SBATCH --job-name=rpd_detect_brasil
#SBATCH --output=out/rpd_detect_brasil-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-4000
#SBATCH --ntasks=1

hostname

Rscript rpd_detect_brasil.R $SLURM_ARRAY_TASK_ID

# echo "$SLURM_ARRAY_TASK_ID"

wait