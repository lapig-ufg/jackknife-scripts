import sys, os
import datetime
import gdal, ogr, osr
import numpy as np
import time
from scipy.ndimage import median_filter

import glob
from os.path import join, exists

def createOutputImage(referenceFile, outputFile, data, imageFormat = 'GTiff'):
  
  driver = gdal.GetDriverByName(imageFormat)
  referenceDs = gdal.Open(referenceFile)
  referenceBand = referenceDs.GetRasterBand(1)
  xSize = referenceDs.RasterXSize
  ySize = referenceDs.RasterYSize

  originX, pixelWidth, _, originY, _, pixelHeight  = referenceDs.GetGeoTransform()

  outRasterSRS = osr.SpatialReference()
  outRasterSRS.ImportFromWkt(referenceDs.GetProjectionRef())

  #print("Creating " + outputFile + " ("+str(xSize)+"x"+str(ySize)+")")
  outRaster = driver.Create(outputFile, xSize, ySize, 1, referenceBand.DataType, [ 'COMPRESS=LZW' ])
  outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
  outRaster.SetProjection(outRasterSRS.ExportToWkt())
  rasterBand = outRaster.GetRasterBand(1)
  rasterBand.WriteArray(data)
  rasterBand.FlushCache()

  return outRaster

def readData(inputFiles):
  
  result = []

  ds = gdal.Open(inputFiles[0])
  Xsize = ds.RasterXSize
  Ysize = ds.RasterYSize

  for inputFile in inputFiles:
    ds = gdal.Open(inputFile)
    rasterBand = ds.GetRasterBand(1)
    dataraster = rasterBand.ReadAsArray(0, 0, Xsize, Ysize)
    result.append(dataraster)

  return np.stack(result)

def writeData(outputBaseDir, inputFiles, outputData):
    
  referenceFile = inputFiles[0]

  for i in range(0, len(inputFiles)):
    inputFile = os.path.basename(inputFiles[i])
    year = inputFile[0:4]
    outputDir = outputBaseDir + year

    if not os.path.exists(outputDir):
      try:
        os.makedirs(outputDir)
      except:
        pass

    outputfile = outputDir + '/' + inputFile.replace('.tif', '_tsmedian.tif')

    data = outputData[i ,:,:]
    outRaster = createOutputImage(referenceFile, outputfile, data)

def applyFilter(data):
  return median_filter(data, size=(5,3,3), mode="mirror")

def log(*arg):
  
  dateStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  msgList = list(arg)
  msgList = [var for var in msgList if var]
  msg = " ".join(msgList)

  identifier=str(currentTile)
  print("{dateStr} [{identifier}] {msg}".format(dateStr=dateStr, identifier=identifier, msg=msg))

def formatTime(timeValue):
  return str(round( (timeValue),2))

inputDir = '/data/DADOS_GRID/run_median_filter/pastagem_col4/'
#inputDir = '/data/PASTAGEM/Mapeamento/MapBiomas/Versions/v4.0/GLC/pastagem_col4/'
outputDir = '/data/SENTINEL/PASTURE_COL4/'

tiles = ['001057','001058','001059','001060','001061','001062','001063','001064','001065','001066','001067','002057','002059','002060','002061','002062','002063','002064','002065','002066','002067','002068','003058','003059','003060','003061','003062','003063','003064','003065','003066','003067','003068','004059','004060','004061','004062','004063','004064','004065','004066','004067','005059','005060','005063','005064','005065','005066','005067','006063','006064','006065','006066','214064','214065','214066','214067','215063','215064','215065','215066','215067','215068','215069','215070','215071','215072','215073','215074','216063','216064','216065','216066','216067','216068','216069','216070','216071','216072','216073','216074','216075','216076','217062','217063','217064','217065','217066','217067','217068','217069','217070','217071','217072','217073','217074','217075','217076','218062','218063','218064','218065','218066','218067','218068','218069','218070','218071','218072','218073','218074','218075','218076','218077','219062','219063','219064','219065','219066','219067','219068','219069','219070','219071','219072','219073','219074','219075','219076','219077','220062','220063','220064','220065','220066','220067','220068','220069','220070','220071','220072','220073','220074','220075','220076','220077','220078','220079','220080','220081','221061','221062','221063','221064','221065','221066','221067','221068','221069','221070','221071','221072','221073','221074','221075','221076','221077','221078','221079','221080','221081','221082','221083','222061','222062','222063','222064','222065','222066','222067','222068','222069','222070','222071','222072','222073','222074','222075','222076','222077','222078','222079','222080','222081','222082','222083','223060','223061','223062','223063','223064','223065','223066','223067','223068','223069','223070','223071','223072','223073','223074','223075','223076','223077','223078','223079','223080','223081','223082','224060','224061','224062','224063','224064','224065','224066','224067','224068','224069','224070','224071','224072','224073','224074','224075','224076','224077','224078','224079','224080','224081','224082','225058','225059','225060','225061','225062','225063','225064','225065','225066','225067','225068','225069','225070','225071','225072','225073','225074','225075','225076','225077','225080','225081','226057','226058','226059','226060','226061','226062','226063','226064','226065','226066','226067','226068','226069','226070','226071','226072','226073','226074','226075','227058','227059','227060','227061','227062','227063','227064','227065','227066','227067','227068','227069','227070','227071','227072','227073','227074','227075','228058','228059','228060','228061','228062','228063','228064','228065','228066','228067','228068','228069','228070','228071','228072','229058','229059','229060','229061','229062','229063','229064','229065','229066','229067','229068','229069','229070','229071','230059','230060','230061','230062','230063','230064','230065','230066','230067','230068','230069','231057','231058','231059','231060','231061','231062','231063','231064','231065','231066','231067','231068','231069','232056','232057','232058','232059','232060','232061','232062','232063','232064','232065','232066','232067','232068','232069','233057','233058','233059','233060','233061','233062','233063','233064','233065','233066','233067','233068','220082']


tileIdx = int(sys.argv[1])-1
currentTile = tiles[tileIdx]

log("Starting")

inputFiles = sorted(glob.glob( join(inputDir, '*',  '*' + currentTile + '*.tif') ), reverse=True)

print(inputFiles)

if len(inputFiles) != 34:
  log("Wrong images number: " + str(len(inputFiles)))

gdal.SetCacheMax(2**30)

readingTime = time.time()
data = readData(inputFiles)
readingTime = (time.time() - readingTime)

log(' Data read time: ', formatTime(readingTime), 'segs')

if np.sum(data) != 0:
  
  print('Input data:' + str(data.shape))

  filterTime = time.time()
  dataFiltered = applyFilter(data)
  #dataFiltered = data
  filterTime = (time.time() - filterTime)

  log(' Filter application time: ', formatTime(filterTime), 'segs')
  print('Output data:' + str(dataFiltered.shape))

  writingTime = time.time()
  writeData(outputDir, inputFiles, dataFiltered)
  writingTime = (time.time() - writingTime)

  log(' Data write time: ', formatTime(writingTime), 'segs')
  log(' CPU/IO relation: ', str(filterTime / (readingTime+writingTime)) )
  log(' Total time:', str(filterTime+readingTime+writingTime))
  
else:
  log(" Only zero values")

log("Finished")