#!/usr/bin/python

import random
import ogr
import gdal
import sys
import os
import numpy
import csv
import time
import multiprocessing

def randomPointsIn(inputShpPath, nPoints, boundsGeometry = None):

	def checkPoint(pointGeometry):
		minx, maxx, miny, maxy = pointGeometry.GetEnvelope();
		inputLayer.SetSpatialFilterRect(minx, miny, maxx, maxy);

		inputLayer.ResetReading();
		feature = inputLayer.GetNextFeature();

		if feature is None:
			return True
		else:
			if boundsGeometry is not None:
				return not boundsGeometry.Contains(pointGeometry);
			else:
				return False

	def newPoint(lon, lat):
		point = ogr.Geometry(ogr.wkbPoint)
		point.AddPoint(lon, lat)

		return point;

	driver = ogr.GetDriverByName('ESRI Shapefile')

	inputShp = driver.Open(inputShpPath)
	inputLayer = inputShp.GetLayer()
	
	if boundsGeometry is not None:
		minx, maxx, miny, maxy = boundsGeometry.GetEnvelope();
		inputLayer.SetSpatialFilterRect(minx, miny, maxx, maxy);

		inputLayer.ResetReading();
		count = inputLayer.GetFeatureCount();
		
		resultGeometry = ogr.Geometry(ogr.wkbPolygon);
		print(count);
		for i in xrange(count):
			print(i)
			feature = inputLayer.GetNextFeature();
			geometry = feature.GetGeometryRef();
			tmpUnion = resultGeometry.Union(geometry);
			if tmpUnion is not None:
				resultGeometry = tmpUnion

		minx, maxx, miny, maxy = resultGeometry.GetEnvelope();
		print(boundsGeometry.GetEnvelope());
		print(minx, maxx, miny, maxy);
	else:
		minx, maxx, miny, maxy = inputLayer.GetEnvelope();
	
	randomPoints = [];

	for i in xrange(nPoints):

		pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))
		while checkPoint(pointGeometry):
			pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))

		randomPoint = { 'geometry': pointGeometry }
		randomPoints.append(randomPoint);

	return randomPoints;

def randomPointsOut(inputShpPath, nPoints, boundsGeometry = None):

	def checkPoint(pointGeometry):
		minx, maxx, miny, maxy = pointGeometry.GetEnvelope();
		inputLayer.SetSpatialFilterRect(minx, miny, maxx, maxy);

		inputLayer.ResetReading();
		feature = inputLayer.GetNextFeature();

		if feature is None:
			if boundsGeometry is not None:
				return not boundsGeometry.Contains(pointGeometry);
			else:
				return False
		else:
			return True

	def newPoint(lon, lat):
		point = ogr.Geometry(ogr.wkbPoint)
		point.AddPoint(lon, lat)

		return point;

	driver = ogr.GetDriverByName('ESRI Shapefile')

	inputShp = driver.Open(inputShpPath)
	inputLayer = inputShp.GetLayer()
	
	if boundsGeometry is not None:
		minx, maxx, miny, maxy = boundsGeometry.GetEnvelope();
	else:
		minx, maxx, miny, maxy = inputLayer.GetEnvelope();
	
	randomPoints = [];

	for i in xrange(nPoints):

		pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))
		while checkPoint(pointGeometry):
			pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))

		randomPoint = { 'geometry': pointGeometry }
		randomPoints.append(randomPoint);

	return randomPoints;

def randomPoints(inputShpPath, nPoints, boundsGeometry = None, attributeFilter = None):

	def newPoint(lon, lat):
		point = ogr.Geometry(ogr.wkbPoint)
		point.AddPoint(lon, lat)

		return point;

	driver = ogr.GetDriverByName('ESRI Shapefile')

	inputShp = driver.Open(inputShpPath)
	inputLayer = inputShp.GetLayer()

	if attributeFilter is not None:
		inputLayer.SetAttributeFilter(attributeFilter)
	
	if boundsGeometry is not None:
		minx, maxx, miny, maxy = boundsGeometry.GetEnvelope();
		inputLayer.SetSpatialFilterRect(minx, miny, maxx, maxy);

	randomPoints = []
	featureCount = inputLayer.GetFeatureCount();

	for i in xrange(nPoints):

		randomFeature=None

		while randomFeature is None:
			try:
				randomFeatureIndex = int(featureCount * random.random());
				inputLayer.SetNextByIndex(randomFeatureIndex);

				randomFeature = inputLayer.GetNextFeature();
				
				while not randomFeature is None and not randomFeature.GetGeometryRef().Intersects(boundsGeometry):
					try:
						randomFeature = inputLayer.GetNextFeature();
					except:
						randomFeature = None;

			except:
				traceback.print_exc()
				randomFeature=None

		featureGeometryClipped = randomFeature.GetGeometryRef().Intersection(boundsGeometry);

		minx, maxx, miny, maxy = featureGeometryClipped.GetEnvelope();

		pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))
		while not featureGeometryClipped.Contains(pointGeometry):
			pointGeometry = newPoint(minx + (random.random() * (maxx-minx)), (miny + (random.random() * (maxy-miny))))

		randomPoint = { 'geometry': pointGeometry }
		randomPoints.append(randomPoint);

	return randomPoints;

def readPoints(inputShpPath):

	def newPoint(lon, lat):
		point = ogr.Geometry(ogr.wkbPoint)
		point.AddPoint(lon, lat)

		return point;
	
	driver = ogr.GetDriverByName('ESRI Shapefile')

	inputShp = driver.Open(inputShpPath)
	inputLayer = inputShp.GetLayer()
	
	featureCount = inputLayer.GetFeatureCount();

	points = [];
	for i in range(featureCount):
		feature = inputLayer.GetNextFeature();
		geometry = feature.GetGeometryRef();
		points.append({ 'geometry': newPoint(geometry.GetX(), geometry.GetY()) });

	return points;

def randomPixels(inputImgPath, pixelValueThreshold, nPoints, boundsGeometry):
	inputImg = gdal.Open(inputImgPath)
	inputBand = inputImg.GetRasterBand(1);
	
	randomPoints = [];
	windowSize = 1;
	xSize = inputImg.RasterXSize;
	ySize = inputImg.RasterYSize;
	xoff, a, b, yoff, d, e = inputImg.GetGeoTransform();

	def pixel2LatLon(x, y):
		xp = a * x + b * y + xoff
		yp = d * x + e * y + yoff

		xp += a / 2.0
		yp += e / 2.0

		return { 'lon': xp, 'lat': yp };
	
	def randomXY():
		randomX = int(random.random() * (xSize - windowSize));
		randomY = int(random.random() * ySize);
		
		return { "x": randomX, "y": randomY };

	def wherePixelValue():
		rxy = randomXY();

		randomPixels = inputBand.ReadAsArray(rxy['x'], rxy['y'], windowSize, 1).astype(numpy.float)[0]
		result = numpy.where( randomPixels >= pixelValueThreshold )[0];
		return { 'index': result, 'pixels': randomPixels, 'rxy': rxy };
	
	while len(randomPoints) < nPoints:

		result = wherePixelValue();

		while len(result['index']) == 0:
			result = wherePixelValue();

		for i in result['index']:
			pixelX = result['rxy']['x'] + i;
			pixelY = result['rxy']['y'];

			lonLat = pixel2LatLon(pixelX, pixelY);

			if len(randomPoints) == nPoints:
				break;

			pointGeometry = ogr.Geometry(ogr.wkbPoint)
			pointGeometry.SetPoint_2D(0, lonLat['lon'], lonLat['lat'])

			if boundsGeometry.Contains(pointGeometry):
				print(len(randomPoints))
				randomPoint = { 'pixelValue': result['pixels'][i], 'geometry': pointGeometry }
				randomPoints.append(randomPoint);

	return randomPoints;

def shpContainsPoints(inputShpPath, points):
	driver = ogr.GetDriverByName('ESRI Shapefile')
	
	inputShp = driver.Open(inputShpPath)
	inputLayer = inputShp.GetLayer()

	result = { 'in': 0, 'not': 0 }

	for point in points:
		minx, maxx, miny, maxy = point['geometry'].GetEnvelope();
		inputLayer.SetSpatialFilterRect(minx, miny, maxx, maxy);
		
		inputLayer.ResetReading();
		feature = inputLayer.GetNextFeature();

		if feature is None:
			result['not'] += 1;
			point['check'] = 'not';
		else:
			result['in'] += 1;
			point['check'] = 'in';

	return result;

def pixelValuesPoints(inputImgPath, pixelValueThreshold, points):
	inputImg = gdal.Open(inputImgPath)
	inputBand = inputImg.GetRasterBand(1);

	xoff, a, b, yoff, d, e = inputImg.GetGeoTransform();

	result = { 'in': 0, 'not': 0 }

	for point in points:
		px = int((point['geometry'].GetX() - xoff) / a)
		py = int((point['geometry'].GetY() - yoff) / e)

		try:
			pixelValue = inputBand.ReadAsArray(px, py, 1, 1)[0][0];
		except:
			pixelValue = 0

		if pixelValue < pixelValueThreshold:
			result['not'] += 1;
			point['check'] = 'not';
		else:
			result['in'] += 1;
			point['check'] = 'in';
	
	return result;

def points2Shp(outputShpPath, points):
	
	try:
		os.remove(outputShpPath);
	except:
		pass

	driver = ogr.GetDriverByName('ESRI Shapefile')

	fields = []
	firstPoint = points[0];
	for key in firstPoint:
		if key != 'geometry':
			fields.append(key);

	output_file = driver.CreateDataSource(outputShpPath)
	output_layer = output_file.CreateLayer("point_out", None, ogr.wkbPoint )

	for field in fields:
		field_name = ogr.FieldDefn(field, ogr.OFTString)
		output_layer.CreateField(field_name)

	for point in points:
		feat = ogr.Feature(output_layer.GetLayerDefn())
		feat.SetGeometry(point['geometry']);
		
		for field in fields:
			feat.SetField(field, point[field] )

		output_layer.CreateFeature(feat)

def result2Csv(outputCsvPath, result, omission, commission, onlyOmission):

	resultFile = open(outputCsvPath, 'wt');
	resultWriter = csv.writer(resultFile);

	resultWriter.writerow(['', 'Classification']);
	resultWriter.writerow(['', 'Pasture', 'Not-pasture', 'Error']);
	resultWriter.writerow(['Pasture', result['true_positive'], result['false_negative'], omission]);
	if not onlyOmission:
		resultWriter.writerow(['Not-pasture', result['false_positive'], result['true_negative'], commission]);

	resultFile.close();

def totalError2Csv(outputCsvPath, totalError):
	resultFile = open(outputCsvPath, 'wt');
	resultWriter = csv.writer(resultFile);

	for row in totalError:
		resultWriter.writerow(row);

	resultFile.close();

def confusionMatrix(inputImg, inputShpPath, nPoints, pixelValueThresholds, boundsGeometry, basename, fixedShpPoints=False, validationShpPoints=None, onlyOmission=False):

	if not isinstance(pixelValueThresholds, list):
		pixelValueThresholds = [pixelValueThresholds];

	shpRandomPoints=None
	totalError = [];
	totalError.append([ '' ]);
	totalError.append([ 'omission' ]);
	totalError.append([ 'commission' ]);

	driver = ogr.GetDriverByName('ESRI Shapefile')

	inputShp2 = driver.Open('/data/lapig/GEO/CLASSIFICATION/PASTURE/INPUT/VALIDATION/DATASET_05/POLYGON_VALIDATION_GAPFILL.shp')
	inputLayer2 = inputShp2.GetLayer()
	
	minx, maxx, miny, maxy = boundsGeometry.GetEnvelope();
	inputLayer2.SetSpatialFilterRect(minx, miny, maxx, maxy);

	inputLayer2.ResetReading();
	count = inputLayer2.GetFeatureCount();
	
	resultGeometry = ogr.Geometry(ogr.wkbPolygon);
	#print(count);
	for i in xrange(count):
		#print(i)
		feature = inputLayer2.GetNextFeature();
		geometry = feature.GetGeometryRef();
		resultGeometry = resultGeometry.Union(geometry);

	for pixelValueThreshold in pixelValueThresholds:
		
		if not fixedShpPoints or shpRandomPoints is None:
			if validationShpPoints is None:
				print( "  {0} {1}% {2}points randomPoints".format( time.strftime("%H:%M:%S"),pixelValueThreshold,nPoints ) );
				shpRandomPoints = randomPointsIn(inputShpPath, nPoints, boundsGeometry)
			else:
				shpRandomPoints = readPoints(validationShpPoints)
				nPoints = len(shpRandomPoints)

		print( "  {0} {1}% {2}points pixelValuesPoints".format( time.strftime("%H:%M:%S"),pixelValueThreshold,nPoints ) );
		resultShpAnalisys = pixelValuesPoints(inputImg, pixelValueThreshold, shpRandomPoints);

		result = {};
		
		result["true_positive"] = resultShpAnalisys["in"];
		result["false_negative"] = resultShpAnalisys["not"];
		omission = float(result['false_negative']) / (float(result['true_positive']) + float(result['false_negative']));
		totalError[0].append(pixelValueThreshold);
		totalError[1].append(omission);
		
		points2Shp(basename + '_V' + str(pixelValueThreshold) + '_SHP_POINTS.shp', shpRandomPoints);

		commission = 'NULL';
		if not onlyOmission:
			print( "  {0} {1}% {2}points randomPixels".format( time.strftime("%H:%M:%S"),pixelValueThreshold,nPoints ) );
			imgRandomPoints = randomPixels(inputImg, pixelValueThreshold, nPoints, resultGeometry);
			
			print( "  {0} {1}% {2}points shpContainsPoints".format( time.strftime("%H:%M:%S"),pixelValueThreshold,nPoints ) );
			resultImgAnalisys = shpContainsPoints(inputShpPath, imgRandomPoints);

			result["false_positive"] = resultImgAnalisys['not'];
			result["true_negative"] = resultImgAnalisys['in'];
			commission = float(result['false_positive']) / (float(result['false_positive']) + float(result['true_negative']));
			totalError[2].append(commission);
			points2Shp(basename + '_V' + str(pixelValueThreshold) + '_IMG_POINTS.shp', imgRandomPoints);

		result2Csv(basename + '_V' + str(pixelValueThreshold) + '_ERROR_MATRIX.csv', result, omission, commission, onlyOmission)

	totalError2Csv(basename + '_TOTAL_ERROR.csv', totalError)

