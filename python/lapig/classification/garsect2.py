#!/usr/bin/env /opt/anaconda/bin/python
################################################################################
#    GARSECT: RANDOM FOREST IMAGE CLASSIFIER
#
#    AUTHORS: Stephen Hagen, Matthew Hansen, Bobby Braswell
#    EMAIL: rbraswell@appliedgeosolutions.com
#
#    Copyright (C) 2014 Applied Geosolutions
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>
################################################################################

import os
import sys
import commands
import argparse
import time
import csv

import numpy as np
from osgeo import gdal, ogr
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

np.seterr(all='raise')
gdal.UseExceptions()

__version__ = "0.2"
__license__ = "GPLv2"
__email__ = "rbraswell@appliedgeosolutions.com"

MAXPROCS = 5

def read_raster(infile, scale=False):
    f = gdal.Open(infile)
    meta = f.GetMetadata()
    proj = f.GetProjection()
    geo = f.GetGeoTransform()
    data = f.ReadAsArray()
    if scale is True:
        nbands = f.RasterCount
        info = []
        data = data.astype('float64')
        for i in range(nbands):
            band = f.GetRasterBand(i+1)
            missing = band.GetNoDataValue()
            offset = band.GetOffset()
            scale = band.GetScale()
            info.append({'missing':missing, 'offset':offset, 'scale':scale})
        return data, proj, geo, meta, info            
    else:
        return data, proj, geo, meta

def create_datatype(np_dtype):
    np_dtype = str(np_dtype)
    typestr = 'gdal.GDT_' + np_dtype.title().replace('Ui', 'UI')
    g_dtype = eval(typestr)
    if g_dtype == 'gdal.GDT_UInt8':
        g_dtype = 'gdal.GDT_Byte'
    return g_dtype

def write_raster(fname, data, proj, geo, meta, outputbands=[], creationOptions=[]):
    driver = gdal.GetDriverByName('GTiff')
    try:
        (nband, ny, nx) = data.shape
    except:
        nband = 1
        (ny, nx) = data.shape
        data = data.reshape(1, ny, nx)

    if not outputbands:
        outputbands = range(nband);
        outputNband = nband;
    else:
        outputNband = len(outputbands)

    dtype = create_datatype(data.dtype)
    tfh = driver.Create(fname, nx, ny, outputNband, dtype, creationOptions)
    tfh.SetProjection(proj)
    tfh.SetGeoTransform(geo)
    tfh.SetMetadata(meta)
    
    outputBandIndex = 0;
    for i in range(nband):
        for j in outputbands:
            if i == j:
                band = tfh.GetRasterBand(outputBandIndex+1)
                band.WriteArray(data[i])
                outputBandIndex += 1;

    tfh = None

def get_raster_info(infile):
    fp = gdal.Open(infile)
    info = dict()
    info['fp'] = fp
    info['nband'] = fp.RasterCount
    info['xydim'] = fp.RasterXSize, fp.RasterYSize
    info['meta'] = fp.GetMetadata()
    info['proj'] = fp.GetProjection()
    info['geo'] = fp.GetGeoTransform()
    info['format'] = fp.GetDriver().ShortName
    bp = fp.GetRasterBand(1)
    info['dtype'] = gdal.GetDataTypeName(bp.DataType)    
    return info

def library_table(rasterfile, shapefile, attribute="class", fill_value=None, usebands=None):
    if usebands is not None:
        usebands = [b - 1 for b in usebands]  
    result, tmprasterfile = gdal_rasterize(rasterfile, shapefile, attribute)
    assert result[0] == 0
    imagefile = gdal.Open(rasterfile)
    imagedata = imagefile.ReadAsArray()
    dims = imagedata.shape
    if len(dims) == 2:
        imagedata = imagedata.reshape(1, dims[0], dims[1])
    classfile = gdal.Open(tmprasterfile)
    classband = classfile.GetRasterBand(1)
    classdata = classband.ReadAsArray()
    os.remove(tmprasterfile)
    xmx = classdata.max()
    result = {'uid':[], 'class':[], 'value':[], 'location':[]}
    count = 0
    for i in range(1, xmx+1):
        w = np.where(classdata == i)
        nw = len(w[0])
        for j in range(nw):
            if usebands is None:
                values = imagedata[:, w[0][j],w[1][j]]
            else:
                values = imagedata[usebands, w[0][j],w[1][j]]            
            if fill_value in values:
                continue
            count += 1
            result['uid'].append(count)
            result['class'].append(i)
            result['value'].append(values)
            result['location'].append((w[0][j], w[1][j]))
    return result

def gdal_rasterize(rasterfile, shapefile, attribute, outfile=None, clobber=False):
    if outfile is not None:
        if os.path.exists(outfile) and clobber is True:
            print "removing", outfile
            os.remove(outfile)
        elif os.path.exists(outfile) and clobber is False:
            raise Exception('output file exists and clobber is False')
    proj_vector = get_vector_proj(shapefile)
    info_raster = get_raster_info(rasterfile)
    proj_raster = info_raster['proj']
    if proj_vector != proj_raster:
        projpath = os.path.splitext(rasterfile)[0] + '.proj'
        fp = open(projpath, 'w')
        fp.write(proj_raster+'\n')
        fp.close()
        newvectorpath = os.path.splitext(shapefile)[0] + "_reproj.shp"
        reproject_vector(shapefile, projpath, newvectorpath) 
        shapefile = newvectorpath
        os.remove(projpath)
    layer = os.path.splitext(os.path.split(shapefile)[1])[0]
    if outfile is None:
        outfile = tempfilename()
    blank_raster_like(rasterfile, outfile)
    cmd = "gdal_rasterize -l %s -a %s %s %s" % (layer, attribute, shapefile, outfile)
    result = commands.getstatusoutput(cmd)
    rmstring = os.path.splitext(newvectorpath)[0]
    commands.getstatusoutput('rm ' + rmstring + '.*')
    return result, outfile

def blank_raster_like(inpath, outpath, value=0, ndtype='int16'):
    info = get_raster_info(inpath)
    driver = gdal.GetDriverByName("GTiff")
    nx = info['xydim'][0]
    ny = info['xydim'][1]
    gdtype = eval('gdal.GDT_'+ndtype.title())
    tfh = driver.Create(outpath, nx, ny, 1, gdtype, [])
    tfh.SetProjection(info['proj'])
    tfh.SetGeoTransform(info['geo'])
    meta = {}
    tfh.SetMetadata(meta)
    tband = tfh.GetRasterBand(1)
    data = value + np.zeros((ny, nx), dtype = ndtype)
    tband.WriteArray(data)
    tfh = None

def tempfilename():
    import tempfile
    import uuid
    return os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

def get_vector_proj(infile, format = 'Wkt'):
    assert format in ('Wkt', 'XML', 'PCI', 'USGS', 'Proj4', 'PrettyWkt', 'MICoordSys')
    ds = ogr.Open(infile)
    assert ds is not None
    layer = ds.GetLayer(0)
    spatial_reference = layer.GetSpatialRef()
    export_function = eval('spatial_reference.ExportTo'+format)
    proj = export_function()
    return proj

def reproject_vector(infile, proj, outfile):
    if os.path.exists(outfile):
        os.remove(outfile)
    cmd = "ogr2ogr -t_srs %s %s %s" % (proj, outfile, infile)
    result = commands.getstatusoutput(cmd)
    assert not result[0], result[1]

def present_stats(ytrue, ypred):
    kappa, producers, consumers, overall, maxmiss, cmi, npts = calculate_stats(ytrue, ypred)
    ave_producers = producers.mean()
    ave_consumers = consumers.mean()
    print "\nConfusion matrix"
    print cmi
    print "\nNumber of training points"
    print npts
    print "\nProducer's accuracy"
    print producers
    print "\nConsumers accuracy"
    print consumers
    print "\nMean producer's accuracy"
    print ave_producers
    print "\nMean consumer's accuracy"
    print ave_consumers
    print "\nOverall accuracy"
    print overall
    print "\nMax misclassified"
    print maxmiss
    print "\nKappa coefficient"
    print kappa
    print
    return kappa


def calculate_stats(ytrue, ypred):
    cmi = confusion_matrix(ytrue, ypred)
    npts = cmi.sum(axis=1)
    cm = cmi.copy().astype('float32')/cmi.sum()
    overall = np.sum(np.diag(cm))
    producers = np.diag(cm) / np.sum(cm, axis=1)
    consumers = np.diag(cm) / np.sum(cm, axis=0)
    ave_producers = producers.mean()
    ave_consumers = producers.mean()
    err = np.sum(cm.sum(axis=0) * cm.sum(axis=1))
    kappa = (overall - err)/(1. - err)    
    nrm = cmi.astype('float32')/np.diag(cmi)
    maxmiss = np.triu(nrm, 1).max()
    return kappa, producers, consumers, overall, maxmiss, cmi, npts


TRAINFRAC = 0.95
MINTRAIN = 100
MINVALIDATE = 20

def optimize_model(X, y, nproc):
    nsamp = y.size
    print "nsamp", nsamp

    maxtrees = 50
    niter = 20
    ntrain = int(TRAINFRAC*nsamp)
    if ntrain < MINTRAIN or (nsamp - ntrain) < MINVALIDATE:
        raise Exception, "Not enough training data to optimize! %f %f" % (ntrain, nsamp-ntrain)
    idx = np.arange(nsamp)
    accuracy_prev = -999.
    accuracy_max = -999
    for itree in range(maxtrees):        
        np.random.seed(111)
        accuracies = []
        for i in range(niter):
            np.random.shuffle(idx)                    
            mod = RandomForestClassifier(n_estimators=itree+5, max_depth=None, min_samples_split=1,
                                         random_state=0, n_jobs=nproc)
            mod.fit(X[idx[:ntrain]], y[idx[:ntrain]])            
            ypred = mod.predict(X[idx[ntrain:]])
            try:
                accuracy = calculate_stats(y[idx[ntrain:]], ypred)[0]
                accuracies.append(accuracy)
            except Exception:
                continue
        try:        
            accuracy = np.mean(accuracies)
        except: 
            raise Exception, "Your classes probably have very unbalanced membership - fix training data"
            #Look into incorporating Steve's old script so that unbalanced classes don't matter
        improvement = accuracy - accuracy_prev
        #print itree, accuracy, improvement
        accuracy_prev = accuracy
        if accuracy > accuracy_max:
            accuracy_max = accuracy        
        if improvement < 0.:
            break
    return mod


def perform_crossval(X, y, ntree, nproc):
    nsamp = y.size
    niter = 20
    ntrain = int(0.5*nsamp)
    idx = np.arange(nsamp)
    kappas = []
    accuracies = []
    for i in range(niter):
        np.random.shuffle(idx)                    
        mod = RandomForestClassifier(n_estimators=ntree, max_depth=None, min_samples_split=1,
                                     random_state=0, n_jobs=nproc)
        mod.fit(X[idx[:ntrain]], y[idx[:ntrain]])            
        ypred = mod.predict(X[idx[ntrain:]])
        try:
            stats = calculate_stats(y[idx[ntrain:]], ypred)
            kappas.append(stats[0])
            accuracies.append(stats[3])
        except:
            pass
    return np.mean(accuracies), np.mean(kappas);

def run2(rasterfile, shapefile, attribute, fillvalue, outputfile, outputfileStats, nproc, ntree, outputbands=[], usebands=None):

    print( "  {0} library_table".format( time.strftime("%H:%M:%S") ) );
    result = library_table(rasterfile, shapefile, attribute, fillvalue, usebands)

    X = np.array(result['value'])
    y = np.array(result['class'])

    if np.any(np.isnan(X)):
        raise Exception, "There are NAN values in %s" % rasterfile
    
    print( "  {0} RandomForestClassifier".format( time.strftime("%H:%M:%S") ) );
    mod = RandomForestClassifier(n_estimators=ntree, max_depth=None, min_samples_split=1,random_state=0, n_jobs=nproc)
    mod.fit(X, y)

    data, proj, geo, meta = read_raster(rasterfile)
    dims = data.shape

    if len(dims) != 3:
        assert len(dims) == 2, "unexpected image dimensions: %d" % len(dims)            
        data = data.reshape(1, dims[0], dims[1])
        dims = list(dims)
        dims = tuple([1, dims[0], dims[1]])

    data = data.reshape(dims[0], dims[1]*dims[2]).T
    if np.any(np.isnan(data)):
        raise Exception, "There are NAN values in %s" % rasterfile
        #data[np.isnan(data)] = fillvalue

    if fillvalue is not None:
        wvalid = np.all(data != fillvalue, axis=1)
    else:
        wvalid = np.arange(dims[1]*dims[2])
    
    ypred = (100*mod.predict_proba(data[wvalid,:])).astype('uint16').T
    nbands = len(set(result['class']))

    data = np.zeros((nbands, dims[1]*dims[2]), dtype='int16')
    data[:,wvalid] = ypred
    data = data.reshape(nbands, dims[1], dims[2])

    print( "  {0} write_raster".format( time.strftime("%H:%M:%S") ) );
    write_raster(outputfile, data, proj, geo, {}, outputbands, [ 'COMPRESS=lzw', 'INTERLEAVE=BAND', 'TILED=YES' ])
    
    if outputfileStats != None:

        print( "  {0} calculate_stats".format( time.strftime("%H:%M:%S") ) );
        kappa, producers, consumers, overall, maxmiss, cmi, npts = calculate_stats(y, mod.predict(X))
        
        print( "  {0} perform_crossval".format( time.strftime("%H:%M:%S") ) );
        cvAccuracy, cvKappa = perform_crossval(X, y, mod.n_estimators, nproc);
        aveProducers = producers.mean()
        aveConsumers = consumers.mean()

        resultFile = open(outputfileStats, 'wt');
        resultWriter = csv.writer(resultFile);

        resultWriter.writerow( ["kappa", kappa ] )
        resultWriter.writerow( ["producers", producers ] )
        resultWriter.writerow( ["consumers", consumers ] )
        resultWriter.writerow( ["overall", overall ] )
        resultWriter.writerow( ["maxmiss", maxmiss ] )
        resultWriter.writerow( ["cmi", cmi ] )
        resultWriter.writerow( ["npts", npts ] )
        resultWriter.writerow( ["cvAccuracy", cvAccuracy ] )
        resultWriter.writerow( ["cvKappa", cvKappa ] )
        resultWriter.writerow( ["aveProducers", aveProducers ] )
        resultWriter.writerow( ["aveConsumers", aveConsumers ] )

        resultFile.close();
        
    
def run(rasterfile, shapefile, attribute, fillvalue, suffix, dominant, noprobs, stats, 
        crossval, nproc, ntree, rasterfiles=None, usebands=None):

    print "extracting training data..."
    result = library_table(rasterfile, shapefile, attribute, fillvalue, usebands)

    X = np.array(result['value'])
    y = np.array(result['class'])

    print X.shape
    print y.shape

    if np.any(np.isnan(X)):
        raise Exception, "There are NAN values in %s" % rasterfile
    
    if ntree == -1:
        print "calculating optimal number of trees...",
        mod = optimize_model(X, y, nproc)
        print mod.n_estimators
    else:
        mod = RandomForestClassifier(n_estimators=ntree, max_depth=None, min_samples_split=1,
                                     random_state=0, n_jobs=nproc)

    print "fitting random forest model..."
    mod.fit(X, y)

    # within sample statistics
    if stats:
        print "calculating statistics..."
        present_stats(y, mod.predict(X))
    # out of sample statistics
    if crossval:
        print "performing crossvalidation..."
        cvAccuracy, cvKappa = perform_crossval(X, y, mod.n_estimators, nproc)
        print "\nMean out-of-sample accuracy"
        print cvAccuracy
        print "\nMean out-of-sample Kappa"
        print cvKappa, "\n"

    # deal with list of rasters for prediction
    if not rasterfiles:
        rasterfiles = [rasterfile]
    #elif rasterfile not in rasterfiles:
    #    rasterfiles.append(rasterfile)
    
    for rasterfile in rasterfiles:
        print "reading raster data from %s..." % rasterfile
        data, proj, geo, meta = read_raster(rasterfile)    
        if usebands is not None:
            usebands = [b - 1 for b in usebands]
            data = data[usebands, :]
        dims = data.shape

        if len(dims) != 3:
            assert len(dims) == 2, "unexpected image dimensions: %d" % len(dims)            
            data = data.reshape(1, dims[0], dims[1])
            dims = list(dims)
            dims = tuple([1, dims[0], dims[1]])

        data = data.reshape(dims[0], dims[1]*dims[2]).T
        if np.any(np.isnan(data)):
            raise Exception, "There are NAN values in %s" % rasterfile
            #data[np.isnan(data)] = fillvalue

        print "assigning classes to pixels..."
        if fillvalue is not None:
            wvalid = np.all(data != fillvalue, axis=1)
        else:
            wvalid = np.arange(dims[1]*dims[2])
        if noprobs:
            # output only dominant class
            ypred = mod.predict(data[wvalid,:]).astype('uint16').T
            nbands = 1
        else:
            # calculate class probabilities
            ypred = (100*mod.predict_proba(data[wvalid,:])).astype('uint16').T
            nbands = len(set(result['class']))
            if dominant:
                # output only probabilities
                x = ypred.argmax(axis=0).astype('uint16') + 1
                ypred = np.vstack((x, ypred))
                nbands += 1

        data = np.zeros((nbands, dims[1]*dims[2]), dtype='int16')
        data[:,wvalid] = ypred
        data = data.reshape(nbands, dims[1], dims[2])

        fbase,ext = os.path.splitext(os.path.basename(rasterfile))
        outputfile = fbase + suffix + ext
        print "writing file %s..." % outputfile
        write_raster(outputfile, data, proj, geo, {})

def main():    
    
    prog = os.path.split(__file__)[1]
    parser = argparse.ArgumentParser(prog=prog, 
        description='Supervised classification using random forest', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--raster', required=True,
                        help='raster file for training')

    parser.add_argument('rasters', nargs='*', default=None,
                        help='additional rasters for prediction')

    parser.add_argument('-v', '--vector', required=True,
                        help='vector file containing training polygons')
    parser.add_argument('-a', '--attribute', required=True,
                        help='vector attribute containing class IDs')
    parser.add_argument('-s', '--suffix', default='_garsect', 
                        help='suffix to append to output')
    parser.add_argument('-m', '--missing', default=None, type=float,
                        help='missing value')
    parser.add_argument('-d', '--dominant', default=False, action='store_true',
                        help='include dominant class in output')
    parser.add_argument('-n', '--noprobs', default=False, action='store_true',
                        help='do not include class probabilities in output')
    parser.add_argument('--stats', default=False, action='store_true',
                        help='output classification statistics')
    parser.add_argument('-c', '--crossval', default=False, action='store_true',
                        help='perform cross-validation analysis to choose fitting parameter')
    parser.add_argument('-p', '--procs', default=5, type=int, choices=xrange(1,MAXPROCS+1),
                        help='number of processes to use (max %d)' % MAXPROCS)
    parser.add_argument('-t', '--trees', default=10, type=int,
                        help='number of trees to use (-1 to optimize)')
    parser.add_argument('-b', '--bands', default=None, type=int, nargs='+',
                        help='which bands to use starting with 1 (default: all)')

    parser.add_argument('--version', action='version', version=prog+' '+ __version__)

    args = parser.parse_args()

    if args.procs < 1 or args.procs > MAXPROCS:
        args.procs = MAXPROCS
    if args.trees < -1 or 0: 
       raise Exception, "number of trees must be greater than zero" 

    run(args.raster, args.vector, args.attribute, args.missing, args.suffix, args.dominant,
        args.noprobs, args.stats, args.crossval, args.procs, args.trees, args.rasters, args.bands)


if __name__ == "__main__":
    main()

