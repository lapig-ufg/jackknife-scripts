
################################################################################
################################################################################
#' Claudinei Oliveira dos Santos
#' Biologo | Mestre em Ecologia | Doutorando em Ciencias Ambientais
#' IPAM- Instituto de Pesquisa Amb. da Amazonia | Assistente de Pesquisa
#' LAPIG- Lab. de Processamento de Imagens e Geoprocessamento | Doutorando
#' claudineisantosnx@gmail.com | claudinei.santos@ipam.org.br
#' 
#' calcular media mensal de ndvi
################################################################################
################################################################################
#pacots, funcoes e configuracoes
options(scipen = 9999)
library(raster)
library(gtools)
library(dplyr)
library(lubridate)
args = commandArgs(trailingOnly = TRUE)
rasterOptions(tmpdir = '/data/SENTINEL/Rtemp')

####################################
####################################
# data das imagens
DT <- read.table("/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/timelineDT", sep = " ", h = TRUE)

# ndvi
INPUTDI <- '/data/DADOS02/RASTER/QUALIDADE_PASTAGEM/DADOS/RASTER/pa_br_ndvi_maxmin_250_lapig'
PATTERN <- '*.tif'
lsf <- Sys.glob(file.path(INPUTDI, PATTERN))

DT$DTymd <- ymd(DT$DTymd)
DT$DTym <- floor_date(DT$DTymd, 'month')
DT$YEAR <- as.numeric(substr(DT$DTyj, 1, 4))
DT$DOY <-  substr(DT$DTyj, 5, 7)

lsf_dt <- cbind(DT[1:length(lsf),], lsf)
# MONTH <- unique(month(lsf_dt$DTym))
lsf_dt <- lsf_dt[1:411,]

beginCluster(n = 20)  
for (i in 12:12) {
	ST <- Sys.time()
	print(paste0("processing Mes = ", i))

	lsfMes <- as.character(lsf_dt[month(lsf_dt$DTym) == i, 'lsf'])

	rbrick <- stack(sapply(lsfMes[1:length(lsfMes)-1], raster))
	print(rbrick)
	
	rbrickout <- clusterR(rbrick, calc, args=list(fun = mean, na.rm = TRUE))
	names(rbrickout) <- paste0("pa_br_ndvi_mean_", i)

	pathWrite <- paste0('/data/SENTINEL/media_mensal_ndvi/pa_br_ndvi_media_mes_2000_2017_250_lapig/pa_br_ndvi_media_mes_', i, '_250_lapig.tif')
	print(pathWrite)
	writeRaster(rbrickout, filename = pathWrite)

	print( Sys.time() - ST)
}
endCluster()

################################################################################
################################################################################