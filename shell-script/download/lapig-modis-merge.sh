#!/bin/bash

. lapig-modis-commons.sh $@

cd $SCRIPT_DIR

for day in $(find -name "*.hdf" | cut -d. -f3 | cut -b6- | sort | uniq); do
	
	mosaik_filelist="$MODIS_PRODUCT_NAME-$day.list"
	
	find -name "$MODIS_PRODUCT_NAME*$day*hdf" > $mosaik_filelist
	bandsNumber=$(head -n1 $mosaik_filelist | xargs gdalinfo | grep '.*SUBDATASET.*NAME=.*' | wc -l)

	for i in $(seq $bandsNumber); do

		bandName=$(echo $MODIS_PRODUCT_BANDS | cut -d, -f$i)
		
		mosaik_hdf_output="$MODIS_PRODUCT_NAME-$day-$i"
		mosaik_tif_output=$mosaik_hdf_output".lapig.tif"

		subset=$(for j in $(seq $bandsNumber); do [[ $i == $j ]] && echo -n "1 " || echo -n "0 "; done)

		echo $mosaik_hdf_output $mosaik_tif_output
		modis_mosaic.py -m $MRT_DIR -s "$subset" -o $mosaik_hdf_output $mosaik_filelist
		modis_convert.py -m $MRT_DIR -s "( 1 )" -o $mosaik_tif_output $mosaik_hdf_output.hdf


		rm  $mosaik_hdf_output.hdf $mosaik_hdf_output.hdf.xml $mosaik_hdf_output_mrt_resample.conf

	done

	rm $mosaik_filelist
done

rm *.txt *.log

mkdir tiles
mv *.hdf *.hdf.xml tiles

#gdal_translate -co TILED=YES -co COMPRESS=lzw -ot Int16 MOD09Q1-B01-049.sur_refl_b01.tif MOD09Q1-B01-049.sur_refl_b01-2.tif