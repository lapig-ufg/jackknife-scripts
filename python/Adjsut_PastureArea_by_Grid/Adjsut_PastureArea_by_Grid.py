import os
import sys
import numpy
import glob
import pandas as pd
import fiona
import rasterio
import rasterio.mask

def loop_zonal_stats(input_zone_polygon, input_raster_dir,field_name,out_dir,precision = 100):

    df = pd.DataFrame()

    precision = int(precision)

    shapefile = fiona.open(input_zone_polygon, "r") 

    input_rasters = glob.glob(os.path.join(input_raster_dir,'*.tif'))

    for feature in shapefile:

        geometry = feature["geometry"] 
        grid_name = feature["properties"]["TILE_T"] 
        feature_id = feature["id"] 

        for raster in input_rasters:

            result = {}

            year = str(os.path.basename(raster)[:5]) 

            print(year)

            if int(year[1:]) > 2018:

                continue

            grid_pasture_area = float(feature["properties"][str(year)+'_area'])
            grid_pasture_prop = float(feature["properties"][str(year)+'_prop'])

            with rasterio.open(raster) as raster_src:
                clip_image, transform = rasterio.mask.mask(raster_src, [geometry], crop=True)
                out_meta = raster_src.meta

            pixelWidth = out_meta['transform'][0]
            pixelHeight = out_meta['transform'][4]

            #####################################

            base_cut_value = 5100
            base_area = numpy.sum(clip_image >= base_cut_value)
            total_area = numpy.sum(clip_image > 0)

            base_prop = float(base_area/total_area)

            adjust_prop = base_prop

            if grid_pasture_prop > base_prop:

                while grid_pasture_prop > adjust_prop:

                    base_cut_value -= precision

                    adjust_prop = numpy.sum(clip_image >= base_cut_value)/total_area

            elif grid_pasture_prop < base_prop:

                while grid_pasture_prop < adjust_prop:

                    base_cut_value += precision

                    adjust_prop = numpy.sum(clip_image >= base_cut_value)/total_area

            else:
                adjust_prop = base_prop

            adjust_area = float(numpy.sum(clip_image >= base_cut_value))*((pixelWidth*(pixelHeight*-1))/10000.0)

            array2export = numpy.where(clip_image >= base_cut_value,1,0)

            out_meta.update({"driver": "GTiff",
                 "height": clip_image.shape[1],
                 "width": clip_image.shape[2],
                 "dtype": array2export.dtype,
                 "compress": 'lzw',
                 "transform": transform})

            if os.path.exists(os.path.join(out_dir,year)) is False:
                os.mkdir(os.path.join(out_dir,year))

            with rasterio.open(os.path.join(out_dir,year,os.path.basename(raster)[:-4]+'_adjusted.tif'), "w", **out_meta) as out_raster:
                out_raster.write(array2export)

            #####################################

            result['ID'] = int(feature_id)
            result['Grid'] = str(grid_name)
            result['Ano'] = int(year[1:])
            result['total_area'] =  float(total_area*((pixelWidth*(pixelHeight*-1))/10000.0))
            result['base_area_51'] =  float(base_area*((pixelWidth*(pixelHeight*-1))/10000.0))
            result['base_prop_51'] = float(base_prop)
            result['estimated_area'] = float(grid_pasture_area)
            result['estimated_prop'] = float(grid_pasture_prop            )
            result['adjust_area'] = float(adjust_area)
            result['adjusted_prop'] = float(adjust_prop)
            result['cut_value'] = float(base_cut_value)

            df  = pd.concat([df,pd.DataFrame(result,index=[0])])


    year_dirList = [directory for directory in os.listdir(out_dir) if os.path.isdir(os.path.join(out_dir,directory))]

    for year in year_dirList:

        files = glob.glob(os.path.join(out_dir,year,'*.tif'))

        os.system('gdalbuildvrt -srcnodata 0 -vrtnodata 0 ' + os.path.join(out_dir,year +'.vrt ') + ' '.join(files))
        os.system('gdal_translate -a_nodata 0 -of COG ' + os.path.join(out_dir,year +'.vrt ')+ os.path.join(out_dir,year +'.cog ') + '-co COMPRESS=LZW -co BIGTIFF=IF_NEEDED')
        os.system('del ' + os.path.join(out_dir,year +'.vrt '))

    output_name = os.path.join(out_dir,'Pasture_Grid_Adjust_Percentage_Brasil.csv')

    df = df.replace(numpy.nan, 0)

    pd.options.display.float_format = '{:.4f}'.format

    df.to_csv(output_name,mode='w',index = False,sep =';')

    print('The entire process is now over. Take a good nap!')

loop_zonal_stats(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
