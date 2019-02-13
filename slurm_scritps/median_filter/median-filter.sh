#!/bin/bash
#
#SBATCH --job-name=median-filter
#SBATCH --output=out_slurm_job_median-filter/median-filter-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-1137
#SBATCH --ntasks=2

# ySize = 145446

ARRAY_BATCH_SIZE=128
ARRAY_START_INDEX=$((($SLURM_ARRAY_TASK_ID-1) * $ARRAY_BATCH_SIZE ))

TASK_BATCH_SIZE=$(($ARRAY_BATCH_SIZE / $SLURM_NTASKS))
START_INDEX_TASK=$ARRAY_START_INDEX

for TASK in $(seq 1 $SLURM_NTASKS); do
	
	START_INDEX_TASK=$START_INDEX_TASK
	END_INDEX_TASK=$(($START_INDEX_TASK + $TASK_BATCH_SIZE))
	
	python -u /data/DADOS_GRID/run_median_filter/mapbiomas_filter.py $START_INDEX_TASK $END_INDEX_TASK &
	#echo "$START_INDEX_TASK $END_INDEX_TASK"

	START_INDEX_TASK=$END_INDEX_TASK
done

wait