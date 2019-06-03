suppressMessages(library(bfast))
suppressMessages(library(raster))
suppressMessages(library(dplyr))

args = as.numeric(commandArgs(trailingOnly=TRUE))

# Retrieve the ids of the coordinates in the csv file
features <- read.csv("/data/DADOS_GRID/result_BFASTMonitor/ids_pontos_faltando.csv", fill = TRUE, sep = ",")
ndvi <- brick("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig_2000_2019.tif")

### Rodando para pontos faltantes:
distinct_ids = features %>% select(seq_id) %>% distinct(seq_id)
distinct_vector = distinct_ids$seq_id

select_seq_id <- features %>% select(lon, lat, seq_id) %>% filter(seq_id == distinct_vector[args])
# coordinatesRow <- select_seq_id %>% select(lon, lat)
# coords_mat_s4 <- as.matrix(coordinatesRow)

lat = select_seq_id$lat[1]
lon = select_seq_id$lon

# OK
# lat = -18.9048292
# lon = -43.872104

# Error
# lat = -8.87707128
# lon = -49.6984509


# Creating a Coordinate S4 Class
# setClass("coordinates", slots=list(lon="numeric", lat="numeric"))
# s4_coordinates <- new("coordinates", lon = select_seq_id$lon, lat = select_seq_id$lat)


bfast_apply = function(lon, lat) {

outError <- tryCatch( {

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

	# any(na.rm = TRUE, ndvi_vals == "-Inf")
	if (any(ndvi_vals %in% "-Inf")) {

		result_bfastmonitor <- cbind(monitor_breakpoint = NA, monitor_magnitude = NA)

	} else {

		ndvi_ts <- ts(ndvi_vals, start= c(2000, 2), frequency = 23)

		result_bfastmonitor <- run_bfast_monitor(ndvi_ts)
	
	}

	result = data.frame(
		"lon" = lon,
		"lat" = lat
	)

	bfastMonitorResult <- cbind(result, result_bfastmonitor)
	bfastMonitorTableFormated <- write.table(bfastMonitorResult, col.names = FALSE, row.names = FALSE, sep = ";")


	}, error = function(err){
		message(paste("Error in :", lon, lat))
		message(err)
	}
	# , finally = {
	# 	print("Teste finally")
	# }

	)

}

for (i in 1:length(lon)) {
	bfast_apply(lon[i], lat)
}