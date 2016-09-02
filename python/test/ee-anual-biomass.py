#!/usr/bin/python

import math
import time
import json
import ee
import traceback

# BR '001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068'
# CERRADO '226069','227069','226070','227070','219068','229069','221069','216070','232063','226057','231058','224078','218077','225059','225061','224082','225077','225060','232062','233057','226060','231064','231063','229063','229061','224061','233068','223060','230064','233058','229065','229064','226061','228062','221067','232069','233065','215069','229062','231060','215063','220062','220079','231062','228064','226065','220077','230063','223079','215073','226066','221061','227064','220065','231065','226063','227073','227062','231069','228061','219077','229066','226072','221078','228066','233066','231059','226064','215074','227066','225076','230067','224079','225080','227061','221068','218067','225068','221071','220075','220081','227065','228069','219074','232066','229068','219070','224062','225065','223068','227069','222061','216064','226068','217068','220063','215066','223062','222076','226074','226071','224076','224063','218073','225064','220074','216068','221073','222069','222070','214067','221075','222083','230069','222079','221062','216072','221081','225073','217069','218069','225075'

ee.Initialize()

config = {
    "grid": {
      #"tiles": ['226069','227069','226070','227070','219068','229069','221069','216070','232063','226057','231058','224078','218077','225059','225061','224082','225077','225060','232062','233057','226060','231064','231063','229063','229061','224061','233068','223060','230064','233058','229065','229064','226061','228062','221067','232069','233065','215069','229062','231060','215063','220062','220079','231062','228064','226065','220077','230063','223079','215073','226066','221061','227064','220065','231065','226063','227073','227062','231069','228061','219077','229066','226072','221078','228066','233066','231059','226064','215074','227066','225076','230067','224079','225080','227061','221068','218067','225068','221071','220075','220081','227065','228069','219074','232066','229068','219070','224062','225065','223068','227069','222061','216064','226068','217068','220063','215066','223062','222076','226074','226071','224076','224063','218073','225064','220074','216068','221073','222069','222070','214067','221075','222083','230069','222079','221062','216072','221081','225073','217069','218069','225075'],
      "tiles": ['223071', '221073'],
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
          "indexes": [
               { "id": "ndvi", "expression": "(b('B5') - b('B4')) / (b('B5') + b('B4'))" }  
            ,  { "id": "biomass", "expression": "16.1379 * pow(2.718281, ((5.9111 * (2.5 * ( (b('B5') - b('B4')) / (b('B5') + (2.4 * b('B4')) + 1)  )))))" }  
          ],
          "composites": [
              { "id": "out", "dates": [ { "start": "2013-10-01", "end": "2013-10-31" }, { "start": "2014-10-01", "end": "2014-10-31" } ] }
            , { "id": "nov", "dates": [ { "start": "2013-11-01", "end": "2013-11-30" }, { "start": "2014-11-01", "end": "2014-11-30" } ] }
            , { "id": "dez", "dates": [ { "start": "2013-12-01", "end": "2013-12-31" }, { "start": "2014-12-01", "end": "2014-12-31" } ] }
            , { "id": "jan", "dates": [ { "start": "2014-01-01", "end": "2014-01-31" }, { "start": "2015-01-01", "end": "2015-01-31" } ] }
            , { "id": "fev", "dates": [ { "start": "2014-02-01", "end": "2014-02-28" }, { "start": "2015-02-01", "end": "2015-02-28" } ] }
            , { "id": "mar", "dates": [ { "start": "2014-03-01", "end": "2014-03-31" }, { "start": "2015-03-01", "end": "2015-03-31" } ] }
            , { "id": "abr", "dates": [ { "start": "2013-04-01", "end": "2013-04-30" }, { "start": "2014-04-01", "end": "2014-04-30" } ] }
          ]
        }
      ]
  }
  , "cloud": {
      "cloudCoverThreshold": 60
    , "eeThreshold": 40
    , "bqaThreshold": 53248
    , "gapfillValue": 0
  }
  , "mask": {
      "pasture": ee.Image("users/lealparente/pasture_mask")
  }
}

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
      print(indexName(index['id']))
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

  return mvc;

def run(gridCell):
  
  gapfillValue = config['cloud']['gapfillValue']
  serie = config['mvc']['series'][0];
  composites = serie['composites'];
  pastureMask = config['mask']['pasture']

  mask = pastureMask.eq(1).clip(gridCell);
  mvc = getMVC(serie, gridCell, False);
  
  biomassAnual = mvc.select('biomass-' + composites[0]['id']);
  biomassError = ee.Image(0).add(biomassAnual.eq(gapfillValue));

  for i in xrange(1,len(composites)):
    c = composites[i];
    cPrev = composites[i-1];
    
    cBiomass = mvc.select('biomass-' + c['id']);
    cPrevBiomass = mvc.select('biomass-' + cPrev['id']);
    
    cError = cBiomass.eq(gapfillValue);

    cBiomass = cBiomass.subtract(cPrevBiomass);
    cBiomassMask = cBiomass.gte(0);
    cBiomass = cBiomass.mask(cBiomassMask);
    cBiomass = cBiomass.unmask(0);

    biomassAnual = biomassAnual.add(cBiomass);
    biomassError = biomassError.add(cError);
  
  biomassAnual = biomassAnual.select([0],['b1'])
  biomassAnual = biomassAnual.addBands(biomassError.select([0],['error']))
  biomassAnual = biomassAnual.mask(mask);
    
  return biomassAnual;

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
      if('error_message' in status and status['error_message'] != 'Error: no valid training data were found.'):
        print(task.config['description'], 'Re-run task')
        reRuntask = ee.batch.Export.image(mapResult[task.id], task.id, task.config)
        taskPool.append(reRuntask)

center = None
taskPool = []
mapResult = {}

for tile in config['grid']['tiles']:
  
  execFlag = True
  gridCell = ee.FeatureCollection(config['grid']['ftCollection']) \
    .filter(ee.Filter.eq('TILE_T', 'T'+tile)) \
    .first() \
    .geometry();

  while execFlag:
    try:
      coordList = gridCell.coordinates().getInfo()
      biomassAnual = run(gridCell)
      taskId = tile
      
      while len(taskPool) >= config['download']['poolSize']:
        checkPoolState(config,taskPool)

      print(taskId);
      taskConfig = config['download']['taskConfig']
      taskConfig['region'] = [coordList[0][0], coordList[0][1], coordList[0][2], coordList[0][3]]

      print("Starting task " + taskId)
      task = ee.batch.Export.image(biomassAnual, taskId, taskConfig)
      mapResult[taskId] = biomassAnual;
      task.start()

      taskPool.append(task)
      execFlag = False
        
    except:
      traceback.print_exc()
      execFlag = True

while len(taskPool) > 0:
  checkPoolState(config,taskPool)