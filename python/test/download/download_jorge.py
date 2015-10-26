#!/usr/bin/python

import datetime
import ee
import os
import copy

from lapig.ee import download
from datetime import datetime
from dateutil.relativedelta import *

ee.Initialize()

NDVI_PALETTE = 'e48919, e8dfa0, 0aa73c';
evi2Expression = "2.5 * ( ( b('B5') - b('B4') ) / ( b('B5') + (2.4 * b('B4') ) + 1))";

pastagem = ee.Image("04773272298627679741-09757940799309423091");

def newDate(dateStr):
  return datetime.strptime(dateStr, "%m/%d/%Y");

def getMonthInterval(starDt, endDt):
  monthIntervals = []

  dt1 = newDate(starDt);
  endDt = newDate(endDt);

  dt2 = copy.copy(dt1);

  while dt2.month < endDt.month or dt2.year < endDt.year or dt2.day < endDt.day:
    dt2 = copy.copy(dt1);

    dt2 = dt2 + relativedelta(months=+1, days=-1);
    
    monthIntervals.append({ "dt1": copy.copy(dt1), "dt2": copy.copy(dt2) });

    dt1 = dt1 + relativedelta(months=+1);
  
  return monthIntervals;

def applyModel(collectionId, starDt, endDt, bounds, mask):
  
  imgResult = [];

  def applyCloudScore(image):
          
    image = image.mask(mask);
    image = ee.Algorithms.Landsat.simpleCloudScore(image);
    
    quality = image.select('cloud').gt(10);
    maskedImage = image.mask().And(quality.Not());
    
    image = image.mask(maskedImage) \
                .expression(evi2Expression) \
                .select([0],['evi2']);
    
    return image;

  monthIntervals = getMonthInterval(starDt, endDt);

  for m in monthIntervals:
    img = ee.ImageCollection(collectionId) \
                .filterDate(m['dt1'], m['dt2']) \
                .filterBounds(bounds);
                          
    modelImg = img.map(applyCloudScore) \
                          .median();
    
    imgResult.append({ 'img': modelImg, 'id': 'EVI2-' + str(m['dt1'].month) + str(m['dt1'].year) });

  return imgResult

bounds = pastagem.reduceToVectors(scale=10000).geometry().bounds();

#"202.07 * b('evi2') - 17.658"
result = applyModel('LANDSAT/LC8_L1T_TOA', '10/01/2013', '09/30/2014', bounds, pastagem);
bbox = { 'x1': -68.8245687407108, 'y1': -24.307904722689177, 'x2': -41.51588258047489,  'y2': -1.4907825295665782 };

for r in result:
  print('donwlodeando... ' + r['id'])
  download.eeImage(r['img'], 30, 'EPSG:4326', bbox, r['id']);