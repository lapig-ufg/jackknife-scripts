id='111 meanvar cerrado 1'
# Floresta Amazonica 1
# lon=-71.7339
# lat=-4.5797

# Floresta Amazonica 2
# lon=-63.3465
# lat=-2.3445

# Cerrado 1
# lon=-47.409027978
# lat=-14.8124019099999

# Cerrado 2
lon=-49.321339833
lat=-12.5992400109999

filename=paste0(c(id),'.png')

png(paste(filename, sep=""),height=600, width=1200)

library(raster)
suppressMessages(library(changepoint))
suppressMessages(library(ggplot2))
suppressMessages(library(ggfortify)) # enable timeseries in autoplot

ndvi <- brick("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/mod13q1_ndvi_maxmin_list.tif")

cellNumber <- cellFromXY(ndvi, c(lon, lat))
pix_ndvi <- as.numeric(ndvi[cellNumber])


ts_pix_ndvi <- ts(pix_ndvi, start = 2000.49, frequency = 23)
#ts_pix_ndvi <- ts(pix_ndvi[308:423], start= 2012.49, frequency = 23)


cpt_ts_pix_ndvi <- autoplot(cpt.meanvar(ts_pix_ndvi), size=0.5) +

# minseglen=1

# cpt.mean single change point
# pen.value=1, penalty='Manual', test.stat='CUSUM'


# PELT, fast and exact
# cpt.mean(ts_pix_ndvi, method='PELT', pen.value=1, penalty='Manual')

labs(x="Date", y="ts_pix_ndvi", title="Changepoint mod13q1 pixel", subtitle=cellNumber) + # add labels

theme(plot.title = element_text(size=20, face="bold", vjust=2), # style the axis and title text

axis.title.x=element_text(size=15, vjust=0.5),

axis.title.y=element_text(size=15, vjust=0.5),

axis.text.x=element_text(size=15, vjust=0.5),

axis.text.y=element_text(size=15, vjust=0.5),

plot.margin=unit(c(10,10,0,0),"mm")) # adjust plot margin


plot(cpt_ts_pix_ndvi, main = paste0('Changepoint mod13q1 pixel ', cellNumber))

dev.off()

# cpt.mean(ts_pix_ndvi, penalty='None', pen.value=1, test.stat='CUSUM')

# cpt_ts_pix_ndvi <- cpt.var(ts_pix_ndvi, penalty='Manual', test.stat='CSS')



# Cerrado 1, Changepoint Locations : 402
# cpt.var(ts_pix_ndvi, penalty='Manual', pen.value="log(2*log(n))", method='BinSeg', test.stat='Normal', Q=1)


# Amazonia 2, Changepoint Locations : 181
# cpt.var(ts_pix_ndvi, penalty='Manual', pen.value="log(2*log(n))", method='BinSeg', test.stat='Normal', Q=1)