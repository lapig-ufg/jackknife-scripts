#!/usr/bin/env /opt/anaconda/bin/python

import sys
import rsgislib
from rsgislib import imageutils

imgListParam = sys.argv[1];
imgBandsParam = sys.argv[2];
outputImageParam = sys.argv[3];

imageList = imgListParam.split(',')
bandNamesList = imgBandsParam.split(',')

outputImage = outputImageParam

gdalFormat = 'GTiff'
dataType = rsgislib.TYPE_32FLOAT

rsgislib.imageutils.stackImageBands(imageList, bandNamesList, outputImage, None, 0, gdalFormat, dataType)