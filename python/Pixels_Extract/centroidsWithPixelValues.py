import os
import gdal, ogr, osr, numpy;

def pixelsPosition2Coordinates(raster, xPosition, yPosition, centerCorrection = True):
	xOrigin, pixelWidth, dummy, yOrigin, dummy2, pixelHeight  = raster.GetGeoTransform();

	lon = xPosition * pixelWidth + xOrigin;
	lat = yPosition * pixelHeight + yOrigin;

	if centerCorrection:
		lon = lon + pixelWidth/2
		lat = lat + pixelHeight/2

	return lon, lat;

def lonLat2pixelsPosition(raster, lon, lat, centerCorrection = True):
	xOrigin, pixelWidth, dummy, yOrigin, dummy2, pixelHeight  = raster.GetGeoTransform();

	xDistance = numpy.diff([lon, xOrigin])[0];
	yDistance = numpy.diff([lat, yOrigin])[0];

	xPosition = int(xDistance / pixelWidth);
	yPosition = int(yDistance / pixelHeight);

	return abs(xPosition), abs(yPosition);

def centroidsWithPixelValues(raster_path, shapefile_path):
	
	shapefileDriver = ogr.GetDriverByName("ESRI Shapefile")
	geotiffDriver = gdal.GetDriverByName('GTiff');

	dataSource = shapefileDriver.Open(shapefile_path, 0)
	vectorInput = dataSource.GetLayer()
	vectorInputSRS = vectorInput.GetSpatialRef()

	rasterInput = gdal.Open(raster_path);

	xmin, xmax, ymin, ymax = vectorInput.GetExtent();
	xOrigin, pixelWidth, dummy, yOrigin, dummy2, pixelHeight  = rasterInput.GetGeoTransform();

	xcount = int((xmax - xmin)/pixelWidth)+1
	ycount = int((ymax - ymin)/pixelWidth)+1

	xPosition, yPosition = lonLat2pixelsPosition(rasterInput,xmin,ymax);
	xmin, ymax = pixelsPosition2Coordinates(rasterInput,xPosition,yPosition, False);

	rasterOutput = geotiffDriver.Create('opa.tif', xcount, ycount, 1, gdal.GDT_Byte, options = [])
	rasterOutput.SetGeoTransform((xmin, pixelWidth, 0, ymax, 0, pixelHeight))

	rasterSrs = osr.SpatialReference();
	rasterSrs.ImportFromWkt(rasterInput.GetProjectionRef());
	rasterOutput.SetProjection(rasterSrs.ExportToWkt());

	gdal.RasterizeLayer(rasterOutput, [1], vectorInput, burn_values=[1], options = [ "ALL_TOUCHED=TRUE", "BURN_VALUE_FROM"]);
	rasterOutputBand = rasterOutput.GetRasterBand(1);
	rasterOutputBand.SetNoDataValue(0);
	rasterOutputValues = rasterOutputBand.ReadAsArray(0, 0, xcount, ycount);
	rasterOutputValues = numpy.where(rasterOutputValues == 1)

	if os.path.exists('points.shp'):
		shapefileDriver.DeleteDataSource('points.shp')
			
	outDataSource = shapefileDriver.CreateDataSource('points.shp')
	outLayer = outDataSource.CreateLayer('points.shp', geom_type=ogr.wkbPoint, srs=vectorInputSRS)

	xCounter = 0
	bands = rasterInput.RasterCount;
	
	for i in range(1, bands+1):
		bandField = ogr.FieldDefn('band'+str(i), ogr.OFTReal);
		outLayer.CreateField(bandField)

	for yIndex in rasterOutputValues[0]:
			xIndex = rasterOutputValues[1][xCounter]
			
			lon, lat = pixelsPosition2Coordinates(rasterOutput,xIndex,yIndex);
			print(lon, lat);

			point = ogr.Geometry(ogr.wkbPoint)
			point.AddPoint(lon, lat)
			featureDefn = outLayer.GetLayerDefn()
			outFeature = ogr.Feature(featureDefn)
			outFeature.SetGeometry(point)
			
			for i in range(1, bands+1):
				rasterInputBand = rasterInput.GetRasterBand(i);
				xPostion, yPosition = lonLat2pixelsPosition(rasterInput, lon, lat);
				rasterValue = rasterInputBand.ReadAsArray(xPostion, yPosition, 1, 1);
				
				fieldName = 'band'+str(i);
				fieldValue = rasterValue[0][0];
				
				outFeature.SetField(fieldName, float(rasterValue))
			
			outLayer.CreateFeature(outFeature)
			outFeature = None
				
			xCounter += 1

raster = 'ndvi_2014_2017.vrt'
shapefile = "talhoes.shp"

centroidsWithPixelValues(raster, shapefile);
