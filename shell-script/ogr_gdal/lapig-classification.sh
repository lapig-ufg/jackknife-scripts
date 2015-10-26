#!/bin/bash

TMP_DIR='/data/tmpfs'

GRID_SHP='/data/lapig/GEO/SHP/Cenas_Landsat_BR.shp'
GRID_LAYER=$(basename $GRID_SHP | cut -d. -f1)

SAMPLES_SHP='/data/lapig/GEO/SHP/MT/training-dataset.shp'
SAMPLES_LAYER='training-dataset'
SAMPLES_CLASS_ATTR="CLASSE_ID2"

PATHTILE="228"
ROW="68
"
GAPFILL="0"

GRID_FIDS=$(ogrinfo -geom=NO -sql "SELECT FID FROM $GRID_LAYER WHERE SPRNOME = '$PATHTILE/$ROW'" "$GRID_SHP" | grep 'FID' | cut -d' ' -f6)

NULL_VALUES='0'
TILE_FILE_NAME=$PATHTILE"_"$ROW"_"$GAPFILL
MULTIBAND_RASTER="/data/lapig/DEV/python/mosaik/$TILE_FILE_NAME.tif"

GRID_STATS_LAYER="grid_stats"
GRID_STATS_SHP="$TMP_DIR/$GRID_STATS_LAYER.shp"

for fid in $GRID_FIDS; do 
#for fid in $(echo 12 14 19 22 30 43 45 46); do 

	tmp_samples_layer=$PATHTILE"0"$ROW"_TRAINNING"
	tmp_samples_shp="$tmp_samples_layer.shp"
	tmp_samples_regex="$tmp_samples_layer.*"

	tmp_fid_layer="grid_fid_$fid"
	tmp_fid_shp="$TMP_DIR/$tmp_fid_layer.shp"
	tmp_fid_regex="$TMP_DIR/$tmp_fid_layer.*"

	ogr2ogr -sql "SELECT * FROM $GRID_LAYER WHERE FID = '$fid'" "$tmp_fid_shp" "$GRID_SHP"

	echo "Cliping samples vector layer (Grid fid $fid)"
	ogr2ogr -progress -clipsrclayer "$tmp_fid_layer" -clipsrc "$tmp_fid_shp" "$tmp_samples_shp" "$SAMPLES_SHP"
<<end_long_comment
	echo "Start fid $fid $(date)"
	tmp_raster="$TMP_DIR/multiband_raster_$fid.tif"
	tmp_raster_output="$TMP_DIR/multiband_raster_"$fid"_garsect.tif"
	tmp_raster_output_b2="$TMP_DIR/multiband_raster_"$fid"_garsect_b2.tif"
	
	echo $tmp_raster_output
	echo $tmp_raster_output_b2

	tmp_samples_layer="samples_$fid"
	tmp_samples_shp="$TMP_DIR/$tmp_samples_layer.shp"
	tmp_samples_regex="$TMP_DIR/$tmp_samples_layer.*"

	tmp_fid_layer="grid_fid_$fid"
	tmp_fid_shp="$TMP_DIR/$tmp_fid_layer.shp"
	tmp_fid_regex="$TMP_DIR/$tmp_fid_layer.*"
	
	tmp_garsect2_output="$TMP_DIR/garsect_$fid.out"

	ogr2ogr -sql "SELECT * FROM $GRID_LAYER WHERE FID = '$fid'" "$tmp_fid_shp" "$GRID_SHP"

	echo "Cropping  multiband raster layer (Grid fid $fid)"
	gdalwarp -dstnodata "$NULL_VALUES" -co TILED=YES -co BIGTIFF=YES -crop_to_cutline -overwrite -multi -cutline "$tmp_fid_shp" "$MULTIBAND_RASTER" "$tmp_raster"

	echo "Cliping samples vector layer (Grid fid $fid)"
	ogr2ogr -progress -clipsrclayer "$tmp_fid_layer" -clipsrc "$tmp_fid_shp" "$tmp_samples_shp" "$SAMPLES_SHP"

	garsect2.py -p 5 -r "$tmp_raster" -v "$tmp_samples_shp" --stats --crossval -a "$SAMPLES_CLASS_ATTR" -m "$NULL_VALUES" -b 1 2 3 4 6 8 &> $tmp_garsect2_output
	
	totalSamples=$(ogrinfo -sql "SELECT COUNT(*) as contagem FROM $tmp_samples_layer" $tmp_samples_shp | grep "contagem (Integer)" | cut -d' ' -f6)
	meanProd=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Mean producer's accuracy" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	meanCons=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Mean consumer's accuracy" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	overall=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Overall accuracy" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	misclass=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Max misclassified" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	kappa=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Kappa coefficient" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	crossValAcc=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Mean out-of-sample accuracy" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)
	crossValKappa=$(head -n $(($(cat $tmp_garsect2_output | grep -n "Mean out-of-sample Kappa" | cut -d: -f1)+1)) $tmp_garsect2_output | tail -n1)

	sqlStat="SELECT *, $meanProd as meanProd, $meanCons as meanCons, $overall as overall, $misclass as misclass, $kappa as kappa, $totalSamples as totalSam, $crossValAcc as crAcc, $crossValKappa as crKap FROM $GRID_LAYER WHERE FID = '$fid'"
	ogr2ogr -update -append $GRID_STATS_SHP $GRID_SHP -sql "$sqlStat" -nln $GRID_STATS_LAYER


	echo "Classification stats:"
	echo "	Mean producer's accuracy: $meanProd"
	echo "	Mean consumer's accuracy: $meanCons"
	echo "	Overall accuracy: $overall"
	echo "	Max misclassified: $misclass"
	echo "	Kappa coefficient: $kappa"
	echo "	Total samples: $totalSamples"
	echo "	Mean out-of-sample accuracy (Cross Validation): $crossValAcc"
	echo "	Mean out-of-sample Kappa (Cross Validation): $crossValKappa"

	echo "Extract band 2"
	gdal_translate -b 2 -co COMPRESS=lzw -co INTERLEAVE=BAND -co TILED=YES -ot Int16 $tmp_raster_output $tmp_raster_output_b2

	echo "Remove temp files"
	rm -v $tmp_samples_regex $tmp_fid_regex $tmp_raster $tmp_raster_output

	mv $tmp_raster_output_b2 $tmp_raster_output

	
	echo "End fid $fid $(date)"
end_long_comment
done