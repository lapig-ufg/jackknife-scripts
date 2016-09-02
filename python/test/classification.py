#!/usr/bin/python

import ee
import os
import ogr
import osr
import gdal
import time
import math
import argparse
import ee.mapclient

from string import ascii_uppercase
from multiprocessing import Pool
from subprocess import call

from lapig.classification import garsect2
from lapig.classification import randompoints
from lapig.ee import newmvc
from lapig.ee import download


VERSION='1.0'
MAXPROCS = 4
CONFIG = {
		"BASEPATH": "/data/lapig/GEO/CLASSIFICATION/PASTURE/",
		"TEMPPATH": "/data/tmpfs/"
}

class Classification:

	def __init__(self, properties):
		
		self.mvcNullValue = 0;

		self.geoDB = {
				"ds": {}
			,	"layers": {}
			,	"drivers": { "shp": ogr.GetDriverByName('ESRI Shapefile') },
		}

		for key, value in vars(properties).iteritems():
			#print(key, value);
			setattr(self, key, value)

		self.pctClassAttribute = 'PCT_Past'
		self.runtimeDataset = "{0}_{1}_{2}_{3}".format(self.mvcDataset, self.trainningDataset, self.validationDataset, self.nTreeRandomForest);

		self.createDirIfNotExists( self.basepath('OUTPUT', self.runtimeDataset, 'CLASSIFICATION') )
		self.createDirIfNotExists( self.basepath('OUTPUT', self.runtimeDataset, 'VALIDATION') )

	def getCurrentTime(self):
		return time.strftime("%d/%m/%Y - %H:%M:%S");

	def createDirIfNotExists(self, dir):
		if not os.path.exists(dir):
			os.makedirs(dir)

	def joinDirs(self, basepath, dirs):
		return os.path.join(basepath, dirs)

	def temppath(self, *dirs):
		return os.path.join(CONFIG['TEMPPATH'], *dirs)

	def basepath(self, *dirs):
		return os.path.join(CONFIG['BASEPATH'], *dirs)

	def getGrid(self, filepath):
		if filepath not in self.geoDB['layers']:

			self.geoDB['ds'][filepath] = self.geoDB['drivers']['shp'].Open(filepath);
			self.geoDB['layers'][filepath] = self.geoDB['ds'][filepath].GetLayer();

			if self.tiles is not None:
				strTiles = "'" + self.tiles.replace(",", "','") + "'";
				attributeFilter = "{0} IN ({1})".format(self.tileAttribute, strTiles);
				self.geoDB['layers'][filepath].SetAttributeFilter(attributeFilter);

		return self.geoDB['layers'][filepath];

	def getGridClassification(self):
		return self.getGrid( self.basepath('INPUT', 'GRID', 'CLASSIFICATION_GRID.shp') ); 

	def getGridDownload(self):
		return self.getGrid( self.basepath('INPUT', 'GRID', 'DOWNLOAD_GRID.shp') ); 

	def getMvcFile(self, tile):
		mvcDataset = "DATASET_{0}".format(self.mvcDataset);
		mvcFilename = "{0}_G{1}_MVC.tif".format(tile, self.gapfill.zfill(2));
		return self.basepath('INPUT', 'MVC', mvcDataset, mvcFilename);

	def download(self):

		ee.Initialize();

		gridDownload = self.getGridDownload();
		tilesCount = gridDownload.GetFeatureCount();

		for i in xrange(tilesCount):
			feature = gridDownload.GetNextFeature();

			x1, x2, y1, y2 = feature.geometry().GetEnvelope();
			tile = feature.GetFieldAsString(self.tileAttribute);

			print( "{0} Tile {1}".format(time.strftime("%d/%m/%Y"), tile) );

			path = int(tile[:3])
			row = int(tile[3:])
			bbox = { 'x1': x1, 'y1': y1, 'x2': x2,  'y2': y2 };

			mvcFile = self.getMvcFile(tile);

			if not os.path.exists(mvcFile):

				print("  calculate MVC");
				gapfill = self.gapfill;
				if self.gapfill == 'L1':
					gapfill = -1;

				mvcs = newmvc.getImages(path, row, bbox, self.cloudThreshold , gapfill);

				#NDVI_PALETTE = 'ec1413, e8dfa0, 0aa73c';
				#ee.mapclient.addToMap(mvcs['months'][2], { 'palette': NDVI_PALETTE }, 'cs2');
				#ee.mapclient.centerMap(-49.25,-16.66,5)

				tileFiles = [];
 				
				monthIndex = 1;
				for mvcMonth in mvcs['months']:
					tileFile = self.temppath(tile + '-' + str(monthIndex) );
					
					print("  download MVC {0}".format(tileFile));
					download.eeImage(mvcMonth, 30, 'EPSG:4326', bbox, tileFile);
					tileFiles.append(tileFile + '.NDVI.tif');
					
					monthIndex += 1;
				
				for devIndexes in [ 'cs1', 'cs2', 'stdDev' ]:
					tileFile = self.temppath(tile + '-' + devIndexes);
					
					print("  download MVC {0}".format(tileFile));
					download.eeImage(mvcs[devIndexes], 30, 'EPSG:4326', bbox, tileFile);
					tileFiles.append(tileFile + '.NDVI.tif');

				vrtFile = self.temppath(tile + '.vrt');
				tileFilesStr = ' '.join(tileFiles);
				gdalbuildvrt = 'gdalbuildvrt -separate {0} {1}'.format(vrtFile, tileFilesStr);
				gdalTranslate = "gdal_translate -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE {0} {1}".format(vrtFile, mvcFile);

				print("  merge bands");
				os.system(gdalbuildvrt);
				os.system(gdalTranslate);

				print("  remove temp files");
				tileFiles.append(vrtFile);
				for f in tileFiles:
					os.remove(f);
				

			else:
				print(" MVC exists... Next !!!")


	def classifyWithRandTrainning(self, feature):

		tile = feature.GetFieldAsString(self.tileAttribute);
		
		mvcFile = self.getMvcFile(tile)
		boundsGeometry = feature.geometry();
		nRandomPoints = self.nTreeRandomPoints;
		execNumber = int(self.trainningDataset[1:]);

		classificationResults = [ ];
		
		print( "{0} Tile {1}".format(time.strftime("%d/%m/%Y"), tile) );
		
		for i in range(execNumber):
			tmpFiles = [];
			rSuffix = "_R" + str(i) + '-' + str(execNumber);
			fileBaseName = tile + rSuffix;

			pctRandom = float(feature.GetFieldAsString(self.pctClassAttribute));

			print( " Execution {0}".format( str(i + 1) ) );

			filterTile="{0} = '{1}'".format(self.tileAttribute, tile);
			gridFile = self.basepath('INPUT', 'GRID', 'CLASSIFICATION_GRID.shp');

			
			validationDataset = "DATASET_{0}".format(self.validationDataset);
			validationFile = self.basepath('INPUT', 'VALIDATION', validationDataset, 'POLYGON_VALIDATION.shp');

			trainningFile = self.temppath(fileBaseName + ".shp");
			
			tmpFiles.append(self.temppath(fileBaseName + ".shp"));
			tmpFiles.append(self.temppath(fileBaseName + ".dbf"));
			tmpFiles.append(self.temppath(fileBaseName + ".shx"));
			tmpFiles.append(self.temppath(fileBaseName + ".prj"));
			
			try:
				os.remove(trainningFile);
			except:
				pass

			srs = osr.SpatialReference()
			srs.ImportFromEPSG(4326)

			trainningDs = self.geoDB['drivers']['shp'].CreateDataSource(trainningFile)
			trainningLayer = trainningDs.CreateLayer("point_out", srs, ogr.wkbPoint )
			trainningLayer.CreateField( ogr.FieldDefn(self.trainningAttribute, ogr.OFTString) )

			fixedTotalPoints = int(math.ceil(nRandomPoints * 0.25));
			pctTotalPoints = int(math.trunc(nRandomPoints * 0.75));

			nRandPointIn = int(math.trunc(pctTotalPoints * pctRandom)) + (fixedTotalPoints / 2)
			print( "  {0} {1} randomPoints".format( time.strftime("%H:%M:%S"), nRandPointIn ) );
			inTrainningPoints = randompoints.randomPointsIn(validationFile, nRandPointIn, boundsGeometry);

			nRandPointOut = int(math.ceil(pctTotalPoints * (1 - pctRandom))) + (fixedTotalPoints / 2)
			print( "  {0} {1} randomPointsOut".format( time.strftime("%H:%M:%S"), nRandPointOut ) );
			notInTrainningPoints = randompoints.randomPointsOut(validationFile, nRandPointOut, boundsGeometry);

			for point in notInTrainningPoints:
				feat = ogr.Feature(trainningLayer.GetLayerDefn())
				feat.SetGeometry(point['geometry']);
				feat.SetField(self.trainningAttribute, 1)
				trainningLayer.CreateFeature(feat)
			
			for point in inTrainningPoints:
				feat = ogr.Feature(trainningLayer.GetLayerDefn())
				feat.SetGeometry(point['geometry']);
				feat.SetField(self.trainningAttribute, 2)
				trainningLayer.CreateFeature(feat)
			
			trainningLayer.SyncToDisk();

			tempOutputFile = self.temppath(fileBaseName + "_noclip.tif");
			tmpFiles.append(tempOutputFile);

			classificationResult = self.temppath(fileBaseName + '.tif');
			classificationResults.append(classificationResult);
			
			print( "  {0} Classify".format( time.strftime("%H:%M:%S") ) );
			resultClassification = garsect2.run2(mvcFile, trainningFile, self.trainningAttribute, self.mvcNullValue, tempOutputFile, None, 1, self.nTreeRandomForest, [1]);
			
			command = 'gdalwarp -co COMPRESS=lzw -co INTERLEAVE=BAND -co TILED=YES -ot Int16 -q -dstnodata "{0}" -cwhere "{1}" -crop_to_cutline -overwrite -multi -cutline {2} {3} {4}'.format(self.mvcNullValue, filterTile, gridFile, tempOutputFile, classificationResult);
			os.system(command);

			print( "  {0} Remove temp files".format( time.strftime("%H:%M:%S") ) );
			for tmpFile in tmpFiles:
				os.remove(tmpFile);
		
		letters = [];
		params = '';
		for i,classificationResult in enumerate(classificationResults):
			letter = ascii_uppercase[i];
			params += " -{0} {1} ".format(letter, classificationResult);
			letters.append(letter);

		expr = "({0})/{1}".format( '+'.join(letters), len(letters) );
		outputFilename = "{0}_CLASSIFICATION.tif".format(tile);
		outputFile = self.basepath('OUTPUT', self.runtimeDataset, 'CLASSIFICATION', outputFilename);

		print( " {0} AVG classification calcultion".format( time.strftime("%H:%M:%S") ) );
		command = 'gdal_calc.py --co="COMPRESS=deflate" --co="INTERLEAVE=BAND" --co="TILED=YES" --NoDataValue=0 {0} --outfile={1} --calc="{2}"'.format(params, outputFile, expr)
		os.system(command);

		for classificationResult in classificationResults:
			print( " {0} Remove temp files".format( time.strftime("%H:%M:%S") ) );
			os.remove(classificationResult);

		return '';

	def classify(self, feature):
		tile = feature.GetFieldAsString(self.tileAttribute);

		print( "{0} Tile {1}".format(time.strftime("%d/%m/%Y"), tile) );

		filterTile="{0} = '{1}'".format(self.tileAttribute, tile);
		gridFile = self.basepath('INPUT', 'GRID', 'CLASSIFICATION_GRID.shp');

		mvcFile = self.getMvcFile(tile);

		trainningDataset = "DATASET_{0}".format(self.trainningDataset);
		trainningFilename = "{0}_TRAINNING.shp".format(tile);
		trainningFile = self.basepath('INPUT', 'TRAINNING', trainningDataset, trainningFilename);
		
		tempOutputFilename = "{0}_G{1}_{2}_MVC.tif".format(tile, self.gapfill.zfill(2), self.trainningDataset);
		tempOutputFile = self.temppath(tempOutputFilename);

		outputFilename = "{0}_CLASSIFICATION.tif".format(tile);
		outputFile = self.basepath('OUTPUT', self.runtimeDataset, 'CLASSIFICATION', outputFilename);

		outputStatsFilename = "{0}_STATS.csv".format(tile);
		outputStatsFile = self.basepath('OUTPUT', self.runtimeDataset, 'VALIDATION', outputStatsFilename);

		if not self.noClassify:
			print( " {0} Classify".format( time.strftime("%H:%M:%S") ) );
			resultClassification = garsect2.run2(mvcFile, trainningFile, self.trainningAttribute, self.mvcNullValue, tempOutputFile, outputStatsFile, 1, self.nTreeRandomForest, [1]);
			
			command = 'gdalwarp -co COMPRESS=lzw -co INTERLEAVE=BAND -co TILED=YES -ot Byte -q -dstnodata "{0}" -cwhere "{1}" -crop_to_cutline -overwrite -multi -cutline {2} {3} {4}'.format(self.mvcNullValue, filterTile, gridFile, tempOutputFile, outputFile);
			os.system(command);

			os.remove(tempOutputFile);
		
		return outputFile;

	def validate(self, outputFile, feature):

		boundsGeometry = feature.geometry();
		tile = feature.GetFieldAsString(self.tileAttribute);

		validationDataset = "DATASET_{0}".format(self.validationDataset);
		validationFile = self.basepath('INPUT', 'VALIDATION', validationDataset, 'POLYGON_VALIDATION.shp');

		validationTileDir = self.basepath('OUTPUT', self.runtimeDataset, 'VALIDATION', tile);
		self.createDirIfNotExists(validationTileDir);

		thresholds = [10,20,30,40,50,60,70,80,90];
		outputFilepathBase = self.joinDirs(validationTileDir, tile);

		validationShpPoints = None;
		if self.prefetchedShpPoints:
			validationShpPointsFilename = "{0}_POINTS_VALIDATION.shp".format(tile);
			validationShpPoints = self.basepath('INPUT', 'VALIDATION', validationDataset, validationShpPointsFilename);
		
		print(validationShpPoints);
		print( " {0} validate".format( time.strftime("%H:%M:%S") ) );
		randompoints.confusionMatrix(outputFile, validationFile, self.nValidationPoints, thresholds, boundsGeometry, outputFilepathBase, True, validationShpPoints, self.onlyOmission)

	def run(self):

		if not self.noDownload:
			self.download();

		gridClassification = self.getGridClassification();
		tilesCount = gridClassification.GetFeatureCount();

		for i in xrange(tilesCount):
			feature = gridClassification.GetNextFeature();

			outputFile = None
			if self.trainningDataset[:1] == 'R':
				outputFile = self.classifyWithRandTrainning(feature)
			else:
				outputFile = self.classify(feature)

			if not self.noValidate:
				self.validate(outputFile, feature)

def main():    
    
    prog = os.path.split(__file__)[1]
    parser = argparse.ArgumentParser(prog=prog, 
        description='LAPIG classification', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-i', '--tiles', default=None, 
                        help='Grid tiles filter')
    parser.add_argument('-c', '--tile-attribute', dest='tileAttribute', default='TILE', 
                        help='The attribute used to identify one tile in shapefiles grid')
    parser.add_argument('-a', '--trainning-attribute', dest='trainningAttribute', default='CLASS_ID', 
                        help='The attribute with class id in trainning dataset')

    parser.add_argument('-r', '--mvc-dataset', dest='mvcDataset', default='01',
                        help='MVC dataset')
    parser.add_argument('-t', '--trainning-dataset', dest='trainningDataset', default='01',
                        help='Trainning dataset')
    parser.add_argument('-v', '--validation-dataset', dest='validationDataset', default='01',
                        help='Validation dataset')

    parser.add_argument('-gf', '--mvc-gapfill-value', dest='gapfill', default='L1',
                        help='Gapfill value used in MVC approach')
    parser.add_argument('-ct', '--mvc-cloud-threshold', dest='cloudThreshold', default=40, type=int,
                        help='Cloud Threshold used in MVC approach')
    parser.add_argument('-tn', '--tree-number-randomforest', dest='nTreeRandomForest', default=10, type=int,
                        help='Tree number used in classification approach')
    parser.add_argument('-ntr', '--number-trainning-random-points', dest='nTreeRandomPoints', default=1000, type=int,
                        help='Random points number used in random classification approach')
    parser.add_argument('--prefetched-shp-random-points', dest='prefetchedShpPoints', action='store_true',
                        help='Number of random validation point for error matrix')
    parser.add_argument('--only-omission', dest='onlyOmission', action='store_true', 
												help='Calculate only omission error')
    parser.add_argument('-vp', '--validation-point-number', dest='nValidationPoints', default=3000, type=int,
                        help='Number of random validation point for error matrix')

    parser.add_argument('--no-download', dest='noDownload', action='store_true',
                        help='Download MVCs from Earth Engine')
    parser.add_argument('--no-classify', dest='noClassify', action='store_true',
                        help='Execute classification approach')
    parser.add_argument('--no-validate', dest='noValidate', action='store_true',
                        help='Execute validation approach')

    parser.add_argument('-p', '--procs', default=MAXPROCS,
                        help='Execute validation approach')

    parser.add_argument('--version', action='version', version=VERSION)

    properties = parser.parse_args()

    classification = Classification(properties);
    classification.run();

    #run(args.tiles, args.tileAttribute, args.mvcDataset, args.gapfill, args.cloudThreshold, args.trainningDataset, args.validationDataset, args.noDownload, args.noClassify, args.noValidate, args.procs);

if __name__ == "__main__":
    main()