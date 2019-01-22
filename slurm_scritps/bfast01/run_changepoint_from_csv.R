suppressMessages(library(parallel))

args <- commandArgs(trailingOnly = TRUE)

# Read only range args of the csv file
features <- read.csv("/data/DADOS_GRID/BFAST10/shape/coordinates_ndvi_vals_56k.csv", 
	header = FALSE, fill = TRUE, sep = ";")
coordinates <- features[args[1]:args[2],]

changepoint_coord = function(coordinate) {
	
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

		return( as.Date(paste0(doy,'.',year), "%j.%Y"))
	}

	lon <- coordinate[1]
	lat <- coordinate[2]
	ndvi_vals <- as.numeric(c(coordinate[3:425]))


	ndvi_ts = ts(ndvi_vals, start= start_date, frequency = year_frequency)
	cpt_ts_ndvi  <- cpt.var(ndvi_ts, Q=1, penalty='Manual', test.stat='CSS')
	
	
 	ndvi_ts_1218 <- ts(ndvi_vals[308:423], start= start_date_1218, frequency = year_frequency)
	cpt_ts_ndvi_1218  <- cpt.var(ndvi_ts_1218, Q=1, penalty='Manual', test.stat='CSS')

	data.frame(
		"lon" = lon,
		"lat" = lat,
		
		"breakpoint" = cpt_ts_ndvi@cpts[1],
		"breakdate" = breakpoint2date(cpt_ts_ndvi@cpts[1]),
		
		"breakpoint_1218" = 308 + cpt_ts_ndvi_1218@cpts[1],
		"breakdate_1218" = breakpoint2date(308 + cpt_ts_ndvi_1218@cpts[1])
	)
}

ncores = detectCores()
clusterPool = makeCluster(ncores)
hideOutput <- capture.output(output <- clusterEvalQ(clusterPool, {
	library(changepoint)
}))

# Run changepoint and write csv
changepointResultList <- parApply(cl = clusterPool, coordinates, 1, changepoint_coord)

cptResultListTableFormated <- write.table(changepointResult <- do.call('rbind', changepointResultList), 
	col.names = FALSE, row.names = FALSE, sep = ";")


# Teste 1
# cpt.meanvar(ndvi_ts, Q=1)

# Teste 2
# cpt.var(ndvi_ts, Q=1, penalty='Manual', test.stat='Normal')

# Teste 3
# cpt.var(ndvi_ts, Q=1, penalty='Manual', test.stat='CSS')

# Teste....
# cpt.mean(ndvi_ts, Q=1, penalty='None', pen.value=1, test.stat='CUSUM')