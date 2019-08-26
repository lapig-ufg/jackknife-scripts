args <- commandArgs(trailingOnly = TRUE)

getReferenceRaster <- function(inputDir, pattern) {

  imageFiles = Sys.glob(file.path(inputDir, pattern))

  rasterFile <- raster(imageFiles[1])

  rasterFile
}

getBlocksOffset <- function(colOffset, rowOffset, nBlock, nColBlock = NULL, nRowBlock = NULL) {
    if(!is.null(nColBlock)){
        print("blocos por colunas")
        #blocks by col
        blocksOffset <- data.frame(iBlock = 1, colOffset, rowOffset)
        for(iBlock in 2:nBlock){
            blockOffset_i <- c(iBlock, (colOffset + ((iBlock-1) * nColBlock)), rowOffset)
            blocksOffset <-rbind(blocksOffset, blockOffset_i)
        }
        return(blocksOffset)
    } else if(!is.null(nRowBlock)){
        print("blocos por linhas")
        #blocks by col
        blocksOffset <- data.frame(iBlock = 1, colOffset, rowOffset)
        for(iBlock in 2:nBlock){
            blockOffset_i <- c(iBlock, colOffset, (rowOffset + ((iBlock-1) * nRowBlock)))
            blocksOffset <-rbind(blocksOffset, blockOffset_i)
        }
        return(blocksOffset)
    } else {
        print("O numero de linhas ou colunas por blocks nao informado")

    }
}

getOutputExtent <- function(referenceRaster, blockOffset, blockSize) {
    extentBlock <- extent(referenceRaster, blockOffset[2], c((blockOffset[2]-1) + blockSize[2]),
                          blockOffset[1], c((blockOffset[1]-1) + blockSize[1]))
    return(extentBlock)
}

readBlockImages = function(inputDir, outputExtent, pattern) {

  imageFiles <- mixedsort(Sys.glob(file.path(inputDir, pattern)))

  rasterBlock_img1 <- (crop(raster(imageFiles[1]), outputExtent))

  imageDataList <- data.frame(cellNumber = 1:ncell(rasterBlock_img1))
  imageDataList[,2:(length(imageFiles)+1)] <- NA
  names(imageDataList)[2:ncol(imageDataList)] <- paste0('band',1:(ncol(imageDataList)-1))

  imageDataList[,2:ncol(imageDataList)] <- lapply(imageFiles, function(x){crop(raster(x), outputExtent)[]})

  return(imageDataList[,-1]) #nao gravar cellNumber
}


# cumulative anomaly trend
cata <- function(data = NA,
                         refStart = 2005,
                         refEnd = 2009,
                         intStart = 2010,
                         intEnd = 2018) {
#    source("/data/SENTINEL/DATASAN/rpd_detect_cerrado/maxmin.R")
  data <- as.numeric(gsub(-Inf, NA, data))
  if (all(is.na(data)) == TRUE) {
    YrBfAfAAmp = rep(NA, 5)
  } else if (sum(is.na(data)) > 10){
    YrBfAfAAmp = rep(NA, 5)
  } else {
    DT <- read.table("/data/DADOS_GRID/DATASAN/rpd_detect_cerrado/timelineNdvi", sep = " ", h = TRUE)
    
    ndvi <- as.numeric(data])
    #ndvi <- forecast::na.interp(ndvi)
    #ndvi <- maxmin_filter(ndvi, nn = 3, grau = 2, desvio = 1)
    
    DT <- DT[1:length(ndvi),]
    
    pix <- as.data.frame(
                         cbind(DTyj = as.character(DT$DTyj),
                         DTymd = as.character(DT$DTymd),
                         ndvi)
                         )
    
    pix$ndvi <- as.numeric(as.character(pix$ndvi))
    pix$DTymd <- lubridate::ymd(pix$DTymd)
    
    pix$DTy <- as.numeric(substr(pix$DTyj, 1, 4))
    pix$DTj <-  as.numeric(substr(pix$DTyj, 5, 7))
  
    refData <- pix[dplyr::between(pix$DTy, refStart, refEnd),]
    intData <- pix[dplyr::between(pix$DTy, intStart, intEnd),]

    refMean <-  doBy::summaryBy(ndvi ~ DTj, data = refData, na.rm = TRUE)
    names(refMean)[2] <- 'refMean'    
    
    mIntData <-  doBy::orderBy( ~ DTyj,
                              data = merge(intData, refMean, by = 'DTj'))
  
    acumDiffer <- cumsum(mIntData$ndvi - mIntData$refMean)
    
    intData$acumDiffer <- acumDiffer
###
###
    intDataWet <- intData[lubridate::month(intData$DTymd) %in% c(1:3,10:12), ]
    intDataWet$season <- NA
    intDataWet$season <- sort(c(intDataWet[lubridate::month(intDataWet$DTymd) %in% c(10:12), ]$DTy, 
                                 intDataWet[lubridate::month(intDataWet$DTymd) %in% c(1:4), ]$DTy+1))

    intDataWetMean <- doBy::summaryBy(acumDiffer ~ season, data = intDataWet, FUN = median)
    names(intDataWetMean) <- c("DTy", "acumDiffer")
    intDataWetMean$DTy <- lubridate::ymd(paste0(intDataWetMean$DTy, '-02-01'))

    anoInter <- year(intDataWetMean[intDataWetMean$acumDiffer == min(intDataWetMean$acumDiffer),]$DTy)
    intDataBfInter <- intData[intData$DTy < anoInter,]
    intDataAfInter <- intData[intData$DTy >= anoInter,]

    ampBfInter <- max(intDataBfInter$acumDiffer) - min(intDataBfInter$acumDiffer)
    ampAfInter <- max(intDataAfInter$acumDiffer) - min(intDataAfInter$acumDiffer)

    if(nrow(intDataBfInter) > 3){
        LMBf <- as.numeric(
            lm(intDataBfInter$acumDiffer ~ intDataBfInter$DTymd)$coefficients
            )
    } else{
        LMBf <- c(0, 0)
    }
    
    if(nrow(intDataAfInter) > 3){
        LMAf <- as.numeric(
            lm(intDataAfInter$acumDiffer ~ intDataAfInter$DTymd)$coefficients
            )
    } else{
        LMAf <- c(0, 0)
    }
	YrBfAfAAmp <- c(anoInter, LMBf[2], LMAf[2], ampBfInter, ampAfInter)
  
  }
  return(YrBfAfAAmp)
}

###
###

saveImage <- function(outputData, outputfile, blockOffset, outputExtent, referenceRaster) {

  outputfile = paste0(outputfile, 'rowcolOffset_', blockOffset[2], '_', blockOffset[1], '.tif') ###

  outputRaster <- crop(referenceRaster, outputExtent)
  outputRaster[] <- outputData

  writeRaster(outputRaster, filename=outputfile, overwrite=TRUE)
}

procRasterBlocks <- function(inputDir, outputDir, fileToExtent, pattern, nColBlock = NULL, nRowBlock = NULL, ncores = NULL) {
        STTot <- Sys.time()

        ncores <- ifelse(is.null(ncores), detectCores(), ncores)
        #print(ncores)

        clusterPool <- makeCluster(ncores)
        clusterEvalQ(clusterPool, { 
        	require(doBy) 
        	require(dplyr)
            library(forecast)
            library(lubridate)
        	})

        #preparing blocks
        referenceRaster <- getReferenceRaster(inputDir, pattern)

        rowMin <- rowFromY(referenceRaster, ymax(fileToExtent))
        rowMax <- rowFromY(referenceRaster, ymin(fileToExtent))
        colMin <- colFromX(referenceRaster, xmin(fileToExtent))
        colMax <- colFromX(referenceRaster, xmax(fileToExtent))

        nRow <- rowMax - rowMin
        nCol <- colMax - colMin

        colOffset <- colMin
        rowOffset <- rowMin
        nRowBlock <- ifelse(is.null(nRowBlock), nRow, nRowBlock)
        nColBlock <- ifelse(is.null(nColBlock), nCol, nColBlock)

        nBlock <- ifelse(is.null(nRowBlock), 
        	ceiling(nCol / nColBlock), 
        	ceiling(nRow / nRowBlock) )
        print(paste0("Numero de blocos = ", nBlock))

        iBlockSize <- c(nColBlock, nRowBlock)
        # blocksOffset <- getBlocksOffset(colOffset, rowOffset, nBlock, nColBlock, nRowBlock = NULL)
        blocksOffset <- getBlocksOffset(colOffset, rowOffset, nBlock, nColBlock = NULL, nRowBlock)

        #process data by blocks
        for (bloco in args) {
            print(paste0("executing block = ", bloco))

            iBlockOffset <- as.numeric(blocksOffset[bloco, 2:3])
            print(iBlockOffset)

            STBloco <- Sys.time()
            outputExtent <- getOutputExtent(referenceRaster, iBlockOffset, iBlockSize)

            #read data of the block
            STRead <- Sys.time()
            blockData = readBlockImages(inputDir, outputExtent, pattern)
            totSTRead <- paste0("time to read block ", bloco, " = ", Sys.time() - STRead)
            print(totSTRead)

            #run function
            STRun <- Sys.time()
            anomalytrendResult <- as.data.frame(t(parApply(cl = clusterPool, blockData, 1, cata)))
            names(anomalytrendResult) <- c('ano_intervencao', 
                                           'slope_antes', 
                                           'slope_apos', 
                                           'amplitude_antes', 
                                           'amplitude_apos'
                                           )

            totSTRun <- paste0("time to run function = ", Sys.time() - STRun)
            print(totSTRun)

            #Write results
            for (i in 1:ncol(anomalytrendResult)) {
                outputfile <- paste0(outputDir, "/", names(anomalytrendResult)[i], '_block_', bloco, '_')
                outputData <- anomalytrendResult[, i]
                saveImage(outputData, outputfile, iBlockOffset, outputExtent, referenceRaster)
            }
            totSTBloco <- paste0("time to execute block = ", bloco, " = ", Sys.time() - STBloco)
			print(totSTBloco)
 
        	rm(anomalytrendResult, blockData)
        	gc(reset = TRUE)
        }
        print(paste0("time to execute all blocks = ", Sys.time() - STTot))
        stopCluster(clusterPool)
}

#Run
suppressWarnings(suppressMessages(library(raster)))
suppressWarnings(suppressMessages(library(doBy)))
suppressWarnings(suppressMessages(library(gtools)))
suppressWarnings(suppressMessages(library(dplyr)))
suppressWarnings(suppressMessages(library(parallel)))
suppressWarnings(suppressMessages(library(lubridate)))
suppressWarnings(suppressMessages(library(forecast)))

#brasil;
inputDir <- '/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig'
outputDir <- '/data/SENTINEL/DATASAN/rpd_detect_cerrado/result'
fileToExtent <- raster("/data/SENTINEL/DATASAN/bi_ce_slope_pasture_2017_v2.tif")

#fileToExtent
#args <- 1000
pattern <- "*.tif"
nColBlock <- NULL
nRowBlock <- 5 # 870
ncores <- NULL
procRasterBlocks( inputDir, outputDir, fileToExtent, pattern, nColBlock = NULL, nRowBlock, ncores = NULL)

##
##