id='1222 strucchange'
# lon=-71.7339
# lat=-4.5797
lon=-47.409027978
lat=-14.8124019099999
filename=paste0(c(id),'.png')

png(paste(filename, sep=""),height=600, width=1200)

library(raster)
#library(AnomalyDetection)
#library(changepoint)
library(strucchange)
library(ggplot2)
library(fpp) # for 'ausair' data
library(ggfortify) # enable timeseries in autoplot

ndvi <- brick("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/mod13q1_ndvi_maxmin_list.tif")

cellNumber <- cellFromXY(ndvi, c(lon, lat))
pix_ndvi <- as.numeric(ndvi[cellNumber])


ts_pix_ndvi <- ts(pix_ndvi, start = 2000.49, frequency = 23)
#ts_pix_ndvi <- ts(pix_ndvi[308:423], start= 2012.49, frequency = 23)


bpts <- breakpoints(ts_pix_ndvi ~ 1)# get the breakpoints

bpts_ts_pix_ndvi <- autoplot(bpts, size=0.5, cpt.linetype="solid") +

labs(x="Date", y="ts_pix_ndvi", title="Strucchange with breakpoint function mod13q1 pixel", subtitle=cellNumber) + # add labels

theme(plot.title = element_text(size=20, face="bold", vjust=2), # style the axis and title text

axis.title.x=element_text(size=15, vjust=0.5),

axis.title.y=element_text(size=15, vjust=0.5),

axis.text.x=element_text(size=15, vjust=0.5),

axis.text.y=element_text(size=15, vjust=0.5),

plot.margin=unit(c(10,10,0,0),"mm")) # adjust plot margin


plot(bpts_ts_pix_ndvi, main = paste0('Strucchange mod13q1 pixel ', cellNumber))

dev.off()