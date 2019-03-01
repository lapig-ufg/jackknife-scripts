#####################################################################
#####################################################################
#'

###
###
# Workstation
setwd('Y:\\CENTURYCERRADO/mosaicsWorkstation/block_34')
filesNames <- list.files(pattern = '*.tif')
newNames <- gsub("01.tif", "01_wk.tif", filesNames)

file.rename(filesNames, newNames)

###
###
# Áqua
setwd('Y:\\CENTURYCERRADO/mosaics')
filesNames <- list.files(pattern = '*.tif')
newNames <- gsub("01.tif", "01_aqua.tif", filesNames)

file.rename(filesNames, newNames)
#####################################################################
#####################################################################
