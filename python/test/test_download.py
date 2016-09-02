#!/usr/bin/python

import ee

from lapig.ee import download
from datetime import datetime

start = datetime(2014, 12, 01);
end = datetime(2014, 12, 31);
bbox = { 'x1': -54.2505, 'y1': -19.6136, 'x2': -45.5273,  'y2': -12.3744 };
outputName = 'landsat-8-go';

ee.Initialize();
img = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate(start, end).mean();

download.eeImage(img, 30, 'EPSG:4326', bbox, outputName);