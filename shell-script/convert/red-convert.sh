#!/bin/bash

IFS="
"

PROJ="epsg:4674"
SRC="/data/lapig/TMP/PASTAGEM.ORG/Categorias/Vegetação/pa_br_red_250_lapig_old/"
DST="/data/lapig/TMP/PASTAGEM.ORG/Categorias/Vegetação/pa_br_red_250_lapig/"

cd $SRC
#rm -vR *.xml *.html *.tfw *.htm *.ovr Thumbs.db
for file in $(find -iname "RED_BRASIL_*.tif"); do
	year=$(echo $file | cut -d_ -f3)
	day=$(echo $file | cut -d_ -f4 | cut -d. -f1)
	new_file=pa_br_red_250_"$year$day"_lapig.tif
	echo $new_file
	gdal_translate -a_nodata 0 -co COMPRESS=deflate -co INTERLEAVE=BAND -co TILED=YES -a_srs $PROJ $file $DST$new_file
done

# mv pa_br_lst_day_250_2000_273_lapig.tif pa_br_lst_day_250_2001_105_lapig.tif ../