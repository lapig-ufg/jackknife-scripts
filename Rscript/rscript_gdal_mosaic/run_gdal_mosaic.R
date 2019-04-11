imagesNames <- paste0("ndvi_", 1:26, "_")

listImages <- paste0('gdalbuildvrt mosaics/', imagesNames, "mosaic.vrt", " ", imagesNames, "*.tif")
listTifWrite <- paste0("gdal_translate -a_srs 'EPSG:4326' -co COMPRESS=LZW -co TILED=True mosaics/", imagesNames, "mosaic.vrt mosaics/", imagesNames, "mosaic.tif")
listVrtTif <- paste0 (listImages, '; ', listTifWrite)

write.table(listVrtTif, file = '/data/SENTINEL/pa_br_ndvi_maxmin_250_lapig/mosaics/maxminFilter_ImageListToMosaic.txt', row.names = FALSE, col.names = FALSE, quote = FALSE)

