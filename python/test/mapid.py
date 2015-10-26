#!/usr/bin/python

import ee
import ee.mapclient

from lapig.ee import mvc


ee.Initialize();

NDVI_PALETTE = 'ec1413, e8dfa0, 0aa73c';

lc8 = ee.ImageCollection("LANDSAT/LC8_L1T_TOA").filterDate('2015-06-01','2015-06-17').max()
mapId = lc8.getMapId({ 'bands': ['B6', 'B5', 'B4']})

print(mapId);