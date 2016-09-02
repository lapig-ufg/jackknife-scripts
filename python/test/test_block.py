import gdal
import numpy
import traceback
import glob
import os

def test(raster):
	i = 0
	countStat = []
	maxStat = []
	minStat = []
	meanStat = []
	while True:
		try:
			data = readBlock(raster, 1, i, 256)
			data = numpy.array(data.astype(numpy.float32))
			
			count = len(data.flatten());
			countStat.append(count)
			
			data = data[numpy.where(data != 0)]
			count = len(data.flatten());

			if count > 0:
				maxStat.append(numpy.max(data))
				minStat.append(numpy.min(data))
				meanStat.append(numpy.average(data))
				print(i)
			
			i += 1

		except:
			print(traceback.format_exc())
			break

	print('COUNT: ', str(numpy.sum(countStat)))
	print('MAX: ', str(numpy.max(maxStat)))
	print('MIN: ', str(numpy.min(minStat)))
	print('MEAN: ', str(numpy.average(meanStat)))

	#STATISTICS_MAXIMUM=1.1944754123688
	#STATISTICS_MEAN=0.41143873996396
	#STATISTICS_MINIMUM=-0.16459989547729
	#STATISTICS_STDDEV=0.14231428425098

def readBlock(raster, band, i, blockSize):

	xSize = raster.RasterXSize
	ySize = raster.RasterYSize

	colBlocks = (xSize / blockSize)
	lastXBlockSize = xSize % blockSize
	if lastXBlockSize > 0:
		colBlocks += 1
		
	rowBlocks = (ySize / blockSize)
	lastRowBlockSize = ySize % blockSize
	if lastRowBlockSize > 0:
		rowBlocks += 1

	maxBlocks = colBlocks * rowBlocks

	if maxBlocks <= i:
		msg = 'Invalid block, there are only ' + str(maxBlocks) + ' blocks'
		raise ValueError(msg)

	colI = i % colBlocks

	if (i >= colBlocks):
		rowI = i / colBlocks
	else:
		rowI = 0

	xBlockSizeI = blockSize
	if (colI == (colBlocks - 1) and lastXBlockSize > 0):
		xBlockSizeI = lastXBlockSize
	
	rowBlockSizeI = blockSize
	if (rowI == (rowBlocks - 1) and lastRowBlockSize > 0):
		rowBlockSizeI = lastRowBlockSize

	rasterBand = raster.GetRasterBand(band)
	return rasterBand.ReadAsArray(colI * blockSize, rowI * blockSize, xBlockSizeI, rowBlockSizeI)

def readBlockFromImages(files, band, i, blockSize):
	result = []

	for file in files:
	  print(file)
	  data = readBlock(gdal.Open(file), band, i, blockSize)
	  data = numpy.array(data.astype(numpy.float16))
	  result.append(data)

	return result;

os.chdir("/data/lapig/TMP/Bernard_GAP/BRASIL/EVI2/")
evi2Files = sorted(glob.glob("EVI2_BRASIL*.tif"))
flagFiles = sorted(glob.glob("EVI2_flag_BRASIL*.tif"))

evi2Blocks = readBlockFromImages(evi2Files, 1, 2500, 256);
flagBlocks = readBlockFromImages(flagFiles, 1, 2500, 256);

print(evi2Blocks)
print(flagBlocks)