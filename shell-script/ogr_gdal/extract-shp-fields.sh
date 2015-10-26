#!/bin/bash

for shp in $(find -name '*.shp'); do
	layer=$(basename $shp | cut -d. -f1)
	for field in $(ogrinfo -q -geom=NO -fid 0 $shp $layer | grep '=' | cut -d\( -f1 | sed 's,^ *,,; s, *$,,'); do
		echo -e "$field\t$layer\t$shp"
	done
done