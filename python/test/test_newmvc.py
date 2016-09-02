#!/usr/bin/python

import ee
import ee.mapclient
import shapefile

from lapig.ee import newmvc
from lapig.ee import download


ee.Initialize();

NDVI_PALETTE = 'ec1413, e8dfa0, 0aa73c';

sf = shapefile.Reader("/data/lapig/GEO/SHP/pa_br_cenas_landsat_1000_2001_LAPIG_corrigido.shp");

gapFillValues=[0]
cloudThreshold=40

pathRows = [ [227, 67], [228, 67], [227, 68], [228, 68] ]

for rec in sf.shapeRecords():
	path = rec.record[0]
	row = rec.record[1]
	
	for pathRow in pathRows:
		if path == pathRow[0] and row == pathRow[1]:
			shpBbox = rec.shape.bbox;

			bbox = { 'x1': shpBbox[0], 'y1': shpBbox[1], 'x2': shpBbox[2],  'y2': shpBbox[3] };

			for gapFillValue in gapFillValues:
				
				basename = str(path) + '_' + str(row) + '_gapfill_' + str(gapFillValue) + '_';
				print('GENERATE ' + basename);

				mvcs = newmvc.getImages(path, row, bbox, cloudThreshold, gapFillValue);

				#ee.mapclient.addToMap(mvcs['cs1'], { 'palette': NDVI_PALETTE }, 'dez/jan');
				#ee.mapclient.centerMap(-49.25,-16.66,5)

				#print(mvcs['months']);
				#download.eeImage(mvcs['months'][4], 30, 'EPSG:4326', bbox, basename + str(5));
				#download.eeImage(mvcs['months'][5], 30, 'EPSG:4326', bbox, basename + str(6));
				#print(mvcs['months'][4].getInfo());

				i=1;
				for mvcMonth in mvcs['months']:
					download.eeImage(mvcMonth, 30, 'EPSG:4326', bbox, basename + str(i));
					i += 1
				

				download.eeImage(mvcs['cs1'], 30, 'EPSG:4326', bbox, basename + 'cs1');
				download.eeImage(mvcs['cs2'], 30, 'EPSG:4326', bbox, basename + 'cs2');
				#download.eeImage(mvcs['min'], 30, 'EPSG:4326', bbox, basename + 'min');
				#download.eeImage(mvcs['max'], 30, 'EPSG:4326', bbox, basename + 'max');
				#download.eeImage(mvcs['mean'], 30, 'EPSG:4326', bbox, basename + 'mean');
				download.eeImage(mvcs['stdDev'], 30, 'EPSG:4326', bbox, basename + 'stdDev');

"""
from osgeo import gdal, gdal_array
import numpy as np
b1 = gdal.Open("LT50250232011160PAC01_sr_band1.tif")
b2 = gdal.Open("LT50250232011160PAC01_sr_band2.tif")
array1 = b1.ReadAsArray()
array2 = b2.ReadAsArray()
stacked = np.array([array1,array2])
gdal_array.SaveArray(stacked.astype("int"), "b12_stacked.tif", "GTiff", gdal.Open("LT50250232011160PAC01_sr_band1.tif"))
"""