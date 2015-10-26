#!/usr/bin/python

import ee
import traceback

def imageCollection2Array(collectionId, starDt, endDt, filter):
  imgCollection = ee.ImageCollection(collectionId).filterDate(starDt, endDt).filter(filter);
  
  def getIds(img, prev):
    prev = ee.Dictionary(prev);
    ids = ee.String(prev.get('ids'));
    id = ee.String( collectionId + '/' ).cat( ee.String( img.id() ) ).cat(',');
    ids = ids.cat(id);
    
    return { "ids": ids };
  
  result = imgCollection.iterate(getIds, { "ids": "" });
  result = ee.Dictionary(result);
  
  ids = ee.String(result.get('ids'));
  ids = ids.split(',');
  
  while True:
    try:
      ids = ids.getInfo();
      break;
    except:
      traceback.print_exc();
  
  result2 = [];
  
  for id in ids:
    result2.append({ "img": ee.Image.load(id), "id": id });

  return result2;