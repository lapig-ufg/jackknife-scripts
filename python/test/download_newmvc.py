#!/usr/bin/python

import ee
import ee.mapclient
import shapefile
from lapig.ee import newmvc
from lapig.ee import download

ee.Initialize();

NDVI_PALETTE = 'ec1413, e8dfa0, 0aa73c';

#sf = shapefile.Reader("/data/lapig/GEO/SHP/cenas_landsat_MT_WGS84.shp");
sf = shapefile.Reader("/data/lapig/GEO/SHP/MT/pa_br_landsat_norte_mt.shp");
shapeRecs = sf.shapeRecords();

shpBbox = sf.bbox;
bbox = { 'x1': shpBbox[0], 'y1': shpBbox[1], 'x2': shpBbox[2],  'y2': shpBbox[3] };
mvcs = newmvc.getImages(bbox);

basename = 'NORTE-MT-1';
i=1;
for mvcMonth in mvcs['months']:
	download.eeImage(mvcMonth, 30, 'EPSG:4326', bbox, basename + str(i));
	i += 1

download.eeImage(mvcs['cs1'], 30, 'EPSG:4326', bbox, basename + 'cs1');
download.eeImage(mvcs['cs2'], 30, 'EPSG:4326', bbox, basename + 'cs2');
download.eeImage(mvcs['min'], 30, 'EPSG:4326', bbox, basename + 'min');
download.eeImage(mvcs['max'], 30, 'EPSG:4326', bbox, basename + 'max');
download.eeImage(mvcs['mean'], 30, 'EPSG:4326', bbox, basename + 'mean');
download.eeImage(mvcs['stdDev'], 30, 'EPSG:4326', bbox, basename + 'stdDev');