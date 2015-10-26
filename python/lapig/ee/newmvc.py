#!/usr/bin/python

import datetime
import ee
import ee.mapclient
import os

from datetime import datetime
from dateutil.relativedelta import *

def newDate(year, month, day):
	return datetime(year, month, day);

def getMonthInterval(month, year):
	startDt = newDate(year, month, 1);
	endDt = newDate(year, month, 1);
	
	endDt = endDt + relativedelta(months=+1, days=-1);
	
	return { 'start': startDt, 'end': endDt };

def getStatBands(mvcs):
	mvcCollection = ee.ImageCollection.fromImages(mvcs);

	mvcMean = mvcCollection.reduce(ee.Reducer.mean());
	mvcMax = mvcCollection.reduce(ee.Reducer.max());
	mvcMin = mvcCollection.reduce(ee.Reducer.min());
	mvcStdDev = mvcCollection.reduce(ee.Reducer.std_dev());

	return {
			"mean": mvcMean.select([0], ['NDVI'])
		,	"max": mvcMax.select([0], ['NDVI'])
		,	"min": mvcMin.select([0], ['NDVI'])
		,	"stdDev": mvcStdDev.select([0], ['NDVI'])

	}

def	isInvalidDate(month, year):
	return (
				(month == 1 and ( year == 2013 ) )
		or	(month == 2 and ( year == 2013 ) )
		or	(month == 3 and ( year == 2013 ) )
		or	(month == 4 and ( year == 2015 ) )
		or	(month == 5 and ( year == 2015 ) )
		or	(month == 6 and ( year == 2015 ) )
		or	(month == 7 and ( year == 2015 ) )
		or	(month == 8 and ( year == 2015 ) )
		or	(month == 9 and ( year == 2015 ) )
		or	(month == 10 and ( year == 2015 ) )
		or	(month == 11 and ( year == 2015 ) )
		or	(month == 12 and ( year == 2015 ) )
	)

def getBandNames(img):
	bandNames = None
	while True:
		try:
			bandNames = img.bandNames().getInfo();
			break;
		except:
			continue

	return bandNames

def getMaxImages(bbox, wrsFilter, cloudThreshold):
	months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
	years = [2013, 2014, 2015];
	bqaThreshold = 53248


	def calculateNDVI(image):
		image = ee.Algorithms.Landsat.simpleCloudScore(image);

		bqaCloud = image.select('BQA').gt(bqaThreshold).Not();
		googleCloud = image.select('cloud').gt(cloudThreshold).Not();

		bqaCloud = bqaCloud.mask(bqaCloud).select(['BQA'],['cloud']);
		googleCloud = googleCloud.mask(googleCloud)

		cloudMask = ee.ImageCollection([bqaCloud, googleCloud]).max();

		return image.mask(cloudMask).expression("(b('B5') - b('B4')) / (b('B5') + b('B4'))");

	maxImages = {};

	for month in months:

		yearsResult = [];

		for year in years:

			if( isInvalidDate(month, year) ):
				continue;

			interval = getMonthInterval(month, year);
			yearImg = ee.ImageCollection('LANDSAT/LC8_L1T_TOA') \
									.filterDate(interval['start'], interval['end']) \
									.filter(wrsFilter) \
									.map(calculateNDVI) \
									.max();
			#print(month, year, len(yearImg.bandNames().getInfo()));

			if len( getBandNames(yearImg) ) > 0:
				yearsResult.append(yearImg)
		
		#print(month, len(yearsResult));
		maxImage = ee.ImageCollection.fromImages(yearsResult).max();
		maxImage = maxImage.set({'MONTH': month});
		maxImages[month] = maxImage;

	return maxImages;

def getImages(path, row, bbox, cloudThreshold, gapFillValue):

	wrsFilter = ee.Filter.And( ee.Filter.eq('WRS_PATH', path), ee.Filter.eq('WRS_ROW', row) );
	bboxGeometry = ee.Geometry.Rectangle(bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']);

	mvcs = [];
	mvcsCloud = [];
	mvcGapFil = [];

	maxImages = getMaxImages(bboxGeometry, wrsFilter, cloudThreshold);
	mvcMonths = [ [4,5],[6,7],[8,9],[10,11],[12,1],[2,3] ];

	for mvcMonth in mvcMonths:
		mvc = ee.ImageCollection.fromImages([ maxImages[mvcMonth[0]], maxImages[mvcMonth[1]] ]).max();
		cloud = mvc.mask(mvc.mask().Not()).Not().clip(bboxGeometry);

		#print(mvcMonth, len(mvc.bandNames().getInfo()));
		
		if len( getBandNames(mvc) ) == 0:
			mvc = ee.Image(0).clip(bboxGeometry);
			cloud = ee.Image(0).clip(bboxGeometry);


		mvc = mvc.select([0], ['NDVI']);
		cloud = cloud.select([0], ['NDVI']);

		mvcs.append(mvc);
		mvcsCloud.append(cloud);

	mvcsMean = ee.ImageCollection.fromImages(mvcs).mean();

	for i, mvc in enumerate(mvcs):
		cloud = mvcsCloud[i];

		if gapFillValue is 0:
			gapFill = cloud.multiply(mvcsMean).float();
		else:
			gapFill = cloud.multiply(gapFillValue).float();
		
		resultGapFill = ee.ImageCollection.fromImages([gapFill, mvc]).max();
		mvcGapFil.append(resultGapFill);

	cs1 = mvcGapFil[0].subtract(mvcGapFil[2]).divide(mvcGapFil[2]).select([0], ['NDVI'])
	cs2 = mvcGapFil[4].subtract(mvcGapFil[3]).divide(mvcGapFil[3]).select([0], ['NDVI'])

	result = getStatBands(mvcGapFil);
	result['cs1'] = cs1;
	result['cs2'] = cs2;
	result['months'] = mvcGapFil;

	return result