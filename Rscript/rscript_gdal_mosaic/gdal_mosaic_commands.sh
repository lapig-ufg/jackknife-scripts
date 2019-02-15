
'aglivc'
'bglivs'
'somsc'
'stdeadc'


gdalbuildvrt mosaics/aglivc_2000-01-01.vrt resultRasterAqua/aglivc_2000-01-01*.tif
gdal_translate -a_srs 'EPSG:4326' -co COMPRESS=LZW -co TILED=True mosaics/aglivc_2000-01-01.vrt mosaics/aglivc_2000-01-01.tif


gdalbuildvrt mosaics/aglivc_2000-01-01 resultRasterAqua/aglivc_2000-01-01*.tif;  gdal_translate -a_srs 'EPSG:4326' -co COMPRESS=LZW -co TILED=True mosaics/aglivc_2000-01-01.vrt mosaics/aglivc_2000-01-01.tif
