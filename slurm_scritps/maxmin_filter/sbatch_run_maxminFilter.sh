#!/bin/bash
#
#SBATCH --job-name=maxminFilter
#SBATCH --output=out_slurm_job/maxminFilter-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-234
#SBATCH --ntasks=1

Rscript maxminFilter_on_grid.R $SLURM_ARRAY_TASK_ID

wait