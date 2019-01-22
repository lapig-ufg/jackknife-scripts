suppressMessages(library(rgdal))
suppressMessages(library(raster))
suppressMessages(library(parallel))

# Read shapefile
features <- suppressMessages(readOGR(dsn = "X:\\BFAST01/shape", layer = "PRODES_2017_centroide", 
	verbose=FALSE, stringsAsFactors=FALSE))
coordinates <- features[,]@coords

ndvi <- brick("Y:\\BFAST10/shape/mod13q1_ndvi_maxmin_list.tif")

# data_frame_ndvi <- as.data.frame(coordinates[1:5,])
# data_frame_ndvi[,3:425] <- NA
# 
# for(i in 1:5){
#     print(i)
#     data_frame_ndvi[i,3:425] <- ndvi[cellFromXY(ndvi, coordinates[i,])]
#     }
# 

coordinates <- as.data.frame(coordinates)
coordinates$cellNUmber <- cellFromXY(ndvi, coordinates)

f2 <- function(x){
    as.numeric(ndvi[ x[3] ])
}

# df_ndvi <- as.data.frame(t(apply(coordinates[1:5,], 1, f2)))

ncores = 8
clusterPool = makeCluster(ncores)
clusterEvalQ(clusterPool, {
    suppressMessages(library(raster))
    ndvi <- brick("Y:\\BFAST10/shape/mod13q1_ndvi_maxmin_list.tif")
  })

df_ndvi <- parApply(cl = clusterPool, coordinates, 1, f2)
  
df_ndvi_2 <- as.data.frame(t(df_ndvi))
data_frame_ndvi <- data.frame(coordinates, df_ndvi_2)

write.table(data_frame_ndvi, file = "X:\\DATASAN/teste-final_56k.csv", col.names = FALSE, row.names = FALSE, sep = ";")
