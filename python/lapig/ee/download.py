#!/usr/bin/python

import traceback
import ee
import wget
import zipfile
import os

def bbox2Region(x1, y1, x2, y2):
	return [ [x1, y1],	[x1, y2],	[x2, y1],	[x2, y2] ];

def splitBbox(x1, y1, x2, y2):
	x3 = (x1 + x2) / 2;
	y3 = (y1 + y2) / 2;

	result = [];
	result.append({ 'x1': x1, 'y1': y1, 'x2': x3, 'y2': y3});
	result.append({ 'x1': x1, 'y1': y3, 'x2': x3, 'y2': y2});
	result.append({ 'x1': x3, 'y1': y3, 'x2': x2, 'y2': y2});
	result.append({ 'x1': x3, 'y1': y1, 'x2': x2, 'y2': y3});

	return result;

def unzipFile(filename):
	with zipfile.ZipFile(filename, "r") as z:
		z.extractall(".")

def donwloadTiles(eeImg, scale, crs, bbox, count = 0):
	region = bbox2Region(bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']);
	
	try:
		url = eeImg.getDownloadUrl({ 'scale': scale, 'region': str(region) });
		count = count + 1;

		unziped = None

		while not unziped:
			try:
				print(' # Download tile ' + str(count) + ' from url ' + url);
				fileZip = wget.download(url);

				unzipFile(fileZip);
				unziped = 1;

			except:
				print('Corrupted zip file. We will try download again...\n')
				url = eeImg.getDownloadUrl({ 'scale': scale, 'region': str(region) });

			finally:
				os.remove(fileZip);

	except: 
		traceback.print_exc()
		bboxList = splitBbox(bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']);
		for newBbox in bboxList:
			donwloadTiles( eeImg, scale, crs, newBbox, count);

def mergeBand(imgName, band):
	
	tiles = [];
	oldFiles = [];

	for filename in os.listdir("."):
		if filename.endswith('.' + band + ".tif"):
			
			fileTif = filename
			fileTfw = fileTif.replace('.tif', '.tfw');

			tiles.append(fileTif);

			oldFiles.append(fileTif);
			oldFiles.append(fileTfw);

	print(' # Mege all tif files');
	
	mosaicFilename = imgName + '.' + band + '.tif';
	params = ' -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE -ot Float32 -o ' + mosaicFilename;
	for t in tiles:
		params += ' ' + t;
	
	os.system('gdal_merge.py ' + params);

	"""
	if not os.path.exists('mosaik'):
		os.makedirs('mosaik');

	os.rename(mosaicFilename, 'mosaik/' + mosaicFilename);
	"""

	print(' # Remove ' + str(len(oldFiles)) + 'old files');
	for f in oldFiles:
		os.remove(f);
	

def mergeAll(eeImg, imgName):
	info = eeImg.getInfo();
	for band in info['bands']:
		mergeBand(imgName, band['id']);

def eeImage(eeImg, scale, crs, bbox, imgName):
	print('DOWNLOAD ' + imgName);
	
	donwloadTiles(eeImg, scale, crs, bbox);
	mergeAll(eeImg, imgName);