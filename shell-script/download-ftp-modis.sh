#!/bin/bash

BASE_URL="http://e4ftl01.cr.usgs.gov/MOLT"
PRODUCT="MOD17A2H.006"
TILES="h13v11\|h12v08\|h14v09\|h14v10\|h13v12\|h10v09\|h11v08\|h11v09\|h11v10\|h12v11\|h13v08\|h12v09\|h12v10\|h14v11\|h13v09\|h13v10"

URL="$BASE_URL/$PRODUCT/"

for path in $(curl -s $URL | grep -o ">[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]" | cut -b2- ); do
	for file in $(curl -Ls "$URL$path" | grep $TILES | grep -o [hdf\|xml\|jpg]\"\>.*[hdf\|xml\|jpg] | cut -b4-); do
		echo "$URL$path/$file"
	done
done