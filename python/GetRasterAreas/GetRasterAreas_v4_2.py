import os
import sys
import gdal, ogr, osr, numpy
import datetime

def zonal_stats(feat, input_zone_polygon, input_value_raster, nb):

    # Open data
    raster = gdal.Open(input_value_raster)
    shp = ogr.Open(input_zone_polygon)
    lyr = shp.GetLayer()
    
    #Select feature layer
    feature = lyr.GetFeature(nb)
    name = feature.GetField(str(sys.argv[3]))
    #Get feature geometry
    geometry = feature.GetGeometryRef()

    #Create an virtual Layer
    driver = ogr.GetDriverByName("Memory")

    data_source = driver.CreateDataSource("tempDS")
    srs = lyr.GetSpatialRef()

    layer = data_source.CreateLayer("tempLayer", srs, geometry.GetGeometryType())
        
    Nfeature = ogr.Feature(layer.GetLayerDefn());
    Nfeature.SetGeometry(geometry);
    layer.CreateFeature(Nfeature);

    # Get raster georeference info
    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    print(transform)

    # Get extent of feat
    geom = feat.GetGeometryRef()
    if (geom.GetGeometryName() == 'MULTIPOLYGON'):
        count = 0
        pointsX = []; pointsY = []
        for polygon in geom:
            geomInner = geom.GetGeometryRef(count)
            ring = geomInner.GetGeometryRef(0)
            numpoints = ring.GetPointCount()
            for p in range(numpoints):
                    lon, lat, z = ring.GetPoint(p)
                    pointsX.append(lon)
                    pointsY.append(lat)
            count += 1
    elif (geom.GetGeometryName() == 'POLYGON'):
        ring = geom.GetGeometryRef(0)
        numpoints = ring.GetPointCount()
        pointsX = []; pointsY = []
        for p in range(numpoints):
                lon, lat, z = ring.GetPoint(p)
                pointsX.append(lon)
                pointsY.append(lat)

    else:
        sys.exit("ERROR: Geometry needs to be either Polygon or Multipolygon")

    xmin = min(pointsX)
    xmax = max(pointsX)
    ymin = min(pointsY)
    ymax = max(pointsY)

    # Specify offset and rows and columns to read
    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth)+1
    ycount = int((ymax - ymin)/pixelWidth)+1

    # Create memory target raster
    #target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)
    
    file = '/data/DADOS02/RASTER/EARTHENGINE/drive_vinicius/TESTE_LIBTIFF/TEMP/'+str(name)+'_temp.tif'

    if os.path.exists(file):
        target_ds = gdal.Open(file)
    else:
        target_ds = gdal.GetDriverByName('GTiff').Create('/data/DADOS02/RASTER/EARTHENGINE/drive_vinicius/TESTE_LIBTIFF/TEMP/'+str(name)+'_temp.tif', xcount, ycount, 1, gdal.GDT_Byte,[ 'COMPRESS=LZW' ])
        target_ds.SetGeoTransform((xmin, pixelWidth, 0,ymax, 0, pixelHeight))
        # Create for target raster the same projection as for the value raster
        raster_srs = osr.SpatialReference()
        raster_srs.ImportFromWkt(raster.GetProjectionRef())
        target_ds.SetProjection(raster_srs.ExportToWkt())
        gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[1], options = []) #, options = ["ALL_TOUCHED=TRUE", "BURN_VALUE_FROM"]);

    # Rasterize zone polygon to raster
    
    # Read raster as arrays
    print('Feature mask generated! Proceding to Z0N4L 5T4T1ST1C5')

    banddataraster = raster.GetRasterBand(1)
    bandmask = target_ds.GetRasterBand(1)

    totalSum = 0
    
    rowSize = 256
    lineSize = int(xcount*0.35)
    
    beginAt = datetime.datetime.now()

    for x in range(xoff,xoff+xcount,lineSize):

        for y in range(yoff,yoff+ycount,rowSize):

            if (xcount) > (x-xoff+lineSize):

                if (ycount) > (y-yoff+rowSize):
                    dataraster = banddataraster.ReadAsArray(x, y, lineSize,rowSize).astype(numpy.byte)
                    datamask = bandmask.ReadAsArray(x-xoff, y-yoff,lineSize, rowSize).astype(numpy.byte)
                else:
                    dataraster = banddataraster.ReadAsArray(x, y, lineSize,ycount - (y-yoff)).astype(numpy.byte)
                    datamask = bandmask.ReadAsArray(x-xoff, y-yoff,lineSize, ycount - (y-yoff)).astype(numpy.byte)

            else:
                if (ycount) > (y-yoff+rowSize):
                    dataraster = banddataraster.ReadAsArray(x, y, xcount - (x-xoff), rowSize).astype(numpy.byte)
                    datamask = bandmask.ReadAsArray(x-xoff, y-yoff, xcount - (x-xoff), rowSize).astype(numpy.byte)
                else:
                    dataraster = banddataraster.ReadAsArray(x, y, xcount - (x-xoff),ycount - (y-yoff)).astype(numpy.byte)
                    datamask = bandmask.ReadAsArray(x-xoff, y-yoff,xcount - (x-xoff), ycount - (y-yoff)).astype(numpy.byte)

            zoneraster = dataraster[datamask==1]
            totalSum = totalSum + numpy.sum(zoneraster);
            dataraster = datamask = zoneraster = None
        
    print('Total time spend: ' + str(datetime.datetime.now()-beginAt))

    banddataraster = bandmask = raster = shp = target_ds = None

    #return int(totalSum)
    return float(int(totalSum)*((float(pixelWidth)*float(pixelWidth))/10000.0))

def loop_zonal_stats(input_zone_polygon, input_value_raster,field_name):

    shp = ogr.Open(input_zone_polygon)
    lyr = shp.GetLayer()
    featList = range(lyr.GetFeatureCount())
    statDict = {}

    for FID in featList:
        #FID = 3
        feat = lyr.GetFeature(FID)
        meanValue = zonal_stats(feat, input_zone_polygon, input_value_raster, FID)
        feature = lyr.GetFeature(FID)
        name = feature.GetField(str(field_name))
        print(input_value_raster + ' ' + str(name) + ' ' + str(meanValue))
        statDict[name] = meanValue
    return statDict

loop_zonal_stats(sys.argv[1], sys.argv[2],sys.argv[3])
