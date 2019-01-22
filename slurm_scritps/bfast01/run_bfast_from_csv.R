suppressMessages(library(parallel))

args <- commandArgs(trailingOnly = TRUE)

# Read only range args of the shapefile
features <- read.csv("/data/DADOS_GRID/BFAST10/shape/coordinates_ndvi_vals_56k.csv", 
	header = FALSE, fill = TRUE, sep = ";")
coordinates <- features[args[1]:args[2],]

bfast_coord = function(coordinate) {
	
	year_frequency = 23
	start_year = 2000
	start_day = 49
	
	start_date = as.Date(paste0(start_day,'.',start_year), "%j.%Y")
	start_date_1218 = as.Date(paste0(start_day,'.',2013), "%j.%Y")

	breakpoint2date = function(breakpoint) {
		day_resolution = 16
		
		doy = ((breakpoint %% year_frequency)-1) * day_resolution + start_day
		year = (start_year + floor(breakpoint / year_frequency))

		# Year turn logic
		if (doy > 365) {
			
			doy = doy - 365
			year = year + 1
			
			if (doy < day_resolution) {
				doy = 1 # Year always start in day one
			}

		}

		return( as.Date(paste0(doy,'.',year), "%j.%Y") )
	}

	lon <- coordinate[1]
	lat <- coordinate[2]
	ndvi_vals <- c(coordinate[3:425])


	ndvi_ts = ts(ndvi_vals, start= start_date, frequency = year_frequency)
	bfast01_ndvi  <- bfast01(ndvi_ts, trim=16)
	blassify_ndvi = bfast01classify(bfast01_ndvi, pct_stable=0.50)
	
	ndvi_ts_1218 <- ts(ndvi_vals[308:423], start= start_date_1218, frequency = year_frequency)
	bfast01_ndvi_1218  <- bfast01(ndvi_ts_1218, trim=16)
	blassify_ndvi_1218 = bfast01classify(bfast01_ndvi_1218, pct_stable=0.50)

	data.frame(
		"lon" = lon,
		"lat" = lat,
		
		"breakpoint" = bfast01_ndvi$breakpoints, 
		"breakdate" = breakpoint2date(bfast01_ndvi$breakpoints), 
		"flag_type" = blassify_ndvi$flag_type,
		"flag_significance" = blassify_ndvi$flag_significance,
		"flag_pct_stable" = blassify_ndvi$flag_pct_stable,

		"breakpoint_1218" = 308 + bfast01_ndvi_1218$breakpoints, 
		"breakdate_1218" = breakpoint2date(308 + bfast01_ndvi_1218$breakpoints), 
		"flag_type_1218" = blassify_ndvi_1218$flag_type,
		"flag_significance_1218" = blassify_ndvi_1218$flag_significance,
		"flag_pct_stable_1218" = blassify_ndvi_1218$flag_pct_stable
	)
}

ncores = detectCores()
clusterPool = makeCluster(ncores)
hideOutput <- capture.output(output <- clusterEvalQ(clusterPool, {
	library(bfast)
}))

# Run bfast and write csv
bfastResultList <- parApply(cl = clusterPool, coordinates, 1, bfast_coord)

bfastResultListTableFormated <- write.table(bfastResult <- do.call('rbind', bfastResultList), 
	col.names = FALSE, row.names = FALSE, sep = ";")
