#!/usr/bin/python

import ee
import ee.mapclient

from lapig.ee import mvc


ee.Initialize();

NDVI_PALETTE = 'ec1413, e8dfa0, 0aa73c';

mvcs = mvc.getImages();
print(mvcs);

ee.mapclient.addToMap(mvcs['mean'], { 'palette': NDVI_PALETTE }, 'mvc-mean');