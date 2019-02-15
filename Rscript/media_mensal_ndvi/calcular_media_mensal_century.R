

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

# ndvi
INPUTDI <- 'Y:\\CENTURYCERRADO/mosaics_wk'
PATTERN <- '*.tif'
lsf <- Sys.glob(file.path(INPUTDI, PATTERN))

variaveis <- c("bgliv", "agliv", "stdead", "somsc")
mes <- c("01-01.tif", "02-01.tif", "03-01.tif", "04-01.tif",
		 "05-01.tif", "06-01.tif", "07-01.tif", "08-01.tif",
		 "09-01.tif", "10-01.tif", "11-01.tif", "12-01.tif")

beginCluster(n = 5)  
for(i in 1:length(variaveis)){
	print(variaveis[i])
	lsfVar <- grep(variaveis[i], lsf, value = TRUE)[1:216]

	for(j in 1:12){
		ST <- Sys.time()
		print(paste0("processing Mes = ", j))

		lsfMes <- grep(mes[j], lsfVar, value = TRUE)
        print(length(lsfMes))

		rbrick <- stack(sapply(lsfMes, raster))
		print(rbrick)
	
		rbrickout <- clusterR(rbrick, calc, args=list(fun = mean, na.rm = TRUE))
		names(rbrickout) <- paste0("bi_ce_aglivc_mean_", j)

		pathWrite <- paste0('W:\\media_mensal_century/bi_ce_', 
							variaveis[i], 
							'_media_mes_',
							 j, 
							 '_1km_lapig.tif')
		print(pathWrite)
		writeRaster(rbrickout, filename = pathWrite)

		print( Sys.time() - ST)
	}
}
endCluster()

################################################################################
################################################################################