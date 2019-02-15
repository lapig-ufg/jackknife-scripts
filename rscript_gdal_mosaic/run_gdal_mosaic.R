DTym <- seq.Date(from = ymd('2000-01-01'), to = ymd('2019-12-01'),  by = 'month')
imagesNames <- c(paste0("aglivc_", DTym), paste0("bglivs_", DTym), paste0("somsc_", DTym), paste0("stdeadc_", DTym))

listImages <- paste0('gdalbuildvrt mosaics/', imagesNames, ".vrt", " ", 'resultRasterAqua/', imagesNames, "*.tif")
listTifWrite <- paste0("gdal_translate -a_srs 'EPSG:4326' -co COMPRESS=LZW -co TILED=True mosaics/", imagesNames, ".vrt mosaics/", imagesNames, ".tif")
listVrtTif <- paste0 (listImages, '; ', listTifWrite)

write.table(listVrtTif, file = '/data/SENTINEL/media_mensal_ndvi/vrtTifcenturyImageListToMosaic.txt', row.names = FALSE, col.names = FALSE, quote = FALSE)

