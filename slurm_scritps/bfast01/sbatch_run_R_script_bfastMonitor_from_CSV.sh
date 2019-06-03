#!/bin/bash
#
#SBATCH --job-name=run_bfast_monitor_from_shape.R
#SBATCH --output=result-bfast-monitor-Pontos_Faltando.csv
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-1953
#SBATCH --open-mode=append
#SBATCH --ntasks=1

# CSV with 9699 points
# 1953 faltando

# Run bfast script with array args
Rscript run_bfastMonitor_from_CSV.R $SLURM_ARRAY_TASK_ID

wait