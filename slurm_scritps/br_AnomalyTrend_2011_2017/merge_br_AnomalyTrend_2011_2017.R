#args <- commandArgs(trailingOnly = TRUE)

rasterMerge <-function(inputDir, outputDir, sufixName, pattern){
STTot <- Sys.time()

    outputFile <- paste0(outputDir, "/", sufixName, ".tif")

print(sufixName)
print(outputFile)

    lsf <- mixedsort(
      Sys.glob(
        file.path(inputDir, paste0(sufixName, pattern))
        )
      )
lsf[1:5]
    rasterList <- list()
    for(i in 1:length(lsf)){
        rasterList[[i]] <- raster(lsf[i])
    }
    outputMerge <- do.call(merge, rasterList)

    writeRaster(outputMerge, filename = outputFile)

print(Sys.time() - STTot)
}

#Run
suppressWarnings(suppressMessages(library(raster)))
suppressWarnings(suppressMessages(library(gtools)))

inputDir <- '/data/SENTINEL/DATASAN/br_anomalytrend_2011_2017/blocks_5row_21592col'
outputDir <- '/data/SENTINEL/DATASAN/br_anomalytrend_2011_2017/br_mosaics'
pattern <- "*.tif"

sufixNameList <- c('slope_block',
	#'modelDif_block',
	'pvalue_block',
	'intercept_block',
    'rsquared_block')
    # 'acumDif_block'

#print(as.data.frame(sufixNameList))
for(i in 1:4){
print(i)
sufixName <- sufixNameList[i]
print(sufixName)
rasterMerge(inputDir, outputDir, sufixName, pattern)
}