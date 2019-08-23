import sys
import gdal, ogr, osr, numpy
# import Image

def zonal_stats(feat, input_zone_polygon, input_value_raster, nb):

    # Open data
    raster = gdal.Open(input_value_raster)
    shp = ogr.Open(input_zone_polygon)
    lyr = shp.GetLayer()
    
    feature = lyr.GetFeature(nb)
    
    geometry = feature.GetGeometryRef()

    driver = ogr.GetDriverByName("Memory")

    data_source = driver.CreateDataSource("tempDS")
    srs = lyr.GetSpatialRef()

    layer = data_source.CreateLayer("tempLayer", srs, geometry.GetGeometryType())
        
    Nfeature = ogr.Feature(layer.GetLayerDefn());
    Nfeature.SetGeometry(geometry);
    layer.CreateFeature(Nfeature);

    transform = raster.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

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

    xoff = int((xmin - xOrigin)/pixelWidth)
    yoff = int((yOrigin - ymax)/pixelWidth)
    xcount = int((xmax - xmin)/pixelWidth)
    ycount = int((ymax - ymin)/pixelWidth)

    if xcount <= 0 or ycount <= 0:
        return -1.0, 0

    target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, gdal.GDT_Byte)

    target_ds.SetGeoTransform((
        xmin, pixelWidth, 0,
        ymax, 0, pixelHeight,
    ))

    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(raster.GetProjectionRef())
    target_ds.SetProjection(raster_srs.ExportToWkt())

    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[1], options = []) #, options = ["ALL_TOUCHED=TRUE", "BURN_VALUE_FROM"]);

    banddataraster = raster.GetRasterBand(1)
    dataraster = banddataraster.ReadAsArray(xoff, yoff, xcount, ycount)

    bandmask = target_ds.GetRasterBand(1)
    datamask = bandmask.ReadAsArray(0, 0, xcount, ycount)

    validmask = numpy.logical_and(numpy.logical_not(numpy.isnan(dataraster)), datamask==1)
    validdata = dataraster[validmask]
    
    if len(validdata) > 0:
        area_past = (len(validdata) * 29.1336 * 29.1336) / 10000
        area_1 = len(validdata[validdata>=0.6])
        area_2 = len(validdata[numpy.logical_and(validdata>=0.5,validdata<0.6)])
        area_3 = len(validdata[numpy.logical_and(validdata>=0.4,validdata<0.5)])
        area_4 = len(validdata[validdata<0.4])
        cvp_tot = (area_1 * 1) +  (area_2 * 2) + (area_3 * 3) + (area_4 * 4)
        npixel = len(validdata)
        IDP = cvp_tot/npixel
        return area_past, IDP
    else:
        return 0, 0

def loop_zonal_stats(input_zone_polygon, input_value_raster, field_name, offset, count):

    shp = ogr.Open(input_zone_polygon)
    lyr = shp.GetLayer()
    totalFeatures = lyr.GetFeatureCount()
    statDict = {}

    length = offset + count
    if length > totalFeatures:
        length = totalFeatures

    for FID in range(offset,length):
        feat = lyr.GetFeature(FID)
        area_past, IDP = zonal_stats(feat, input_zone_polygon, input_value_raster, FID)
        feature = lyr.GetFeature(FID)
        name = feature.GetField(str(field_name))
        print(str(FID) + ';' + str(name) + ';' + str(area_past) + ';' + str(IDP))

    return statDict

SHP='/data/DADOS_GRID/DATASAN/idp_car/car_cerrado/car_cerrado.shp'
#RASTER='/data/DADOS_GRID/DATASAN/idp_car/ndviq/ndviq_cerrado_2018.tif'
RASTER='/data/DADOS_GRID/DATASAN/idp_car/ndviq/ndviq_cerrado_2010_mask_10.tif'
FIELD='gid'

loop_zonal_stats(SHP, RASTER, FIELD, int(sys.argv[1]), int(sys.argv[2]))
