suppressWarnings(suppressMessages(library(rgdal)))
suppressWarnings(suppressMessages(library(parallel)))

args = commandArgs(trailingOnly = TRUE)

COL_OFFSET=strtoi(args[1])
ROW_OFFSET=strtoi(args[2])
COL_SIZE=strtoi(args[3])
ROW_SIZE=strtoi(args[4])

# Size is 21592, 18660

#COL_OFFSET=3536
#ROW_OFFSET=6500
#COL_SIZE=50
#ROW_SIZE=50

N_CORES = detectCores()

INPUT_DIR='/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig'
OUTPUT_DIR='/data/SENTINEL/tif_result_bfast_brazil'

getReferenceFile <- function(inputDir, pattern) {
  imageFiles = list.files(path=inputDir, pattern = pattern)
  return(file.path(inputDir, imageFiles[1]))
}

readBlockImages = function(inputDir, blockOffset, blockSize, pattern) {
  imageFiles = list.files(path=inputDir, pattern = pattern)
  imageFiles = sort(imageFiles)

  startTime <- Sys.time()

  cat("Reading", length(imageFiles), 'raster files', '\n')
  cat("Offset:",blockOffset[1], blockOffset[2],'\n')
  cat("Block Size:",blockSize[1], blockSize[2],'\n')
  imageDataList = c()

  for (imageFile in imageFiles) {
    imagePath = file.path(inputDir, imageFile)

    imageGrid <- readGDAL(fname=imagePath,  offset=c(blockOffset[1], blockOffset[2]), region.dim=c(blockSize[1], blockSize[2]), output.dim=c(blockSize[1], blockSize[2]), silent=TRUE)
    imageData <- slot(imageGrid, 'data')

    imageDataList = c(imageDataList, imageData)
  }

  blockImages = do.call('cbind', imageDataList)
  rm(imageDataList)
  gc(verbose=FALSE)

  endTime <- Sys.time()
  cat("Input reading time:\n")
  print((endTime - startTime))

  return(blockImages)
}

runBfast = function(data, ncores) {

  bfastPerPixel = function(data) {
    data <- as.numeric(data)
    
    result = tryCatch({
      data <- na.interp(data)
      ndvi <- ts(data, start= c(2000,2), frequency = 23)
      bf1 <- bfast01(ndvi, trim=23, test=c("Rec-CUSUM", "Score-CUSUM", "ME", "aveF"), aggregate=any, bandwidth=0.05)
      bfResult <- bfast01classify(bf1)

      modelParams = bf1$model[[2]][1]

      bfResult$segment1 = modelParams$coefficients['segment1']
      bfResult$segment2 = modelParams$coefficients['segment2']
      bfResult$trend1 = modelParams$coefficients['segment1:trend']
      bfResult$trend2 = modelParams$coefficients['segment2:trend']

      bfResult$breakdate <- bf1$breakpoint

      return(bfResult)
    }, error = function(e) {
      emptyData <- matrix(ncol = 12, nrow = 1)
      # colNames <- as.numeric(c('flag_type','flag_significance', 'flag_pct_stable', 'trend1', 'trend2'))
      colNames <- c('flag_type','flag_significance','p_segment1','p_segment2','pct_segment1','pct_segment2', 'flag_pct_stable', 'breakdate', 'segment1', 'segment2', 'trend1', 'trend2')

      emptyResult <- setNames(data.frame(emptyData), colNames)
      return(emptyResult)
    })

    return(result)
  }

  cat("Running Bfast01", '\n')
  startTime <- Sys.time()

  clusterPool = makeCluster(ncores)
  clusterEvalQ(clusterPool, {
    library(bfast)
    library(forecast)
  })

  bfastResultList <- parApply(cl = clusterPool, blockData, 1, bfastPerPixel)
  bfastResult <- do.call('rbind', bfastResultList)

  rm(bfastResultList)
  gc(verbose=FALSE)

  endTime <- Sys.time()
  cat("CPU time:\n")
  print((endTime - startTime))
  
  return(bfastResult)
}

saveImage = function(outputData, outputfile, blockOffset, blockSize, referenceFile, dtype) {

  referenceGdal <- readGDAL(fname=referenceFile, offset=blockOffset, region.dim=blockSize, output.dim=blockSize, silent=TRUE)
  outputDataSpatialGrd <- SpatialGridDataFrame(referenceGdal@grid, data=as.data.frame(outputData))
  writeGDAL(outputDataSpatialGrd, outputfile, drivername="GTiff", type=dtype, options="COMPRESS=LZW, TILED=TRUE")

}

saveBfastResult = function(bfastResult, referenceFile, blockOffset, blockSize) {

  startTime <- Sys.time()

  cat("Writing 11 output files \n")
  
  flagsFile = paste0(OUTPUT_DIR, '/', 'flags-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$flag_type, flagsFile, blockOffset, blockSize, referenceFile, "Byte")
  
  flagsSignificanceFile = paste0(OUTPUT_DIR, '/', 'flags-significance-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(as.numeric(bfastResult$flag_significance), flagsSignificanceFile, blockOffset, blockSize, referenceFile, "Float32")

  flagsPctSeg1File = paste0(OUTPUT_DIR, '/', 'pct-seg1-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$pct_segment1, flagsPctSeg1File, blockOffset, blockSize, referenceFile, "Float32")
  
  flagsPctSeg2File = paste0(OUTPUT_DIR, '/', 'pct-seg2-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$pct_segment2, flagsPctSeg2File, blockOffset, blockSize, referenceFile, "Float32")

  flagsPSeg1File = paste0(OUTPUT_DIR, '/', 'p-seg1-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$p_segment1, flagsPSeg1File, blockOffset, blockSize, referenceFile, "Float32")

  flagsPSeg2File = paste0(OUTPUT_DIR, '/', 'p-seg2-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$p_segment2, flagsPSeg2File, blockOffset, blockSize, referenceFile, "Float32")

  breakdateFile = paste0(OUTPUT_DIR, '/', 'breakdate-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(as.numeric(bfastResult$breakdate), breakdateFile, blockOffset, blockSize, referenceFile, "Int32")

  segment1File = paste0(OUTPUT_DIR, '/', 'segment1-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$segment1, segment1File, blockOffset, blockSize, referenceFile, "Float32")

  segment2File = paste0(OUTPUT_DIR, '/', 'segment2-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(bfastResult$segment2, segment2File, blockOffset, blockSize, referenceFile, "Float32")

  trend1File = paste0(OUTPUT_DIR, '/', 'trend1-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(as.numeric(bfastResult$trend1), trend1File, blockOffset, blockSize, referenceFile, "Float32")

  trend2File = paste0(OUTPUT_DIR, '/', 'trend2-', blockOffset[1], '-', blockOffset[2], '.tif')
  saveImage(as.numeric(bfastResult$trend2), trend2File, blockOffset, blockSize, referenceFile, "Float32")

  endTime <- Sys.time()
  cat("Output writing time:\n")
  print((endTime - startTime))
}

pattern = '*.tif$'
blockOffset = c(COL_OFFSET, ROW_OFFSET)
blockSize = c(COL_SIZE, ROW_SIZE)
referenceFile = getReferenceFile(INPUT_DIR, pattern)

blockData = readBlockImages(INPUT_DIR, blockOffset, blockSize, pattern)
bfastResult = runBfast(blockData, N_CORES)

rm(blockData)
gc(verbose=FALSE)

saveBfastResult(bfastResult, referenceFile, blockOffset, blockSize)