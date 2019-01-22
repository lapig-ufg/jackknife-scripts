suppressMessages(library(rgdal))
suppressMessages(library(raster))

# Read shapefile
features <- suppressMessages(readOGR(dsn = "/data/SENTINEL/BFAST01/shape/", layer = "PRODES_2017_centroide", 
	verbose=FALSE, stringsAsFactors=FALSE))
coordinates <- features[,]@coords


ndvi <- brick("/data/DADOS_GRID/BFAST10/shape/mod13q1_ndvi_maxmin_list.tif")

	cell <- cellFromXY(ndvi, coordinates[1:50,])

data_frame_ndvi <- data.frame(coordinates[1:50,], ndvi[cell])
write.table(data_frame_ndvi, file = "teste-final-30-50.csv", col.names = FALSE, row.names = FALSE, sep = ";")