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

anomalyTrend <- function(data = NA, refStart = 2005, refEnd = 2010, intStart = 2011, intEnd = 2017) {
  if (all(is.na(data)) == TRUE) {
    rep(NA, 6)
  } else {
    DT <- read.table("/data/DADOS_GRID/DATASAN/script/br_anomalytrend_2011_2017/timelineNdvi", sep = " ", h = TRUE)

    ndvi <- as.numeric(data)

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

    TIME = c(1:length(acumDiffer))
    LM = summary(lm(acumDiffer ~ TIME))
    LMResult <- as.numeric(c(
      LM$coefficients[1:2, 1],
      LM$coefficients[2, 4],
      LM$r.squared
    ))

    LMResult[5] <- LMResult[1] + (LMResult[2] * length(acumDiffer))
    LMResult[6] <- acumDiffer[length(acumDiffer)]
    LMResult <- round(LMResult, 5)
    return(LMResult)
  }
}

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
        for (bloco in args[1]) {
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
            anomalytrendResult <- as.data.frame(t(parApply(cl = clusterPool, blockData, 1, anomalyTrend)))
            names(anomalytrendResult) <- c('intercept', 'slope', 'pvalue', 'rsquared', 'modelDif', 'acumDif')
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

#Posso usar a lógica do extract, para pegar só os blocos que estão dentro do limite do brasil;
inputDir <- '/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig'
outputDir <- '/data/SENTINEL/DATASAN/br_anomalytrend_2011_2017/blocks_5row_21592col'
fileToExtent <- raster("/data/DADOS_GRID/pa_br_ndvi_maxmin_250_lapig/pa_br_ndvi_maxmin_250_2000049_lapig.tif")

##
# funcao de anomalias
# DT <- read.table("/data/DADOS_GRID/DATASAN/script/br_anomalytrend_2011_2017/timelineNdvi", sep = " ", h = TRUE)
##

#fileToExtent
pattern <- "*.tif"
nColBlock <- NULL
nRowBlock <- 5
ncores <- NULL
procRasterBlocks( inputDir, outputDir, fileToExtent, pattern, nColBlock = NULL, nRowBlock, ncores = NULL)
