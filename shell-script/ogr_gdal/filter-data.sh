#!/bin/bash

for shp in $(find -name '*.shp'); do
	layername=$(basename $shp .shp)
	ogr2ogr -sql "SELECT * FROM $layername WHERE class_name NOT IN ('FLORESTA','FLORESTA_INUNDADA','HIDROGRAFIA','NAO_FLORESTA','NAO_FLORESTA2','NUVEM','RESIDUO','FLORESTA')" filter_$layername.shp $layername.shp
done