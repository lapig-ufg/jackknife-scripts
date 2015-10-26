#!/bin/bash

TRAINNING_DIR='/data/lapig/GEO/CLASSIFICATION/PASTURE/INPUT/TRAINNING/DATASET_02/'
cd "$TRAINNING_DIR"

count=1

for shp in $( find *.shp ); do 
	layername=$(echo $shp | cut -d. -f1)
	outputFile=$(echo $shp | cut -c-6 | uniq | sed 's/\_/0/')_TRAINNING.shp

	echo $shp $outputFile $classId 
	
	sqlNoPasture="SELECT \"1\" as CLASS_ID FROM \"$layername\" WHERE \"Classe_Uso\" <> 'Pastagem'"
	sqlPasture="SELECT \"2\" as CLASS_ID FROM \"$layername\" WHERE \"Classe_Uso\" = 'Pastagem'"

	ogr2ogr -update -append -sql "$sqlNoPasture" $outputFile $shp
	ogr2ogr -update -append -sql "$sqlPasture" $outputFile $shp

done