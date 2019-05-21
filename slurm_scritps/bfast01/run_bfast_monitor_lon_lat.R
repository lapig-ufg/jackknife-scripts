id=111
lon=-49.345059
lat=-10.242655
filename=paste0(c(id),'.png')

# -43.2488982043563;-2.51744429283775

png( paste(filename, sep=""),height=600, width=1200)

library(bfast)
library(raster)

#ndvi <- brick("/data/DADOS_GRID/BFAST10/shape/mod13q1_ndvi_maxmin_list.tif")
ndvi <- brick("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig/pa_br_ndvi_maxmin_250.vrt")

cellNumber <- cellFromXY(ndvi, c(lon, lat))
pix_ndvi <- as.numeric(ndvi[cellNumber])

ts_pix_ndvi <- ts(pix_ndvi, start= c(2000, 2), frequency = 23)
monitor <- bfastmonitor(ts_pix_ndvi, start = c(2015, 12), formula = response ~ harmon + trend, history = "all")

print(monitor$breakpoint)
print(monitor$magnitude)

plot(monitor, main = paste0('BFAST monitor: mod13q1 pixel ', cellNumber))

dev.off()


#bfm1 <- bfmPixel(bf_ts_pix_ndvi, cell=pix_ndvi, start=c(2000, 49), formula=response~harmon, plot=TRUE)