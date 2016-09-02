#!/usr/bin/python

import math
import time
import json
import ee
import traceback

ee.Initialize()

# BR ['001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068'],
#"CAATINGA_PILOTO": ['214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','216063','216064','216065','216066','216067','216068','217062','217063','217064','217065','217066','217067','217068','218062','218063','218064','218065','218066','218067','218068','219062','219063','219064','219065','219066','219067','219068','220062','220063','220064','220065','220066','220067','220068'],
#"ALTA_FLORESTA": ['214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','216063','216064','216065','216066','216067','216068','217062','217063','217064','217065','217066','217067','217068','218062','218063','218064','218065','218066','218067','218068','219062','219063','219064','219065','219066','219067','219068','220062','220063','220064','220065','220066','220067','220068'],

# Configuration options
config = {
  "grid": {
      "tiles": ['001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068'],
      "ftCollection": 'ft:1qNHyIqgUjShP2gQAcfGXw-XoxWwCRn5ZXNVqKIS5'
  }
  , "download": {
        "createTask": True
      , "poolSize": 10
      , "poolCheckTime": 60
      , "taskConfig": { "scale": 30, "maxPixels": 1.0E13, "driveFolder": 'crop_pasture' }
  }
  , "visualization": {
        "addToMap": True
      , "addTmpResults": False
      , "palette": 'f7c1c2, ec1413'
  }
  , "mvc": {
        "qualityIndex": 'ndvi'
      , "series": [
          {
            "prefix": 'C1314_',
            "imgCollection": 'LANDSAT/LC8_L1T_TOA',
            "qualityBand": 'BQA',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B6','B5','B4'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B5') - b('B4')) / (b('B5') + b('B4'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2014-02-01", "end": "2014-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2013-04-01", "end": "2013-05-31" }, { "start": "2014-04-01", "end": "2014-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2013-06-01", "end": "2013-07-31" }, { "start": "2014-06-01", "end": "2014-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2013-08-01", "end": "2013-09-30" }, { "start": "2014-08-01", "end": "2014-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2013-10-01", "end": "2013-11-30" }, { "start": "2014-10-01", "end": "2014-11-30" }  ] }
              ,  { "id": "1201", "dates": [ { "start": "2013-12-01", "end": "2014-01-30" }, { "start": "2014-12-01", "end": "2015-01-31" }  ] }
            ]
          },
          {
            "prefix": 'C111213_',
            "imgCollection": 'LANDSAT/LE7_L1T_TOA',
            "qualityBand": '',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B5','B4','B3'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B4') - b('B3')) / (b('B4') + b('B3'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2011-02-01", "end": "2011-03-31" }, { "start": "2012-02-01", "end": "2012-03-31" }, { "start": "2013-02-01", "end": "2013-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2011-04-01", "end": "2011-05-31" }, { "start": "2012-04-01", "end": "2012-05-31" }, { "start": "2013-04-01", "end": "2013-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2011-06-01", "end": "2011-07-31" }, { "start": "2012-06-01", "end": "2012-07-31" }, { "start": "2013-06-01", "end": "2013-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2011-08-01", "end": "2011-09-30" }, { "start": "2012-08-01", "end": "2012-09-30" }, { "start": "2013-08-01", "end": "2013-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2011-10-01", "end": "2011-11-30" }, { "start": "2012-10-01", "end": "2012-11-30" }, { "start": "2013-10-01", "end": "2013-11-30" } ] }
              ,  { "id": "1201", "dates": [ { "start": "2011-12-01", "end": "2012-01-30" }, { "start": "2012-12-01", "end": "2013-01-30" }, { "start": "2013-12-01", "end": "2014-01-31" } ] }
            ]
          },
          {
            "prefix": 'C1011_',
            "imgCollection": 'LANDSAT/LT5_L1T_TOA',
            "qualityBand": '',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B5','B4','B3'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B4') - b('B3')) / (b('B4') + b('B3'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2010-02-01", "end": "2010-03-31" }, { "start": "2011-02-01", "end": "2011-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2010-04-01", "end": "2010-05-31" }, { "start": "2011-04-01", "end": "2011-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2010-06-01", "end": "2010-07-31" }, { "start": "2011-06-01", "end": "2011-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2010-08-01", "end": "2010-09-30" }, { "start": "2011-08-01", "end": "2011-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2010-10-01", "end": "2010-11-30" }, { "start": "2011-10-01", "end": "2011-11-30" }  ] }
              ,  { "id": "1201", "dates": [ { "start": "2010-12-01", "end": "2011-01-30" }, ] }
            ]
          },
          {
            "prefix": 'C0910_',
            "imgCollection": 'LANDSAT/LT5_L1T_TOA',
            "qualityBand": '',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B6','B5','B4'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B4') - b('B3')) / (b('B4') + b('B3'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2009-02-01", "end": "2009-03-31" }, { "start": "2010-02-01", "end": "2010-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2009-04-01", "end": "2009-05-31" }, { "start": "2010-04-01", "end": "2010-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2009-06-01", "end": "2009-07-31" }, { "start": "2010-06-01", "end": "2010-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2009-08-01", "end": "2009-09-30" }, { "start": "2010-08-01", "end": "2010-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2009-10-01", "end": "2009-11-30" }, { "start": "2010-10-01", "end": "2010-11-30" }  ] }
              ,  { "id": "1201", "dates": [ { "start": "2009-12-01", "end": "2010-01-30" }, { "start": "2010-12-01", "end": "2011-01-31" }  ] }
            ]
          },
          {
            "prefix": 'C0809_',
            "imgCollection": 'LANDSAT/LT5_L1T_TOA',
            "qualityBand": '',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B6','B5','B4'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B4') - b('B3')) / (b('B4') + b('B3'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2008-02-01", "end": "2008-03-31" }, { "start": "2009-02-01", "end": "2009-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2008-04-01", "end": "2008-05-31" }, { "start": "2009-04-01", "end": "2009-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2008-06-01", "end": "2008-07-31" }, { "start": "2009-06-01", "end": "2009-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2008-08-01", "end": "2008-09-30" }, { "start": "2009-08-01", "end": "2009-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2008-10-01", "end": "2008-11-30" }, { "start": "2009-10-01", "end": "2009-11-30" }  ] }
              ,  { "id": "1201", "dates": [ { "start": "2008-12-01", "end": "2009-01-30" }, { "start": "2009-12-01", "end": "2010-01-31" }  ] }
            ]
          },
          {
            "prefix": 'C0708_',
            "imgCollection": 'LANDSAT/LT5_L1T_TOA',
            "qualityBand": '',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B6','B5','B4'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B4') - b('B3')) / (b('B4') + b('B3'))" }  
            ],
            "composites": [
                 { "id": "0203", "dates": [ { "start": "2007-02-01", "end": "2007-03-31" }, { "start": "2008-02-01", "end": "2008-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2007-04-01", "end": "2007-05-31" }, { "start": "2008-04-01", "end": "2008-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2007-06-01", "end": "2007-07-31" }, { "start": "2008-06-01", "end": "2008-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2007-08-01", "end": "2007-09-30" }, { "start": "2008-08-01", "end": "2008-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2007-10-01", "end": "2007-11-30" }, { "start": "2008-10-01", "end": "2008-11-30" }  ] }
              ,  { "id": "1201", "dates": [ { "start": "2007-12-01", "end": "2008-01-30" }, { "start": "2008-12-01", "end": "2009-01-31" }  ] }
            ]
          }
      ]
  }
  , "cloud": {
      "cloudCoverThreshold": 80
    , "eeThreshold": 40
    , "bqaThreshold": 53248
    , "gapfillValue": -1
  }
  , "classification": {
      "nTrees": 100
    , "threshold": 0
    , "variablesPerSplit": 1
  }
  , "trainning": {
      "nPoints": 20000
    , "scale": 30
    , "strategy": 'percentage'
    , "gridCellSize": 5
    , "referenceMask": ee.Image('users/lealparente/pasture_crop_mask_v2')
  }
}

# Pixel class percentage calculation considering landsat image boundary
def getPctPixels(referenceMask, classBand, classValue, gridCell):
  
  total = referenceMask.reduceRegion(reducer=ee.Reducer.count(), geometry=gridCell, scale=30, maxPixels=1.0E13);
  
  classMask = referenceMask.eq(classValue);
  classCount = classMask.mask(classMask).reduceRegion(reducer=ee.Reducer.count(), geometry=gridCell, scale=30, maxPixels=1.0E13)

  nClassCount = ee.Number(ee.Dictionary(classCount).get(classBand));
  nTotal = ee.Number(ee.Dictionary(total).get(classBand));
  
  return nClassCount.divide(nTotal).getInfo()

# Generate a trainning dataset considering two approachs:
# * A priori probability: using getPctPixels method
# * Normal: try to using the same number of samples for all class
def getTrainningDataset(image, gridCell, seed):
  
  classBand = 'class'
  scale = config['trainning']['scale']
  nPoints = config['trainning']['nPoints']
  gridCellSize = config['trainning']['gridCellSize']
  strategy = config['trainning']['strategy']
  referenceMask = config['trainning']['referenceMask']

  nPoints = int(nPoints / (gridCellSize * gridCellSize))
  print(nPoints, gridCellSize, config['trainning']['nPoints'])

  referenceMask = referenceMask.select([0],[classBand]);
  referenceMask = referenceMask.expression("( b('class') == 255 ) ? 3 : ( b('class') == 2 ? 3 : ( b('class') == 4 ? 2 : b('class') ) ) ")

  image = image.addBands(referenceMask);
  gapfillMask = image.neq(-1);
  image = image.mask(gapfillMask);

  classValues = [1,2,3]
  points = image.sample(numPixels=math.trunc(nPoints * 5), scale=scale, seed=seed, region=gridCell)

  result = None;

  for classValue in classValues:
    
    if strategy == 'percentage':
      classPct = getPctPixels(referenceMask, classBand, classValue, gridCell);

      if classPct > 0.1 and classPct < 0.15:
        classPct = 0.15
      elif classPct > 0.75:
        classPct = 0.75

      numClassPoints = math.ceil(nPoints * classPct)
    else:
      numClassPoints = nPoints / len(classValues)
    
    classPoints = points.filter(ee.Filter.eq(classBand, classValue)).limit(numClassPoints)

    if result == None:
      result = classPoints;
    else:
      result = result.merge(classPoints)

  result = result.set('band_order', points.get('band_order'))
  
  return result

# Generate Maximum Value Composite (MVC) and all bands for classification raster dataset
def getMVC(serie, gridCell, fakeBands):

  mvc = None
  indexes = serie['indexes']
  composites = serie['composites']
  eeThreshold = config['cloud']['eeThreshold']
  qualityIndex = config['mvc']['qualityIndex']
  bqaThreshold = config['cloud']['bqaThreshold']
  gapfillValue = config['cloud']['gapfillValue']
  cloudCoverThreshold = config['cloud']['cloudCoverThreshold']
  imgCollection = ee.ImageCollection(serie['imgCollection'])
  
  def indexName(name):
    return name + '-' + configComposite['id']
  
  def calculateIndexes(image):
    scored = ee.Algorithms.Landsat.simpleCloudScore(image)
    
    cloudEE = scored.select('cloud').gte(eeThreshold);
    cloudEE = cloudEE.mask(cloudEE)
    cloudEE = cloudEE.unmask(0);

    cloudMask = None
    if serie['qualityBand']:
      cloudLT = image.select('BQA').gte(bqaThreshold);
      cloudLT = cloudLT.mask(cloudLT).select(['BQA'],['cloud']);
      cloudLT = cloudLT.unmask(0);
      cloudMask = cloudLT.add(cloudEE).gt(0).Not();
    else:
      cloudMask = cloudEE.gt(0).Not();

    resultImage = None
    
    for index in indexes:
      indexBand = image.expression(index['expression']).select([0],[indexName(index['id'])]).toFloat()
      resultImage = indexBand if resultImage == None else resultImage.addBands(indexBand)
    
    resultImage = resultImage.mask(cloudMask);
    resultImage = resultImage.unmask(gapfillValue);

    return resultImage;

  for i in xrange(0,len(composites)):
    configComposite = composites[i]
    
    compositeCol = None
    
    for j in xrange(0, len(configComposite['dates'])):
      date = configComposite['dates'][j]
      
      compositePart = imgCollection \
        .filterDate(date['start'], date['end']) \
        .filterBounds(gridCell.centroid()) \
        .filterMetadata('CLOUD_COVER', 'less_than', cloudCoverThreshold) \
        .map(calculateIndexes)

      compositeCol = compositePart if compositeCol == None else ee.ImageCollection(compositeCol.merge(compositePart))
    
    composite = compositeCol.qualityMosaic(indexName(qualityIndex))
    
    mvc = composite if mvc == None else mvc.addBands(composite)

  bands = [];
  bandNamesMap = {}

  bandNamesList = mvc.bandNames().getInfo()
  for bandName in bandNamesList:
    bandNamesMap[bandName] = True
    bands.append(bandName)

  for index in indexes:
    indexImages = []
    
    for configComposite in composites:
      indexBandname = index['id'] + '-' + configComposite['id']
      compositeBandname = 'C' + configComposite['id']
      indexName(compositeBandname)
      if indexBandname in bandNamesMap:
        mask = mvc.select([indexBandname],[index['id']]).neq(gapfillValue);
        indexImages.append(mvc.mask(mask).select([indexBandname],[index['id']]))
      elif fakeBands:
        mvc = mvc.addBands(ee.Image(gapfillValue).select([0],[indexBandname]))
        bands.append(indexBandname);
    
    """
    i1Cs1 = index['id']+'-120102';
    i2Cs1 = index['id']+'-060708';
    bandNameCs1 = index['id']+'-cs1';
    if (i1Cs1 in bandNamesMap) and (i2Cs1 in bandNamesMap):
      i1Cs1Img = mvc.select(i1Cs1)
      i2Cs1Img = mvc.select(i2Cs1)

      i1Mask = i1Cs1Img.neq(gapfillValue);
      i2Mask = i2Cs1Img.neq(gapfillValue);

      i1Cs1Img = i1Cs1Img.mask(i1Mask);
      i2Cs1Img = i2Cs1Img.mask(i2Mask);

      cs1 = i1Cs1Img.subtract(i2Cs1Img).divide(i2Cs1Img).select([0], [bandNameCs1])
      mvc = mvc.addBands(cs1)
      bands.append(bandNameCs1)
    elif fakeBands:
      mvc = mvc.addBands(ee.Image(gapfillValue).select([0],[bandNameCs1]))
      bands.append(bandNameCs1);
    """
    
    """
    bandNameStdDev = index['id']+'-stddev';
    if len(indexImages) > 0:
      indexCollection = ee.ImageCollection.fromImages(indexImages)
      indexStdDev = indexCollection.reduce(ee.Reducer.stdDev()).select([0], [bandNameStdDev]).toFloat()
      mvc = mvc.addBands(indexStdDev)
      bands.append(bandNameStdDev)
    """
    
    i1Cs1 = index['id']+'-0405';
    i2Cs1 = index['id']+'-0809';
    bandNameCs1 = index['id']+'-cs1';
    if (i1Cs1 in bandNamesMap) and (i2Cs1 in bandNamesMap):
      i1Cs1Img = mvc.select(i1Cs1)
      i2Cs1Img = mvc.select(i2Cs1)

      i1Mask = i1Cs1Img.neq(gapfillValue);
      i2Mask = i2Cs1Img.neq(gapfillValue);

      i1Cs1Img = i1Cs1Img.mask(i1Mask);
      i2Cs1Img = i2Cs1Img.mask(i2Mask);

      cs1 = i1Cs1Img.subtract(i2Cs1Img).divide(i2Cs1Img).select([0], [bandNameCs1])
      mvc = mvc.addBands(cs1)
      bands.append(bandNameCs1)
    elif fakeBands:
      mvc = mvc.addBands(ee.Image(gapfillValue).select([0],[bandNameCs1]))
      bands.append(bandNameCs1);
    
    i1Cs2 = index['id']+'-1201'
    i2Cs2 = index['id']+'-1011'
    bandNameCs2 = index['id']+'-cs2';

    if (i1Cs2 in bandNamesMap) and (i2Cs2 in bandNamesMap): 
      i1Cs2Img = mvc.select(i1Cs2)
      i2Cs2Img = mvc.select(i2Cs2)

      i1Mask = i1Cs2Img.neq(gapfillValue);
      i2Mask = i2Cs2Img.neq(gapfillValue);

      i1Cs2Img = i1Cs2Img.mask(i1Mask);
      i2Cs2Img = i2Cs2Img.mask(i2Mask);

      cs2 = i1Cs2Img.subtract(i2Cs2Img).divide(i2Cs2Img).select([0], [bandNameCs2])
      mvc = mvc.addBands(cs2)
      bands.append(bandNameCs2)
    elif fakeBands:
      mvc = mvc.addBands(ee.Image(gapfillValue).select([0],[bandNameCs2]))
      bands.append(bandNameCs2);
  
  return mvc, bands;

# Execute a classification approach
def classification(mvc, gridCell, classifier):
  
  classificationArray = []
  threshold = config['classification']['threshold']
  
  clipedMvc = mvc.clip(gridCell)

  classificationResult = clipedMvc.classify(classifier);
  classificationResult = classificationResult.toInt8()
  
  classificationResult = classificationResult.set('system:footprint', mvc.get('system:footprint'))

  return classificationResult

def getTrainningDatasetWithNeighbors(tile, neighborsGridCell):
  
  series = config['mvc']['series']

  trainningDataset = None
  trainningBands = None
  mainSerie = series[0]

  for i in xrange(len(neighborsGridCell)):
    neiGridCell = neighborsGridCell[i]
    mvc, mvcBands = getMVC(mainSerie, neiGridCell, True);

    if len(mvcBands) == 0:
      continue;

    key = tile + '-' + mainSerie['prefix'] + ' - ' + str(i)
    seed = abs(hash(key)) % (10 ** 8)
    neiTrainningDataset = getTrainningDataset(mvc, neiGridCell, seed);

    print(key, seed)

    if trainningBands is None:
      trainningBands = mvcBands;
      trainningDataset = neiTrainningDataset;
    else:
      trainningDataset = trainningDataset.merge(neiTrainningDataset);
      trainningBands = list(set(trainningBands) | set(mvcBands))

  return trainningDataset, trainningBands

# Execution control for classification in one grid cell
def run(tile, gridCell, neighborsGridCell):
  
  series  = config['mvc']['series'];
  nTrees = config['classification']['nTrees'];
  variablesPerSplit = config['classification']['variablesPerSplit'];
  
  result = {};
  
  #trainningDataset, trainningBands = getTrainningDatasetWithNeighbors(tile, neighborsGridCell)

  #if len(trainningBands) > 0:
  for serie in series:
    mvc, mvcBands = getMVC(serie, gridCell, False);
    #mvcBands.append('class');
    #serieTrainningDataset = trainningDataset.select(mvcBands)

    #classifier = ee.Classifier.randomForest(nTrees, variablesPerSplit, 1, 0.5);
    #classifier = classifier.train(serieTrainningDataset, 'class', mvcBands);
    
    #serieResult = classification(mvc, gridCell, classifier)
    #result[serie['prefix'] + tile] = serieResult;
    print(serie['prefix'] + tile, mvcBands)
    #else:
    #  print tile + ' classificationBands is empty !!!'
  
  return result

# Control for download pool
def checkPoolState(config, taskPool):
  print(len(taskPool), 'sleep time')
  time.sleep(config['download']['poolCheckTime'])
  for task in list(taskPool):
    status = task.status()
    print(status['state'])
    if status['state'] in (ee.batch.Task.State.FAILED, ee.batch.Task.State.COMPLETED, ee.batch.Task.State.CANCELLED):
      taskPool.remove(task)
      if('error_message' in status):
        print(task.config['description'], status['error_message'])
      if('error_message' in status and status['error_message'] == 'User memory limit exceeded.'):
        taskId = task.config['description'];
        print(taskId, 'Re-run task')
        reRuntask = ee.batch.Export.image(mapResult[taskId]['result'], taskId, mapResult[taskId]['config'])
        reRuntask.start()
        taskPool.append(reRuntask)

def getGridCell(tile):

  gridCellSize = config['trainning']['gridCellSize']
  incNumber = (gridCellSize - 1) / 2

  path = int(tile[:3])
  row = int(tile[3:])

  result = []

  for pInc in xrange(path-incNumber, (path+incNumber) + 1):
    for rInc in xrange(row-incNumber, (row+incNumber) + 1):
      
      pAux = pInc
      rAux = rInc

      if path == 1 and pAux == 0:
        pAux = 233
      elif path == 233 and pAux == 234:
        pAux = 1
      
      tAux = str(pAux).zfill(3) + str(rAux).zfill(3)
      if tAux in tileDict:
        gridCell = ee.FeatureCollection(config['grid']['ftCollection']) \
          .filter(ee.Filter.eq('TILE_T', 'T'+tAux)) \
          .first() \
          .geometry()
        result.append(gridCell)

  return result

center = None
taskPool = []
mapResult = {}
tileDict = {}

for tile in config['grid']['tiles']:
  tileDict[tile] = True

for tile in config['grid']['tiles']:
  
  neighborsGridCell = getGridCell(tile);
 
  gridCell = ee.FeatureCollection(config['grid']['ftCollection']) \
    .filter(ee.Filter.eq('TILE_T', 'T'+tile)) \
    .first() \
    .geometry();

  run(tile, gridCell, neighborsGridCell)