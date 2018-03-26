#!/usr/bin/python

from osgeo import gdal
from rios import applier
from rios import fileinfo
import sys
import numpy as np

infiles = applier.FilenameAssociations()
outfiles = applier.FilenameAssociations()
otherargs = applier.OtherInputs()

infiles.blue = './data/blue.vrt'
infiles.green = './data/green.vrt'
infiles.red = './data/red.vrt'
infiles.nir = './data/nir.vrt'

outfiles.blue = './data/normalized_blue.img'
outfiles.green = './data/normalized_green.img'
outfiles.red = './data/normalized_red.img'
outfiles.nir = './data/normalized_nir.img'

#calc stats values to each image (bands) present in GeoTIFF file and return a list
def stats(filename, nodata):
	ret = []
	gtif = gdal.Open(filename)
	for i in range(1,gtif.RasterCount+1):
		image = gtif.GetRasterBand(i) #GeoTIFF semantic: one image per band
		image.SetNoDataValue(nodata)
		stats = image.ComputeStatistics(False)
		median = np.median(image.ReadAsArray())
		ret.append({
			'min':stats[0],
			'max': stats[1],
			'mean': stats[2],
			'stddev': stats[3],
			'median': median,
			'inputNodata': nodata
			})
	return ret
 
#Constraint: outputNodata value must be out of [-2,2]
def normalize(block, stats, outputNodata):
	block = block.astype('Float32',copy=False)
	mask = block == stats['inputNodata']
	block[mask] = outputNodata
	block[~mask] = block[~mask]
	block[~mask] = 2 * ((block[~mask] - stats['min']) / (stats['max'] - stats['min'])) - 1
	normalized_median = 2 * ((stats['median'] - stats['min']) / (stats['max'] - stats['min'])) - 1
	block[~mask] -= normalized_median
	return block

def parallel_normalize(info, inputs, outputs, otherargs):	
	nbands = inputs.red.shape[0] #assuming all files have the same number of bands
	outputs.red = np.empty(inputs.red.shape,dtype='Float32')
	outputs.green = np.empty(inputs.green.shape,dtype='Float32')
	outputs.blue = np.empty(inputs.blue.shape,dtype='Float32')
	outputs.nir = np.empty(inputs.nir.shape,dtype='Float32')
	for i in range(nbands):
		outputs.red[i] = normalize(inputs.red[i],otherargs.red_stats[i],otherargs.output_nodata)
		outputs.green[i] = normalize(inputs.green[i],otherargs.green_stats[i],otherargs.output_nodata)
		outputs.blue[i] = normalize(inputs.blue[i],otherargs.blue_stats[i],otherargs.output_nodata)
		outputs.nir[i] = normalize(inputs.nir[i],otherargs.nir_stats[i],otherargs.output_nodata)
	print("Processing status " + str(info.getPercent()) + "%")

otherargs.output_nodata = -3
otherargs.blue_stats 	= stats(infiles.blue,0)
otherargs.green_stats 	= stats(infiles.green,0)
otherargs.red_stats 	= stats(infiles.red,0)
otherargs.nir_stats 	= stats(infiles.nir,0)

controls = applier.ApplierControls()
controls.setNumThreads(4)
controls.setJobManagerType('multiprocessing')
applier.apply(parallel_normalize, infiles, outfiles, otherargs, controls=controls)