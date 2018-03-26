#!/bin/bash
gdalbuildvrt -separate -overwrite ./data/blue.vrt $(for file in $(find -name '*_01.vrt' | sort); do	echo $file; done)
gdalbuildvrt -separate -overwrite ./data/green.vrt $(for file in $(find -name '*_02.vrt' | sort); do	echo $file; done)
gdalbuildvrt -separate -overwrite ./data/red.vrt $(for file in $(find -name '*_03.vrt' | sort); do	echo $file; done)
gdalbuildvrt -separate -overwrite ./data/nir.vrt $(for file in $(find -name '*_04.vrt' | sort); do	echo $file; done)