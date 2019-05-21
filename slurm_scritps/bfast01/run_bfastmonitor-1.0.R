library(bfast)
library(raster)

lon=-47.409027978
lat=-14.8124019099999

modisbrick <- brick("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/mod13q1_ndvi_maxmin_list.tif")

cellNumber <- cellFromXY(modisbrick, c(lon, lat))
pix_ndvi <- as.numeric(modisbrick[cellNumber])

ndvi <- bfastts(pix_ndvi, dates, type = c("16-day"))
plot(ndvi/10000)

## derive median NDVI of a NDVI raster brick
# medianNDVI <- calc(modisbrick, fun=function(x) median(x, na.rm = TRUE))
# plot(medianNDVI)

## helper function to be used with the calc() function
xbfastmonitor <- function(x,dates) {
	ndvi <- bfastts(x, dates, type = c("16-day"))
	ndvi <- window(ndvi,end=c(2011,14))/10000
	## delete end of the time to obtain a dataset similar to RSE paper (Verbesselt et al.,2012)
	bfm <- bfastmonitor(data = ndvi, start=c(2010,12), history = c("ROC"))
	return(cbind(bfm$breakpoint, bfm$magnitude))
}

## apply on one pixel for testing
ndvi <- bfastts(as.numeric(modisbrick[1])/10000, dates, type = c("16-day"))
plot(ndvi)

bfm <- bfastmonitor(data = ndvi, start=c(2010,12), history = c("ROC"))
bfm$magnitude
plot(bfm)
xbfastmonitor(modisbrick[1], dates) ## helper function applied on one pixel

## Not run: 
## apply the bfastmonitor function onto a raster brick
library(raster)
timeofbreak <- calc(modisbrick, fun=function(x){
  res <- t(apply(x, 1, xbfastmonitor, dates))
	return(res)
})

plot(timeofbreak) ## time of break and magnitude of change
plot(timeofbreak,2) ## magnitude of change

## create a KMZ file and look at the output
KML(timeofbreak, "timeofbreak.kmz")
