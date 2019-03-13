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

maxminFilter <- function(SERIE, nn = 3, grau = 2, desvio = 1) {
  ###   
  if (all(is.na(SERIE)) == TRUE) {
    rep(NA, length(SERIE))
  ###  
  } else if(sum(is.na(SERIE)) > 8 ){
    rep(NA, length(SERIE))
  ###  
  } else {
    ######
    polyFilter <- function(ts, nn, grau, desvio = 0) {
      ##
      ns = length(ts)
      new_ts = ts
      idx = -nn:nn
      ##
      X = matrix(rep(0, length(idx) * (grau + 1)), ncol = grau + 1, byrow = FALSE)
      X[, 1] = 1
      for (k in 2:(grau + 1)) {
        X[, k] = (idx) ^ k
      }
      ###
      for (i in 1:ns) {
        idx_ts = (abs(idx + i - 1) %% ns + 1)
        y = ts[idx_ts]
        LM = lm.fit(x = X, y = y)
        ###
        if (desvio == 0) {
          new_ts[i] = LM$coefficients[1]
        ###  
        } else {
          sdv = sd(LM$residuals)
          ###
          if (abs(ts[i] - LM$coefficients[1]) > desvio * sdv) {
            new_ts[i] = LM$coefficients[1]
          }
        }
      }
      ##
      return(new_ts) 
    }
    ######
    maxminOutliers <- function(ts, nn) {
      ns = length(ts)
      lmax = c()
      lmin = c()
      ###
      for (i in 1:ns) {
        to = max(1, (i - nn))
        tf = min(ns, (i + nn))
        M = max(ts[to:tf])
        ###
        if (ts[i] == M) {
          lmax = c(lmax, i)
        ###  
        } else {
          m = min(ts[to:tf])
          ###
          if (ts[i] == m) {
            lmin = c(lmin, i)
          }
        }
      }
      ###
      return(list(
        max = lmax,
        min = unlist(lmin),
        ID = c(lmax, lmin)
      ))
    }
    ######
    interpNaTS <- forecast::na.interp(SERIE)
    #
    OUTLIERS <- maxminOutliers(ts = interpNaTS, nn)$ID
    #
    ADJUSTED <-polyFilter(ts = interpNaTS, nn = nn, grau = grau, desvio = desvio)
    #
    FILTER <- interpNaTS
    FILTER[OUTLIERS] <- ADJUSTED[OUTLIERS]
    ###
    return(as.numeric(FILTER))
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
            anomalytrendResult <- as.data.frame(t(parApply(cl = clusterPool, blockData, 1, maxminFilter)))
            names(anomalytrendResult) <- paste0("ndvi_", 1:ncol(anomalytrendResult))
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
        totSTTot <- print(paste0("time to execute all blocks = ", Sys.time() - STTot))
        stopCluster(clusterPool)
}

#Run
suppressWarnings(suppressMessages(library(raster)))
#suppressWarnings(suppressMessages(library(doBy)))
suppressWarnings(suppressMessages(library(gtools)))
#suppressWarnings(suppressMessages(library(dplyr)))
suppressWarnings(suppressMessages(library(parallel)))
suppressWarnings(suppressMessages(library(forecast)))

#Posso usar a lógica do extract, para pegar só os blocos que estão dentro do limite do brasil;
inputDir <- '/data/SENTINEL/pa_br_ndvi_250_lapig'
outputDir <- '/data/SENTINEL/pa_br_ndvi_maxmin_250_lapig'
fileToExtent <- raster("/data/SENTINEL/pa_br_ndvi_250_lapig/pa_br_ndvi_250_2017337_lapig.tif")
#fileToExtent
pattern <- "*.tif"
nColBlock <- NULL
nRowBlock <- 80
ncores <- NULL
procRasterBlocks( inputDir, outputDir, fileToExtent, pattern, nColBlock = NULL, nRowBlock, ncores = NULL)
