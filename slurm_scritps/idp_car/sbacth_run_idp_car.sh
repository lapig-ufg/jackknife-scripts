#!/bin/bash
#
#SBATCH --job-name=idp_car_2010
#SBATCH --output=/data/DADOS_GRID/DATASAN/idp_car/result_idp_car_2010.csv
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-9000
#SBATCH --open-mode=append
#SBATCH --ntasks=1

# total 810527

# hostname
# date

N_ROWS_PER_NODE=100
N_PROCESS=4

START_ROW=0
END_ROW=$N_ROWS_PER_NODE


START_N_START_ROW=$(( ($SLURM_ARRAY_TASK_ID-1)*$N_ROWS_PER_NODE + $START_ROW ))

END_NUM=$(( $SLURM_ARRAY_TASK_ID * $N_ROWS_PER_NODE ))


THREAD_SIZE=$(( ($END_NUM - $START_N_START_ROW) / $N_PROCESS ))

for (( i=0; i<$N_PROCESS; i++ )); do

	python3 /data/DADOS_GRID/DATASAN/idp_car/idp_car.py $(($START_N_START_ROW + ($i*THREAD_SIZE) )) $THREAD_SIZE &

done


wait