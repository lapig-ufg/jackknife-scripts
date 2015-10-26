#!/usr/bin/python

import datetime
import ee
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

	def mvcMonthMaxFn(image):
		md = image.metadata("MONTH");
		return md.mask(image.eq(mvcMax));

	def mvcMonthMinFn(image):
		md = image.metadata("MONTH");
		return md.mask(image.eq(mvcMin));

	mvcMonthMax = mvcCollection.map(mvcMonthMaxFn).reduce(ee.Reducer.max());
	mvcMonthMin = mvcCollection.map(mvcMonthMinFn).reduce(ee.Reducer.min());

	return {
			"mean": mvcMean
		,	"max": mvcMax
		,	"min": mvcMin
		,	"stdDev": mvcStdDev
		,	"monthMax": mvcMonthMax
		,	"monthMin": mvcMonthMin

	}

def getImages():

	BRAZIL_BB = { 'x1': -76.60, 'y1': -35.06, 'x2': -33.43,  'y2': 5.13 };
	BRAZIL_RECT = ee.Geometry.Rectangle(BRAZIL_BB['x1'], BRAZIL_BB['y1'], BRAZIL_BB['x2'], BRAZIL_BB['y2']);

	months = [4, 5, 6, 7, 8, 9, 10, 11, 12];
	years = [2013, 2014];

	mvcs = [];

	for month in months:

		yearsResult = [];

		for year in years:
			interval = getMonthInterval(month, year);
			yearsResult.append( ee.ImageCollection('LANDSAT/LC8_L1T_8DAY_NDVI').filterDate(interval['start'], interval['end']).max().clip(BRAZIL_RECT) );
		
		mvc = ee.ImageCollection.fromImages(yearsResult).max();
		mvc = mvc.set({'MONTH': month});
		mvcs.append(mvc);

	result = getStatBands(mvcs);
	result['months'] = mvcs;

	return result