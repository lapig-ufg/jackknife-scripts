#!/bin/bash
#
#SBATCH --job-name=run_bfast_monitor_from_shape.R
#SBATCH --output=result-bfast-monitor-from-CSV-teste-700.csv
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-10
#SBATCH --open-mode=append
#SBATCH --ntasks=1

# Shape = 368919 coords -> array = 3690

# Run bfast script with array args
Rscript run_bfastMonitor_from_CSV.R $SLURM_ARRAY_TASK_ID

wait