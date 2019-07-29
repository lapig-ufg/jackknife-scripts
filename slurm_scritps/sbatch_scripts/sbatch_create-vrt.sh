#!/bin/bash
#
#SBATCH --job-name=create-vrt
#SBATCH --output=create-vrt-%a.out
#SBATCH --partition=GRID-ALL
#SBATCH --array=1-32

## Create VRT file

YEARS=(1986L5 1987L5 1988L5 1989L5 1990L5 1991L5 1992L5 1993L5 1994L5 1995L5 1996L5 1997L5 1998L5 1999L5 2000L7 2001L7 2002L7 2003L5 2004L5 2005L5 2006L5 2007L5 2008L5 2009L5 2010L5 2011L5 2012L7 2013L8 2014L8 2015L8 2016L8 2017L8)
YEAR_INDEX=$(($SLURM_ARRAY_TASK_ID -1))
JOB_YEAR=${YEARS[$YEAR_INDEX]}

#branch teste

BASE_DIR="/data/DADOS_GRID/pasture_mapbiomas_col3/mosaic_planted_filtered"
BR_EXTENT="-73.9916248 -33.0001510 -34.9860565 6.0000274"

gdalbuildvrt -te $BR_EXTENT $BASE_DIR/$JOB_YEAR.vrt $BASE_DIR/$JOB_YEAR/*.tif