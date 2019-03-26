id=2
lon=-50.148393
lat=-14.227223
filename=paste0(c(id),'.png')

png( paste(filename, sep=""),height=600, width=800)

library(bfast)
library(raster)

ndvi <- brick("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/mod13q1_ndvi_maxmin_list.tif")

cellNumber <- cellFromXY(ndvi, c(lon, lat))
pix_ndvi <- as.numeric(ndvi[cellNumber])

pix_ndvi_ts <- ts(pix_ndvi, start= c(2000,2), frequency = 23)
bf1 <- bfast01(pix_ndvi_ts, trim=23, test=c("Rec-CUSUM", "Score-CUSUM", "ME", "aveF"), aggregate=any, bandwidth=0.05)
bfResult <- bfast01classify(bf1)

plot(bf1, main = paste0('BFAST: mod13q1 pixel ', cellNumber))

dev.off()