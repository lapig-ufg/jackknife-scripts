#!/bin/bash
#
#SBATCH --job-name=merge_br_AnomalyTrend_2011_2017
#SBATCH --output=out_merge/Monitoring_merge_br_AnomalyTrend_2011_2017-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-6
#SBATCH --ntasks=1

hostname

Rscript merge_br_AnomalyTrend_2011_2017.R $SLURM_ARRAY_TASK_ID

wait