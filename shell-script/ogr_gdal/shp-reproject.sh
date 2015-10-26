#!/bin/bash

IFS="
"

PROJ="epsg:4674"
SRC="/data/lapig/TMP/PASTAGEM.ORG/Categorias/Desmatamento"

cd $SRC
for file in $(find -name "*.prj"); do
	if [[ -z $(cat $file | grep 'SIRGAS') ]]; then
		shpfile=$(echo $file | sed 's/\.prj/\.shp/g' )
		newShpfile=$(echo $file | sed 's/\.prj/\_sirgas.shp/g' )
		echo $shpfile $newShpfile
	fi
done