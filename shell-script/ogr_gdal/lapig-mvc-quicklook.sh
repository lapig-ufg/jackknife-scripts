#!/bin/bash

IMG="$1"
SHP="$2" #/data/lapig/GEO/SHP/es_mt_limite_estadual.shp

IMG_NAME=$(basename $IMG | rev | cut -b5- | rev)

gdal_translate -outsize 3% 3% $IMG $IMG_NAME".QUICKLOOK.TMP.tif"
gdalwarp -cutline $SHP $IMG_NAME".QUICKLOOK.TMP.tif" $IMG_NAME".QUICKLOOK.tif"

rm $IMG_NAME".QUICKLOOK.TMP.tif"