#!/bin/bash
#
#SBATCH --job-name=br_AnomalyTrend_2011_2017
#SBATCH --output=out/Monitoring_br_AnomalyTrend_2011_2017-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-3733
#SBATCH --ntasks=1

hostname

Rscript br_AnomalyTrend_2011_2017.R $SLURM_ARRAY_TASK_ID

#echo "$SLURM_ARRAY_TASK_ID"

wait