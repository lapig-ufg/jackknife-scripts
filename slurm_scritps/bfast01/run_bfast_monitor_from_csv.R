library(bfast)
library(raster)
library(dplyr)

# args = commandArgs(trailingOnly=TRUE)

# Retrieve the ids of the coordinates in the csv file
features <- read.csv("/data/SENTINEL/DPAT/BFASTMonitor/ids_seq_teste.csv", fill = TRUE, sep = ",")
ndvi <- brick("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig_2000_2019.tif")

select_seq_id <- features %>% select(lon, lat, seq_id) %>% filter(seq_id == "1")
lat = select_seq_id$lat[1]
lon = select_seq_id$lon
# rowLatNumber <- rowFromY(ndvi, lat)

# cellRow <- cellFromRow(ndvi, rowLatNumber)

#ts_pix_ndvi <- list()

for (i in lon[i]) {
	lon_pix = select_seq_id$lon[i]
	#colLonNumber <- colFromX(ndvi, lon_pix)

	cellNumber <- cellFromXY(ndvi, c(lon_pix, lat))

	pix_ndvi <- as.numeric(ndvi[cellNumber])

	ts_pix_ndvi <- ts(pix_ndvi, start= c(2000, 2), frequency = 23)


	result_lon_lat = data.frame(
		"lon" = lon,
		"lat" = lat
	)

}

# print(ndvi[rowNumber,])

run_bfast_monitor = function(ndvi_ts) {
		
		monitor <- bfastmonitor(ndvi_ts, start = c(2015, 12), formula = response ~ harmon + trend, history = "all")

		monitor_breakpoint = monitor$breakpoint
		monitor_magnitude = monitor$magnitude

		return(data.frame( 
				"monitor_breakpoint" = monitor_breakpoint,
				"monitor_magnitude" = monitor_magnitude
			))
}

result_bfastmonitor <- run_bfast_monitor(ts_pix_ndvi)


bfastMonitorResult <- cbind(result_lon_lat, result_bfastmonitor)


 # <- do.call('rbind', bfastResultList)

print(lon_pix)
print(lat)
print(monitor$breakpoint)
print(monitor$magnitude)