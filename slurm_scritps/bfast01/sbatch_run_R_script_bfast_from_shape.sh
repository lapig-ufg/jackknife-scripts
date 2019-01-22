#!/bin/bash
#
#SBATCH --job-name=run_bfast_from_shape.R
#SBATCH --output=tarefa-run-teste100.csv
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-566
#SBATCH --open-mode=append
#SBATCH --ntasks=1

# Number of coordinates to execute per node
N_COODS_PER_NODE=100

# Calc the START and end END indexes for the Rscript range args
START_INDEX=$(( ($SLURM_ARRAY_TASK_ID - 1) * N_COODS_PER_NODE + 1 ))
END_INDEX=$(($START_INDEX + N_COODS_PER_NODE-1))

# Run bfast script with range args
Rscript run_bfast_from_shape.R $START_INDEX $END_INDEX

wait