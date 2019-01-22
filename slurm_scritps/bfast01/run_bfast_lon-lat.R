
#filename='monotonic_inc.png'
#lon=-42.379056
#lat=-3.168873

#filename='monotonic_dec.png'
#lon=-43.825601
#lat=-6.914239

#filename='monotonic_inc_pos_sig_break.png'
#lon=-54.27952550
#lat=-17.16143001

#filename='monotonic_dec_neg_sig_break.png'
#lon=-49.7780483
#lat=-11.0488255

#filename='interruption_inc_neg_sig_break.png'
#lon=-45.15270441
#lat=-12.36690067

#filename='interruption_dec_pos_sig_break.png'
#lon=-44.7388848
#lat=-6.0951932

#filename='reversal_inc_dec.png'
#lon=-45.69899981
#lat=-15.78634698

#filename='reversal_dec_inc.png'
#lon=-53.3127168
#lat=-18.2359133

#Desmatamento DETER

id='11111 bfast01'
lon=-71.7339
lat=-4.5797
# lon=-47.409027978
# lat=-14.8124019099999
filename=paste0(c(id),'.png')

png( paste(filename, sep=""),height=600, width=1200)

library(bfast)
library(raster)

ndvi <- brick("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/mod13q1_ndvi_maxmin_list.tif")

cellNumber <- cellFromXY(ndvi, c(lon, lat))
pix_ndvi <- as.numeric(ndvi[cellNumber])

#print(pix_ndvi)
ts_pix_ndvi <- ts(pix_ndvi, start= 2000.49, frequency = 23)
#ts_pix_ndvi <- ts(pix_ndvi[308:423], start= 2012.49, frequency = 23)


#mon <- bfastmonitor(ts_pix_ndvi, start = c(2000, 49), formula = response ~ harmon + trend, history = "all")


bf_ts_pix_ndvi  <- bfast01(ts_pix_ndvi, trim=23)
#bf_ts_pix_ndvi  <- bfast01(ts_pix_ndvi, h=0.15)
#bf_ts_pix_ndvi  <- bfast01(ts_pix_ndvi, trim=16)

# "Rec-CUSUM", "OLS-CUSUM", "Rec-MOSUM", "OLS-MOSUM"  "RE", "ME", "fluctuation", "Score-CUSUM", "Nyblom-Hansen", "Chow", "supF", "aveF", "expF"

#ts_pix_ndvi <- ts(pix_ndvi, start= 2000.49, frequency = 23)
#bf_ts_pix_ndvi  <- bfast01(ts_pix_ndvi, trim=16)
#classify = bfast01classify(bf_ts_pix_ndvi, pct_stable=0.50)

#print(bf_ts_pix_ndvi$breakpoints)
#print(classify$flag_type)
#print(classify$flag_significance)
#print(classify$flag_pct_stable)
#print(classify)
#print(bf_ts_pix_ndvi['Coefficients'])
plot(bf_ts_pix_ndvi, main = paste0('BFAST: mod13q1 pixel ', cellNumber))

dev.off()
