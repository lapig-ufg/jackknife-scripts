#!/usr/bin/python

import datetime
import traceback
import shapefile

import csv
import ee
import ee.mapclient

from lapig.ee import utils
from decimal import Decimal

ee.Initialize();

def percentage(value, total):
	return round(Decimal(value) / Decimal(total), 4) * 100

def getPixelsCloud(img, name):
	while True:
		
		try:
			r = img.reduceRegion(ee.Reducer.count(), None, 30, None, None, False, 60000000).getInfo();
			break;
		except:
			traceback.print_exc();

	return r[name];

pixelFile = open('cloudAnalysis-pixel.csv', 'wt')
percentageFile = open('cloudAnalysis-percentage.csv', 'wt')

pixelWriter = csv.writer(pixelFile)
percentageWriter = csv.writer(percentageFile)

collumns = [ 'scene', 'date', 'cloudCover', 'total', \
	'cloud', 	'maybe', \
	'cirrus', 'google_0', \
	'google_10', 'google_20', \
	'google_30', 'google_40', \
	'google_50', 'google_60', \
	'google_70', 'google_80', \
	'google_90', 'google_100', \
];

pixelWriter.writerow(collumns);
percentageWriter.writerow(collumns);

filter = ee.Filter.And( ee.Filter.eq('WRS_PATH', 227), ee.Filter.eq('WRS_ROW', 67) );

lc8array = utils.imageCollection2Array('LANDSAT/LC8', '2013-04-01', '2015-03-31', filter);

for lc8Obj in lc8array:

	ee.Initialize();

	lc8 = lc8Obj['img']

	imgTime = lc8.get('system:time_start').getInfo();
	dt = datetime.datetime.utcfromtimestamp(imgTime/1000);
	strDate = str(dt.strftime('%Y-%m-%d'));

	cloudCover = lc8.get('CLOUD_COVER').getInfo();

	bqa = lc8.select('BQA');

	cloud = bqa.gte(53248);
	cloudMaybe = bqa.gte(36864);
	cirrus = bqa.gte(28672).And(bqa.lte(31744))

	cloud = cloud.mask(cloud);
	cloudMaybe = cloudMaybe.mask(cloudMaybe);
	cirrus = cirrus.mask(cirrus);

	pixelsTotal = getPixelsCloud(bqa, 'BQA');
	pixelsCloud = getPixelsCloud(cloud, 'BQA');
	pixelsCloudMaybe = getPixelsCloud(cloudMaybe, 'BQA');
	pixelsCirrus = getPixelsCloud(cirrus, 'BQA');

	pixelRow = [	lc8Obj['id'], strDate, cloudCover, pixelsTotal, pixelsCloud, pixelsCloudMaybe, pixelsCirrus ];
	percentageRow = [ lc8Obj['id'], cloudCover, percentage(pixelsCloud, pixelsTotal), percentage(pixelsCloudMaybe, pixelsTotal), percentage(pixelsCirrus, pixelsTotal) ];

	for treshold in range(0,100,10):
	  
	  image = ee.Algorithms.Landsat.simpleCloudScore(lc8);
	  cloudImg = image.select('cloud').gt(treshold);
	  cloud = cloudImg.mask(cloudImg)
	  
	  pixelsCloud = getPixelsCloud(cloud, 'cloud');
	  cloudPercentage = percentage(pixelsCloud, pixelsTotal);

	  pixelRow.append(pixelsCloud);
	  percentageRow.append(cloudPercentage);

	pixelWriter.writerow( pixelRow );
	percentageWriter.writerow( percentageRow );

pixelFile.close()
percentageFile.close()