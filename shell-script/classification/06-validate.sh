#!/bin/bash

#TILE="227067"

cp -v $TILE"_CLASSIFICATION_20.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R1_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R1' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R5.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R5_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R5' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R10.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R10_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R10' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R15.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R15_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R15' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R20.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R20_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R20' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R25.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R25_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R25' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points
cp -v $TILE"_CLASSIFICATION_R30.tif" /data/lapig/GEO/CLASSIFICATION/PASTURE/OUTPUT/01_R30_01_10/CLASSIFICATION/$TILE"_CLASSIFICATION.tif"; ./../../classification.py -t'R30' --no-classify --no-download -i $TILE -vp 1000 -tn 10 --prefetched-shp-random-points