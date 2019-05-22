suppressMessages(library(rgdal))
suppressMessages(library(parallel))

args = commandArgs(trailingOnly=TRUE)

layername = tools::file_path_sans_ext(args[1])

print("Reading shapefile")
features <- suppressMessages(readOGR(dsn = ".", layer = layername, verbose=FALSE, stringsAsFactors=FALSE))
coordinates <- features@coords
coordinates <- coordinates[args[2]:args[3],]

bfast_apply = function(coordinate) {
	
	run_bfast_monitor = function(ndvi_ts) {
		
		monitor <- bfastmonitor(ndvi_ts, start = c(2015, 12), formula = response ~ harmon + trend, history = "all")

		monitor_breakpoint = monitor$breakpoint
		monitor_magnitude = monitor$magnitude

		return(data.frame( 
				"monitor_breakpoint" = monitor_breakpoint,
				"monitor_magnitude" = monitor_magnitude
			))
	}

	ndvi <- brick("/data/DADOS_GRID/BFAST10/shape/mod13q1_ndvi_maxmin_list.tif")
	#ndvi <- brick("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig/pa_br_ndvi_maxmin_250.vrt")

	lon <- coordinate[1]
	lat <- coordinate[2]
	cell <- cellFromXY(ndvi, c(lon, lat))
	ndvi_vals <- as.numeric(ndvi[cell])
	
	# ndvi_vals <- ndvi_vals[1:414]

	ndvi_ts <- ts(ndvi_vals, start= c(2000, 2), frequency = 23)

	result_bfastmonitor <- run_bfast_monitor(ndvi_ts)

	result = data.frame(
		"lon" = lon,
		"lat" = lat
	)

	cbind(result, result_bfastmonitor)
}

ncores = detectCores()
clusterPool = makeCluster(ncores)


hideOutput <- capture.output(output <- clusterEvalQ(clusterPool, {
  	suppressMessages(library(bfast))
	suppressMessages(library(raster))
	suppressMessages(library(rgdal))
}))

# startTime <- Sys.time()
# print("Running bfast")

bfastResultList <- parApply(cl = clusterPool, coordinates, 1, bfast_apply)
bfastResult <- do.call('rbind', bfastResultList)

# endTime <- Sys.time()
# cat("time:\n")
# print((endTime - startTime))


# bfastResultListTableFormated <- write.table(bfastResult, col.names = FALSE, row.names = FALSE, sep = ";", file = paste0(layername,".csv"))
print("Write CSV file")
write.table(bfastResult, col.names = FALSE, row.names = FALSE, sep = ";", file = paste0(layername,".csv"))