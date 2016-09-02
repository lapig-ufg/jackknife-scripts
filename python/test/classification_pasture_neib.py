#!/usr/bin/python

import math
import time
import json
import ee
import logging
import traceback
import os

ee.Initialize()

# BR ['001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068'],
#"CAATINGA_PILOTO": ['214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','216063','216064','216065','216066','216067','216068','217062','217063','217064','217065','217066','217067','217068','218062','218063','218064','218065','218066','218067','218068','219062','219063','219064','219065','219066','219067','219068','220062','220063','220064','220065','220066','220067','220068'],
#"ALTA_FLORESTA": ['214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','216063','216064','216065','216066','216067','216068','217062','217063','217064','217065','217066','217067','217068','218062','218063','218064','218065','218066','218067','218068','219062','219063','219064','219065','219066','219067','219068','220062','220063','220064','220065','220066','220067','220068'],

# Configuration options
config = {
  "grid": {
      "allTiles": ['001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068'],
      "tilesToProcess": ['214064','214065','214066','215064','215065','215066','216064','216065','216066','217073','217074','217075','218073','218074','218075','219073','219074','219075','222065','222066','222067','222080','222081','222082','223065','223066','223067','223080','223081','223082','224065','224066','224067','224080','224081','224082','225071','225072','225073','226071','226072','226073','227071','227072','227073','231066','231067','231068','232066','232067','232068','233066','233067','233068'],
      "ftCollection": 'ft:1qNHyIqgUjShP2gQAcfGXw-XoxWwCRn5ZXNVqKIS5'
  }
  , "mvc": {
        "qualityIndex": 'ndvi'
      , "series": [
          {
            "prefix": 'C1415_',
            "imgCollection": 'LANDSAT/LC8_L1T_TOA',
            "qualityBand": 'BQA',
            "visualization": {
              "viewComposites": False,
              "conf": { "bands": ['B6','B5','B4'] },
            },
            "indexes": [
                { "id": "ndvi", "expression": "(b('B5') - b('B4')) / (b('B5') + b('B4'))" }  
              , { "id": "ndwi", "expression": "(b('B5') - b('B6')) / (b('B5') + b('B6'))" }
              , { "id": "cai", "expression": "(b('B7') / b('B6'))" }
            ],
            "composites": [
                 { "id": "1201", "dates": [ { "start": "2013-12-01", "end": "2014-01-31" }, { "start": "2014-12-01", "end": "2015-01-31" } ] }
              ,  { "id": "0203", "dates": [ { "start": "2014-02-01", "end": "2014-03-31" }, { "start": "2015-02-01", "end": "2015-03-31" } ] }
              ,  { "id": "0405", "dates": [ { "start": "2014-04-01", "end": "2014-05-31" }, { "start": "2015-04-01", "end": "2015-05-31" } ] }
              ,  { "id": "0607", "dates": [ { "start": "2014-06-01", "end": "2014-07-31" }, { "start": "2015-06-01", "end": "2015-07-31" } ] }
              ,  { "id": "0809", "dates": [ { "start": "2014-08-01", "end": "2014-09-30" }, { "start": "2015-08-01", "end": "2015-09-30" } ] }
              ,  { "id": "1011", "dates": [ { "start": "2014-10-01", "end": "2014-11-30" }, { "start": "2015-10-01", "end": "2015-11-30" }  ] }
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
  , "trainning": {
      "nPoints": 2000
    , "scale": 30
    , "strategy": 'percentage'
    , "gridCellSize": 3
    , "classBandName": 'class'
    , "referenceMask": ee.Image('users/lealparente/pasture_mask').expression("(b('b1') == 1) ? 1 : 0")
  }
  , "classification": {
      "nTrees": 100
    , "variablesPerSplit": 1
    , "bagFraction": 0.2
    , "minLeafPopulation": 1
  }
  , "filter": {
      "spatial": {
        "enable": False,
        "maxSize": 20,
        "possibleMaxSize": 100,
        "threshold": 0.5
      }
  }
  , "download": {
        "createTask": True
      , "poolSize": 9
      , "poolCheckTime": 60
      , "taskConfig": { "scale": 30, "maxPixels": 1.0E13, "driveFolder": 'pasture' }
  }
}

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Pixel class percentage calculation considering landsat image boundary
def getPctPixels(referenceMask, classValue, gridCell):
  
  classBand = config['trainning']['classBandName']

  total = referenceMask.reduceRegion(reducer=ee.Reducer.count(), geometry=gridCell, scale=30, maxPixels=1.0E13);
  
  classMask = referenceMask.eq(classValue);
  classCount = classMask.mask(classMask).reduceRegion(reducer=ee.Reducer.count(), geometry=gridCell, scale=30, maxPixels=1.0E13)

  nClassCount = ee.Number(ee.Dictionary(classCount).get(classBand));
  nTotal = ee.Number(ee.Dictionary(total).get(classBand));
  
  return nClassCount.divide(nTotal).getInfo()

def getMaxNumClassesPoints(classValues, referenceMask, gridCell, nPoints):

  strategy = config['trainning']['strategy']

  result = []
  totalPct = 0
  
  for i in xrange(len(classValues)):

    if strategy == 'percentage':
      
      classValue = classValues[i];

      if i == len(classValues):
        classPct = 100 - totalPct
      else:
        classPct = getPctPixels(referenceMask, classValue, gridCell);
        totalPct = totalPct + classPct

      if classPct > 0 and classPct < 0.35:
        classPct = 0.35
      elif classPct > 0.65:
        classPct = 0.65

      maxNumClassPoints = math.ceil(nPoints * classPct)
    else:
      maxNumClassPoints = nPoints / len(classValues)

    result.append(maxNumClassPoints)

  return result

def getClassPoints(points, maxNumClassPoints, imageBands, classValue):
  gapfillValue = config['cloud']['gapfillValue']
  classBand = config['trainning']['classBandName']

  filterArray = [ ee.Filter.eq(classBand, classValue) ];
  for band in imageBands:
    if 'ndvi' in band:
       filterArray.append(ee.Filter.neq(band, gapfillValue));

  filterPoints = ee.Filter.And(filterArray);

  return points.filter(filterPoints).limit(maxNumClassPoints)

# Generate a trainning dataset considering two approachs:
# * A priori probability: using getPctPixels method
# * Normal: try to using the same number of samples for all class
def getTrainningDataset(image, imageBands, gridCell, nPoints, seed):
  
  scale = config['trainning']['scale']
  classBand = config['trainning']['classBandName']
  referenceMask = config['trainning']['referenceMask']

  referenceMask = referenceMask.select([0],[classBand]);
  image = image.select(imageBands);
  image = image.addBands(referenceMask);

  classValues = [1,0]
  points = image.sample(numPixels=math.trunc(nPoints * 5), scale=scale, seed=seed, region=gridCell)

  maxNumClassesPoints = getMaxNumClassesPoints(classValues, referenceMask, gridCell, nPoints)

  result = None;

  for i in xrange(len(classValues)):
    
    numClassPoints = 0;
    classValue = classValues[i];
    maxNumClassPoints = maxNumClassesPoints[i];
    
    if maxNumClassPoints > 0:
      classPoints = getClassPoints(points, maxNumClassPoints, imageBands, classValue)
      numClassPoints = classPoints.size().getInfo()
      logger.debug('Samples number for class %s: %s (%s max allow)', classValue, numClassPoints, int(maxNumClassPoints))
      
      if result is None:
        result = classPoints;
      else:
        result = result.merge(classPoints)

    if numClassPoints == 0:
      logger.warning('There isn\'t samples for class %s', classValue)
      return None

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
  
  return mvc, bands;

def preserveCommonBands(array1, array2):
  result = []
  for e1 in array1:
    if e1 in array2:
      result.append(e1);
  return result

def getClassifiers(tile, mvcBandsToClassify, neighborsGridCell):
  
  series = config['mvc']['series']
  nPoints = config['trainning']['nPoints']
  nTrees = config['classification']['nTrees'];
  classBand = config['trainning']['classBandName']
  gridCellSize = config['trainning']['gridCellSize']
  bagFraction = config['classification']['bagFraction'];
  variablesPerSplit = config['classification']['variablesPerSplit'];
  minLeafPopulation = config['classification']['minLeafPopulation'];

  result = []
  mainSerie = series[0]
  trainningBandsAll = None
  trainningDatasetAll = None

  nPointsPart = int(nPoints / (gridCellSize * gridCellSize))

  for i in xrange(len(neighborsGridCell)):
    
    neiGridCellId = neighborsGridCell[i]['id']
    neiGridCellGeom = neighborsGridCell[i]['geom']

    mvc, mvcBands = getMVC(mainSerie, neiGridCellGeom, False);

    if len(mvcBands) == 0:
      continue;

    mvcCommonBands = preserveCommonBands(mvcBands, mvcBandsToClassify)

    key = mainSerie['prefix'] + neiGridCellId
    
    #seedGrid = abs(hash(key + '_grid')) % (10 ** 8)
    seedPart = abs(hash(key + '_part')) % (10 ** 8)

    #trainningDatasetGrid = getTrainningDataset(mvc, mvcCommonBands, neiGridCellGeom, nPoints, seedGrid);
    trainningDatasetPart = getTrainningDataset(mvc, mvcCommonBands, neiGridCellGeom, nPointsPart, seedPart);
    
    #if trainningDatasetGrid is not None:
      #mvcCommonBands.append(classBand)
      #classifier = ee.Classifier.randomForest(nTrees, variablesPerSplit, minLeafPopulation, bagFraction);
      #classifier = classifier.train(trainningDatasetGrid, classBand, mvcCommonBands);
      #mvcCommonBands.remove(classBand);

      #logger.debug('Classifier %s was generate', key)
      #result.append({ 'id': key, 'classifier': classifier, 'bands': mvcCommonBands });
    #else:
      #logger.warning('Classifier %s can\'t be generate. There weren\'t enough samples', key)

    if trainningDatasetPart is not None:
      if trainningBandsAll is None:
        trainningBandsAll = mvcCommonBands;
        trainningDatasetAll = trainningDatasetPart;
      else:
        trainningBandsAll = preserveCommonBands(trainningBandsAll, mvcCommonBands)
        trainningDatasetAll = trainningDatasetAll.merge(trainningDatasetPart)
  
  key = mainSerie['prefix'] + tile + '_' + str(gridCellSize) + 'x' + str(gridCellSize)
  if trainningBandsAll is not None:
    logger.debug('Classifier %s was generate', key)
    
    trainningBandsAll.append(classBand);
    classifier = ee.Classifier.randomForest(nTrees, variablesPerSplit, minLeafPopulation, bagFraction);
    classifier = classifier.train(trainningDatasetAll, 'class', trainningBandsAll);
    trainningBandsAll.remove(classBand);
    result.append({ 'id': key, 'classifier': classifier, 'bands': trainningBandsAll });
  
  else:
    logger.warning('Classifier %s can\'t be generate. There weren\'t enough samples', key)

  return result

# Execute a classification approach
def doClassification(mvc, gridCell, classifiers):
  
  classificationArray = []
  applySpatialFilter = config['filter']['spatial']['enable']
  
  clipedMvc = mvc.clip(gridCell)

  for c in classifiers:
    logger.debug('Executing classifier %s using bands %s', c['id'], ','.join(c['bands']) )
    currentClipedMvc = clipedMvc.select(c['bands'])
    classificationArray.append(currentClipedMvc.classify(c['classifier']))
  
  meanClassification = ee.ImageCollection.fromImages(classificationArray).mean()

  if (applySpatialFilter):
    meanClassification = spatialFilter(meanClassification)

  meanClassification = meanClassification.multiply(10000).toInt16()
  meanClassification = meanClassification.set('system:footprint', mvc.get('system:footprint'))

  return meanClassification

def spatialFilter(classification):

  maxSize = config['filter']['spatial']['maxSize']
  threshold = config['filter']['spatial']['threshold']
  possibleMaxSize = config['filter']['spatial']['possibleMaxSize']

  classMask = classification.gte(threshold)
  labeled = classMask.mask(classMask).connectedPixelCount(possibleMaxSize, True)
  
  region = labeled.lt(maxSize)
  kernel = ee.Kernel.square(1)

  neighs = classification.neighborhoodToBands(kernel).mask(region)
  majority = neighs.reduce(ee.Reducer.mode())
  filtered = classification.where(region, majority)

  return filtered

# Execution control for classification in one grid cell
def run(tile, gridCell, neighborsGridCell):
  
  series  = config['mvc']['series'];
  
  result = {};
  
  mainSerie = series[0]

  logger.debug('Main serie prefix: %s', mainSerie['prefix'])

  timeMergedBands = None

  for serie in series:
    mvc, mvcBands = getMVC(serie, gridCell, False);
    if timeMergedBands is None:
      timeMergedBands = mvcBands
    else:
      print(tile, serie['prefix'], len(timeMergedBands), len(mvcBands))
      timeMergedBands = preserveCommonBands(timeMergedBands, mvcBands)
  
  
  logger.debug('Time merged MVC bands: %s', ','.join(timeMergedBands))

  classifiers = getClassifiers(tile, timeMergedBands, neighborsGridCell)
  logger.info('Classifiers number: %s', len(classifiers))

  if len(classifiers) > 0:
    for serie in series:
      logger.info('Run classification for tile %s', mainSerie['prefix'])
      serieResult = doClassification(mvc, gridCell, classifiers)
      result[serie['prefix'] + tile] = serieResult;
  else:
    logger.warning('Tile %s can\'t be classified', mainSerie['prefix'])

  return result

def getCenterPoint(gridCell):

  lc5 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate('2013-01-01', '2016-01-01').filterBounds(gridCell.centroid());
  lc5 = lc5.getInfo()
  for f in lc5['features']:
    urlPath = ''
    if 'google:cloud_storage_path' in f['properties']:
      urlPath = f['properties']['google:cloud_storage_path']

    cloudCover = -1
    if 'CLOUD_COVER' in f['properties']:
      cloudCover = f['properties']['CLOUD_COVER']

    print f['properties']['LANDSAT_SCENE_ID'], f['properties']['DATE_ACQUIRED'], cloudCover, urlPath

# Control for download pool
def checkPoolState(config, taskPool):
  
  logger.info('The download\'s pool is full... waiting %s secs', config['download']['poolCheckTime'])
  time.sleep(config['download']['poolCheckTime'])

  for task in list(taskPool):
    status = task.status()
    
    taskStatus = status['state']
    taskId = task.config['description']

    if taskStatus in (ee.batch.Task.State.FAILED, ee.batch.Task.State.COMPLETED, ee.batch.Task.State.CANCELLED):
      taskPool.remove(task)
      if('error_message' in status):
        logger.error('Exportation %s %s', taskId, status['error_message'])
      if('error_message' in status and (status['error_message'] == 'User memory limit exceeded.' or status['error_message'] == 'Computation timed out after 600.0 seconds.') ):
        logger.info('Try export classification %s.tif again', taskId)
        reRuntask = ee.batch.Export.image(mapResult[taskId]['result'], taskId, mapResult[taskId]['config'])
        reRuntask.start()
        taskPool.append(reRuntask)
    else:
      logger.info('Exportation %s %s', taskId, taskStatus)

def getGridCell(tile):

  gridCellSize = config['trainning']['gridCellSize']
  incNumber = (gridCellSize - 1) / 2

  path = int(tile[:3])
  row = int(tile[3:])

  result = []

  tAuxArray = []
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
        tAuxArray.append(tAux)
        gridCell = ee.FeatureCollection(config['grid']['ftCollection']) \
          .filter(ee.Filter.eq('TILE_T', 'T'+tAux)) \
          .first() \
          .geometry()
        result.append({ "id": tAux, "geom": gridCell })

  logger.debug('Neighbors tiles: %s', tAuxArray)

  return result

center = None
taskPool = []
mapResult = {}
tileDict = {}

for tile in config['grid']['allTiles']:
  tileDict[tile] = True

for tile in config['grid']['tilesToProcess']:
  
  logger.info('Processing tile %s', tile)

  neighborsGridCell = getGridCell(tile);
 
  execFlag = True
  gridCell = ee.FeatureCollection(config['grid']['ftCollection']) \
    .filter(ee.Filter.eq('TILE_T', 'T'+tile)) \
    .first() \
    .geometry();

  while execFlag:
    try:
      coordList = gridCell.coordinates().getInfo()
      #getCenterPoint(gridCell)
      seriesResult = run(tile, gridCell, neighborsGridCell)
      
      while len(taskPool) >= config['download']['poolSize']:
        checkPoolState(config,taskPool)

      for taskId,serieResult in seriesResult.iteritems():
        taskConfig = config['download']['taskConfig']
        taskConfig['region'] = [coordList[0][0], coordList[0][1], coordList[0][2], coordList[0][3]]

        logger.info('Export classification %s.tif', taskId)
        task = ee.batch.Export.image(serieResult, taskId, taskConfig)
        mapResult[taskId] = { 'result': serieResult, 'config': taskConfig.copy() };
        task.start()

        taskPool.append(task)
      execFlag = False  
    except:
      traceback.print_exc()
      execFlag = True

while len(taskPool) > 0:
  checkPoolState(config,taskPool)