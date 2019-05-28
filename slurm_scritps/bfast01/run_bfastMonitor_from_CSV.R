suppressMessages(library(parallel))
suppressMessages(library(bfast))
suppressMessages(library(raster))
suppressMessages(library(dplyr))

args = commandArgs(trailingOnly=TRUE)

# Retrieve the ids of the coordinates in the csv file
features <- read.csv("/data/SENTINEL/DPAT/BFASTMonitor/ids_pontos_bfastMonitor.csv", fill = TRUE, sep = ",")
ndvi <- brick("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig_2000_2019.tif")

select_seq_id <- features %>% select(lon, lat, seq_id) %>% filter(seq_id == args)
# coordinatesRow <- select_seq_id %>% select(lon, lat)
# coords_mat_s4 <- as.matrix(coordinatesRow)

lat = select_seq_id$lat[1]
lon = select_seq_id$lon

# Creating a Coordinate S4 Class
# setClass("coordinates", slots=list(lon="numeric", lat="numeric"))
# s4_coordinates <- new("coordinates", lon = select_seq_id$lon, lat = select_seq_id$lat)


bfast_apply = function(lon, lat) {
	
	run_bfast_monitor = function(ndvi_ts) {
		
		monitor <- bfastmonitor(ndvi_ts, start = c(2015, 12), formula = response ~ harmon + trend, history = "all")

		monitor_breakpoint = monitor$breakpoint
		monitor_magnitude = monitor$magnitude

		return(data.frame( 
				"monitor_breakpoint" = monitor_breakpoint,
				"monitor_magnitude" = monitor_magnitude
			))
	}

	cell <- cellFromXY(ndvi, c(lon, lat))
	ndvi_vals <- as.numeric(ndvi[cell])
	
	# ndvi_vals <- ndvi_vals[1:414]

	ndvi_ts <- ts(ndvi_vals, start= c(2000, 2), frequency = 23)

	result_bfastmonitor <- run_bfast_monitor(ndvi_ts)

	result = data.frame(
		"lon" = lon,
		"lat" = lat
	)

	bfastMonitorResult <- cbind(result, result_bfastmonitor)
	bfastMonitorTableFormated <- write.table(bfastMonitorResult, col.names = FALSE, row.names = FALSE, sep = ";")
}


for (i in 1:length(lon)) {
	bfast_apply(lon[i], lat)
}