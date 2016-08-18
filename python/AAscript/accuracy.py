#!/usr/bin/python
# -*- coding: utf-8 -*-

import gdal, ogr, csv, os;
import sys
import argparse
from sys import argv;

def getclasssIndex(classs, layer):
	feature0 = layer.GetFeature(0);
	for i in range(0, feature0.GetFieldCount()):
		if feature0.GetFieldDefnRef(i).GetNameRef() == classs:
			return i;
	
	return -1;

def AccuracyAssessment(GDALDataSet, layer, classs, outdir, precision):

	
	if (os.path.isfile(outdir+'accuracy'+'.shp')==True) & (os.path.isfile(outdir+'accuracy'+'.shx')==True) & (os.path.isfile(outdir+'accuracy'+'.dbf')==True):
		os.remove(outdir+'accuracy'+'.shp');
		os.remove(outdir+'accuracy'+'.shx');
		os.remove(outdir+'accuracy'+'.dbf');


	driver = ogr.GetDriverByName('ESRI Shapefile')
	output_file = driver.CreateDataSource(outdir);

	output_layer = output_file.CreateLayer('accuracy', None, ogr.wkbPoint );
	classsReference = ogr.FieldDefn(layer.GetFeature(0).GetFieldDefnRef(getclasssIndex(classs, layer)).GetNameRef(), ogr.OFTString)
	classsclasssification = ogr.FieldDefn('classsClas', ogr.OFTString);

	output_layer.CreateField(classsReference);
	output_layer.CreateField(classsclasssification);

	
	FieldNames = {}
	FieldNamesLista = [];
	line = 0;
	colum = 2;
	pastagem = 0;
	notPastagem = 1;


	gt = GDALDataSet.GetGeoTransform()
	rasterBand = GDALDataSet.GetRasterBand(1);
	
	for feature in layer:
		fieldValue = feature.GetFieldAsString(getclasssIndex(classs, layer));
		if(fieldValue not in FieldNames):
				FieldNamesLista.append(fieldValue);
				FieldNames[fieldValue] = line;
				line += 1

	totalAccuracy = [[0 for x in range(line)] for y in range(colum)]
	layer.ResetReading();

	for feature in layer:
		geom = feature.GetGeometryRef();
		mx, my = geom.GetX(), geom.GetY();

		try:
			px = int((mx - gt[0]) / gt[1]) #x pixel
			py = int((my - gt[3]) / gt[5]) #y pixel
			intval = rasterBand.ReadAsArray(px,py,1,1)
			pixelValue = intval[0][0];

			fieldValue = feature.GetFieldAsString(getclasssIndex(classs, layer));
			accurancyclasssIndex = FieldNames[fieldValue];
			classseReferenciaValue = '';

			if pixelValue >= int(precision):
				totalAccuracy[pastagem][accurancyclasssIndex] += 1;
				classseReferenciaValue = 'Pastagem';
			else:
				totalAccuracy[notPastagem][accurancyclasssIndex] += 1;
				classseReferenciaValue = 'Nao Pastagem';

			feat = ogr.Feature(output_layer.GetLayerDefn())
			feat.SetGeometry(geom);
			feat.SetField(layer.GetFeature(0).GetFieldDefnRef(getclasssIndex(classs, layer)).GetNameRef(), fieldValue);
			feat.SetField('classsClas', classseReferenciaValue);

			output_layer.CreateFeature(feat)

		except OverflowError:
			pass

	count = 0;   
	for line in totalAccuracy:
		if count == 0:
			line.insert(0, 'Pastagem');
			count += 1;
		else:
			line.insert(0, 'NotPastagem')

	keys = []

	for key in FieldNamesLista:
		keys.append(key);

	keys.insert(0,'#####')
	totalAccuracy.insert(0,keys)

	return totalAccuracy


def WriteFile(AAs, outdir):
	with open(outdir+'accuracy'+'.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',');
		for line in AAs:
			spamwriter.writerow(line);
		return True;



def main(classsification, reference, classs, outdir, precision=5000):

	GDALDataSet = gdal.Open(classsification);
	shape = ogr.Open(reference);
	layer = shape.GetLayer();
	AAs =  AccuracyAssessment(GDALDataSet, layer, classs, outdir, precision);
	WriteFile(AAs, outdir);




def parseArguments():
		    
    parser = argparse.ArgumentParser()
    parser.add_argument("classification", help="Raster file", type=str);
    parser.add_argument("reference", help="Shape file", type=str);
    parser.add_argument("classs", help="column value", type=str);
    parser.add_argument("outdir", help="Output directory", type=str);
    parser.add_argument("precision", help="precision to be analyzed", default=5000, nargs='?');

    args = parser.parse_args();

    return args


if __name__ == "__main__":

	args = parseArguments()

	main(args.classification, args.reference, args.classs, args.outdir, args.precision);
