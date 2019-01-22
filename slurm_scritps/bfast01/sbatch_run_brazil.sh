#!/bin/bash
#
#SBATCH --job-name=bfast_brazil
#SBATCH --output=out_bfast_brazil/bfast_brazil-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-3731
#SBATCH --ntasks=1

# --array=1-3731
# Size is 21592, 18660
#	 -->  21591, 18659

# Rscript START_ROW(max 18659) START_COL END_ROW END_COL(max 21591)
# Rscript run.R 18659 1 1 21591


# START_ROW (Linha de começo da execução até a END_ROW)
# END_ROW (FIXO, quantas serão processadas a partir da START_ROW)

# START_COL (Coluna inicial da matriz da imagem)
# END_COL   (Coluna final da matriz imagem)

# Example:
# START_ROW 	START_COL 	END_ROW 	END_COL
#    12		        1	       5		 21591

# N_ROWS_PER_NODE (Número de linhas da imagem que serão processadas por cada Nó do cluster a cada task)

hostname

N_ROWS_PER_NODE=5

START_ROW=1
START_COL=1
END_ROW=$N_ROWS_PER_NODE
END_COL=21591


START_N_START_ROW=$(( ($SLURM_ARRAY_TASK_ID-1)*$N_ROWS_PER_NODE + $START_ROW ))

END_NUM=$(( $SLURM_ARRAY_TASK_ID * $N_ROWS_PER_NODE ))

echo "This is task $SLURM_ARRAY_TASK_ID, which will do runs $START_N_START_ROW to $END_NUM"

# echo "$START_N_START_ROW $START_COL $END_ROW $END_COL"

Rscript run_bfast_brazil.R $START_N_START_ROW $START_COL $END_ROW $END_COL

wait