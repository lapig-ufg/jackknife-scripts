#!/bin/bash

for i in $(seq 20 5 49); do
	
	teste=''
	for j in $(seq $i $(($i + 4))); do
		teste="$teste $j"
		echo $j "/data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_"$j"_01_10/CLASSIFICATION/227067_CLASSIFICATION.tif"
		#gdal_calc.py -A input.tif -B input2.tif --outfile=result.tif --calc="(A+B)/2"
	done

	#echo $teste
done