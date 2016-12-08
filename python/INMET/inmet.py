import os
import csv
import sys
import string
import logging
import requests
import subprocess
import unicodedata

class classExec():
	def nameCaptchaUrl(self,html):
		splitList = html.split('</td>')
		posList = splitList[3]
		splitVar = posList.split('"')
		urlCaptcha = splitVar[1] 
		return urlCaptcha	
	
	def getCaptchaUrl(self,nameCaptchaUrl):
		gCaptch = os.path.join("http://www.inmet.gov.br/sonabra/",nameCaptchaUrl) 
		return gCaptch	
	
	def searchCaptcha(self,getCaptchaUrl):
		with open('Inmet.png',"wb") as fileSave:
			img = requests.get(getCaptchaUrl)
			for block in img.iter_content(1024):
				fileSave.write(block)				

	def funcTesseract(self):
		cmd = "tesseract Inmet.png stdout -psm 7 nobatch digits"				
		resultCaptcha = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		resulOutput = resultCaptcha.communicate()[0]
		output = resulOutput.replace('\n','')
		return output	
	
	def aleaValue(self,var):
		tagCaptcha = var.split('m=')
		captcha = tagCaptcha[1]
		captchaStr = str(captcha)
		return captchaStr	

	def funcLoop(self,url,code,codeImg,dateIni,dateEnd,arrayStations):
		keyPOST = {
			'aleaValue': code,
			'dtaini': dateIni,
			'dtafim': dateEnd,
			'aleaNum': codeImg,
		}
		urlAdress = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'
		urlAdressArray = url+arrayStations
		result = sess.post(urlAdressArray,keyPOST)
		varRandom = string.rfind(result.content,'<form action="dbRegSonabra.php" method="get" name="FRM" id="FRM">')
		return [varRandom,result]

	def saveHtml(self,result):
		with open("Inmet.html","wb") as fileSave:
			fileSave.write(result.content)
			fileSave.close()
			
	def saveCsv(self,csvData,arrayNameStations,dateIni,dateEnd):		
			with open(arrayNameStations+".csv","wb") as fileSave:
				csvData = string.replace(csvData,'vento_rajada,radiacao,precipitacao','')
				csvData = string.replace(csvData,'vento_vel,','vento_vel,vento_rajada,radiacao,precipitacao')
				csvData = string.replace(csvData,',',';')
				csvData = string.replace(csvData,'<br>','\n')
				fileSave.writelines('Data Inicial: '+dateIni+'\n')
				fileSave.writelines('Data Final: '+dateEnd+'\n'+'\n')
				fileSave.write(csvData)
				fileSave.close()

#Variavel que busca os metodos da classe:
varExec = classExec()

#Variaveis globais de parametros fixos:
url = "http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?"
arrayStations = ['Qzg5MQ==', 'QTEwOA==', 'QTE0MA==', 'QTEzOA==', 'QTEwMg==', 'QTEzNg==', 'QTEwNA==', 'QTM1Mw==', 'QTM1NQ==', 'QTMwMw==', 'QTMyNw==', 'QTMyMw==', 'QTM1Ng==', 'QTExMw==', 'QTEyMA==', 'QTEyOA==', 'QTExMA==', 'QTExNw==', 'QTEwOQ==', 'QTExMg==', 'QTEyMQ==', 'QTExMQ==', 'QTExOQ==', 'QTEwMQ==', 'QTEzMw==', 'QTEyMg==', 'QTEyMw==', 'QTEyNg==', 'QTEyNQ==', 'QTEzNA==', 'QTEyNA==', 'QTI0OQ==', 'QTI0Mg==', 'QTI0Mw==', 'QTQyMg==', 'QTQzNA==', 'QTQyOQ==', 'QTQwMg==', 'QTQ0Nw==', 'QTQxOA==', 'QTQzMw==', 'QTQzMg==', 'QTQwNQ==', 'QTQzMQ==', 'QTQxNg==', 'QTQwNg==', 'QTQ0OA==', 'QTQ0Mw==', 'QTQ0Mg==', 'QTQxMw==', 'QTQyNg==', 'QTQzOQ==', 'QTQxMA==', 'QTQ0NQ==', 'QTQyNA==', 'QTQwOA==', 'QTQ0Ng==', 'QTQwNw==', 'QTQ0MA==', 'QTQ1MA==', 'QTQyNQ==', 'QTQwNA==', 'QTQxMg==', 'QTQzOA==', 'QTQxMQ==', 'QTQzMA==', 'QTQyNw==', 'QTQzNg==', 'QTQyMw==', 'QTQwMQ==', 'QTQxNQ==', 'QTQyOA==', 'QTQ0MQ==', 'QTQzNQ==', 'QTQzNw==', 'QTQ0NA==', 'QTQxNA==', 'QTM2MA==', 'QTMxNQ==', 'QTM0Nw==', 'QTM0Mg==', 'QTMwNQ==', 'QTMxNA==', 'QTMxOQ==', 'QTM1OQ==', 'QTM1OA==', 'QTMzOQ==', 'QTMzMg==', 'QTMyNQ==', 'QTMwNg==', 'QTMyNA==', 'QTA0NQ==', 'QTAwMQ==', 'QTY1Nw==', 'QTYxNw==', 'QTYxNQ==', 'QTYxNA==', 'QTYyMw==', 'QTYyMg==', 'QTYxMw==', 'QTYxNg==', 'QTYxMg==', 'QTAyNA==', 'QTAxMw==', 'QTAyMw==', 'QTAzNA==', 'QTAzNg==', 'QTA0Ng==', 'QTAyMg==', 'QTAwMg==', 'QTAxNA==', 'QTAyOA==', 'QTAxNQ==', 'QTAzNQ==', 'QTAxNg==', 'QTAxMg==', 'QTAyNg==', 'QTAzMg==', 'QTAwMw==', 'QTAwNA==', 'QTAyNw==', 'QTAzMw==', 'QTAxNw==', 'QTAyNQ==', 'QTAxMQ==', 'QTAzNw==', 'QTIyMw==', 'QTIyMA==', 'QTIwNA==', 'QTIyMQ==', 'QTIzOA==', 'QTIwNQ==', 'QTIzNw==', 'QTIwNg==', 'QTIyMg==', 'QTIyNA==', 'QTIxOA==', 'QTIxNw==', 'QTIwNw==', 'QTIyNQ==', 'QTIwMw==', 'QTIxOQ==', 'QTU0OQ==', 'QTUzNA==', 'QTUwOA==', 'QTUwNQ==', 'QTUwMg==', 'RjUwMQ==', 'QTUyMQ==', 'QTU0NA==', 'QTUzMA==', 'QTUxOQ==', 'QTU0MQ==', 'QTU1NA==', 'QTU0OA==', 'QTUyMA==', 'QTU1Nw==', 'QTUzOA==', 'QTUzNw==', 'QTUzNg==', 'QTU0Mw==', 'QTUzNQ==', 'QTUyNA==', 'QTUzMg==', 'QTUzMw==', 'QTU0Ng==', 'QTU1NQ==', 'QTU1MA==', 'QTUxMg==', 'QTU1Mw==', 'QTUxOA==', 'QTU1Ng==', 'QTU0MA==', 'QTUzMQ==', 'QTUzOQ==', 'QTUyNg==', 'QTUwNg==', 'QTUwOQ==', 'QTUxNw==', 'QTUxMw==', 'QTUyOQ==', 'QTUxNg==', 'QTUyMw==', 'QTU0NQ==', 'QTU2MA==', 'QTU1MQ==', 'QTUyNQ==', 'QTU1Mg==', 'QTUxNA==', 'QTU0Nw==', 'QTU2MQ==', 'QTUyMg==', 'QTUyNw==', 'QTUxMQ==', 'QTUyOA==', 'QTUwNw==', 'QTU0Mg==', 'QTUxNQ==', 'QTUxMA==', 'QTc1Ng==', 'QTc1MA==', 'QTcxOQ==', 'QTc1OQ==', 'QTc1Nw==', 'QTcwMg==', 'QTc0Mg==', 'QTczMA==', 'QTcyNA==', 'QTc2MA==', 'QTcyMA==', 'QTcyMQ==', 'QTc1Mg==', 'QTcwOQ==', 'QTc1OA==', 'QTc0OQ==', 'QTczMQ==', 'QTcyMg==', 'QTcxNw==', 'QTcxMA==', 'QTcwMw==', 'QTcyMw==', 'QTc0Mw==', 'QTczMg==', 'QTc1MQ==', 'QTc1NA==', 'QTc2MQ==', 'QTcwNA==', 'QTkwOA==', 'QTkyNA==', 'QTkwOQ==', 'QTkzNA==', 'QTkxMA==', 'QTk0MQ==', 'QTkwNQ==', 'QTkxMg==', 'QTkyNg==', 'QTkxMw==', 'QTkxOA==', 'QTkxOQ==', 'QTkwMQ==', 'QTkzMA==', 'QTkwNg==', 'QTkzMg==', 'QTkzMw==', 'QTkxNA==', 'QTkyMA==', 'QTkyOA==', 'QTkyOQ==', 'QTkyNw==', 'QTkxNQ==', 'QTkzNw==', 'QTkzNQ==', 'QTkxNg==', 'QTkwNw==', 'QTkzNg==', 'QTkzMQ==', 'QTkyMQ==', 'QTkwMw==', 'QTkxNw==', 'QTkwNA==', 'QTkwMg==', 'QTkyMg==', 'QTIwMQ==', 'QTIyNg==', 'QTIzNg==', 'QTI0OA==', 'QTIwMg==', 'QTI0MQ==', 'QTIzMQ==', 'QTI0MA==', 'QTIwOQ==', 'QTI0Ng==', 'QTIzOQ==', 'QTIzNQ==', 'QTIzMg==', 'QTIxMA==', 'QTIxMg==', 'QTIxMQ==', 'QTIxNA==', 'QTIxNQ==', 'QTIzMw==', 'QTI1MA==', 'QTIzMA==', 'QTIyNw==', 'QTIxMw==', 'QTIyOQ==', 'QTMxMA==', 'QTM0OA==', 'QTM1Mg==', 'QTMxMw==', 'QTMyMA==', 'QTMzNA==', 'QTMyMQ==', 'QTMzMw==', 'QTMwOQ==', 'QTMyOQ==', 'QTM0MQ==', 'QTM1MQ==', 'QTMyMg==', 'QTM0OQ==', 'QTM2Ng==', 'QTM1Nw==', 'QTMwNw==', 'QTMwMQ==', 'QTM1MA==', 'QTMyOA==', 'QTMzNg==', 'QTMyNg==', 'QTM2NQ==', 'QTMzNw==', 'QTM2MQ==', 'QTMzOA==', 'QTMxMQ==', 'QTM2NA==', 'QTM1NA==', 'QTMwOA==', 'QTMzMA==', 'QTM0Mw==', 'QTMzNQ==', 'QTMzMQ==', 'QTM2Mg==', 'QTM0NQ==', 'QTMxMg==', 'QTM0Ng==', 'QTM2Mw==', 'QTgxOQ==', 'QTg2OQ==', 'QTg3Ng==', 'QTgwNw==', 'QTg0OQ==', 'QTg0Mw==', 'QTg0Ng==', 'QTg3NQ==', 'QTgyNQ==', 'QTgyNA==', 'QTg0Nw==', 'QTgyMw==', 'QTgxOA==', 'QTg3MQ==', 'QTgyMQ==', 'QTgyMA==', 'QTgzNQ==', 'QTg3Mw==', 'QTg0Mg==', 'QTgyMg==', 'QTg1MA==', 'QTg1NQ==', 'QTg3NA==', 'QTg3Mg==', 'QTYwNg==', 'QTYwNA==', 'QTYwNw==', 'QTYyMA==', 'QTYwMw==', 'QTYwOA==', 'QTYyNA==', 'QTYxOQ==', 'QTYxMA==', 'QTYwOQ==', 'QTY1Mg==', 'QTYwMg==', 'QTYyMQ==', 'QTY2Nw==', 'QTYwMQ==', 'QTY1OQ==', 'QTYxOA==', 'QTYxMQ==', 'QTM0MA==', 'QTMxNg==', 'QTM0NA==', 'QTMxNw==', 'QTMxOA==', 'QTMwNA==', 'QTM2Nw==', 'QTk0MA==', 'QTkzOQ==', 'QTkyNQ==', 'QTkzOA==', 'QTEzNQ==', 'QTgyNg==', 'QTgyNw==', 'QTg0MA==', 'QTgxMg==', 'QTgzOA==', 'QTg4NA==', 'QTg3OQ==', 'QTgxMQ==', 'QTg5OQ==', 'QTg1Mw==', 'QTg4MQ==', 'QTgyOA==', 'QTg1NA==', 'QTg4Mw==', 'QTgzNg==', 'QTg0NA==', 'QTg3OA==', 'QTg1Ng==', 'QTgzOQ==', 'QTgwMQ==', 'QTgzMQ==', 'QTgwMg==', 'QTgxMw==', 'QTgwMw==', 'QTgxMA==', 'QTgzMw==', 'QTgwNQ==', 'QTgzMA==', 'QTgzMg==', 'QTgyOQ==', 'QTg1Mg==', 'QTgzNw==', 'QTg4Mg==', 'QTgwOA==', 'QTgzNA==', 'QTgwOQ==', 'QTg4MA==', 'QTg2Nw==', 'QTg1OQ==', 'QTg2MA==', 'QTg0OA==', 'QTgwNg==', 'QTgxNw==', 'QTg2OA==', 'QTg1MQ==', 'QTg2Mw==', 'QTg0MQ==', 'QTg2NQ==', 'QTg2NA==', 'QTg0NQ==', 'QTgxNg==', 'QTg2MQ==', 'QTg2Mg==', 'QTg2Ng==', 'QTgxNQ==', 'QTg1Nw==', 'QTgxNA==', 'QTg1OA==', 'QTQwOQ==', 'QTQyMQ==', 'QTQyMA==', 'QTQxNw==', 'QTQxOQ==', 'QTczNg==', 'QTcyNQ==', 'QTc0MQ==', 'QTc0Ng==', 'QTc0OA==', 'QTc1NQ==', 'QTcwNQ==', 'QTcwNg==', 'QTczOA==', 'QTcwOA==', 'QTczNw==', 'QTcxMg==', 'QTcxNA==', 'QTczOQ==', 'QTc1Mw==', 'QTczMw==', 'QTczNQ==', 'QTcyNw==', 'QTc0NQ==', 'QTcxNg==', 'QTcyNg==', 'QTc0Nw==', 'QTcwNw==', 'QTcxOA==', 'QTcxMQ==', 'QTc0MA==', 'QTcxNQ==', 'QTcwMQ==', 'QTcxMw==', 'QTcyOA==', 'QTczNA==', 'QTcyOQ==', 'QTA1NA==', 'QTAyMQ==', 'QTA0NA==', 'QTA0Mw==', 'QTAzOA==', 'QTAzOQ==', 'QTAxOQ==', 'QTA0MQ==', 'QTA0MA==', 'QTAwOQ==', 'QTAxMA==', 'QTAyMA==', 'QTAxOA==', 'QTA1Mg==', 'VTU2MA==', 'VTU2NQ==']
arrayNameStations = ['AA - Projeto Criosfera', 'AC - Cruzeiro do Sul', 'AC - Epitaciolandia', 'AC - Feijo', 'AC - Parque Estadual Chandless', 'AC - Porto Walter', 'AC - Rio Branco', 'AL - Arapiraca', 'AL - Coruripe', 'AL - Maceio', 'AL - Palmeira dos Indios', 'AL - Pao de Acucar', 'AL - Sao Luis do Quitunde', 'AM - Apui', 'AM - Autazes', 'AM - Barcelos', 'AM - Boca do Acre', 'AM - Coari', 'AM - Eirunepe', 'AM - Humaita', 'AM - Itacoatiara', 'AM - Labrea', 'AM - Manacapuru', 'AM - Manaus', 'AM - Manicore', 'AM - Maues', 'AM - Parintins', 'AM - Presidente Figueiredo', 'AM - Rio Urubu', 'AM - Sao Gabriel da Cachoeira', 'AM - Urucara', 'AP - Macapa', 'AP - Oiapoque', 'AP - Tartarugalzinho', 'BA - Abrolhos', 'BA - Amargosa', 'BA - Barra', 'BA - Barreiras', 'BA - Belmonte', 'BA - Bom Jesus da Lapa', 'BA - Brumado', 'BA - Buritirama', 'BA - Caravelas', 'BA - Conde', 'BA - Correntina', 'BA - Cruz das Almas', 'BA - Curaca', 'BA - Delfino', 'BA - Euclides da Cunha', 'BA - Feira de Santana', 'BA - Guanambi', 'BA - Ibotirama', 'BA - Ilheus', 'BA - Ipiau', 'BA - Irece', 'BA - Itaberaba', 'BA - Itapetinga', 'BA - Itirucu', 'BA - Jacobina', 'BA - Jeremoabo', 'BA - Lencois', 'BA - Luis Eduardo Magalhaes', 'BA - Macajuba', 'BA - Marau', 'BA - Paulo Afonso', 'BA - Piata', 'BA - Porto Seguro', 'BA - Queimadas', 'BA - Remanso', 'BA - Salvador', 'BA - Santa Rita de Cassia', 'BA - Senhor do Bonfim', 'BA - Serrinha', 'BA - Uaua', 'BA - Una', 'BA - Valenca', 'BA - Vitoria da Conquista', 'CE - Acarau', 'CE - Barbalha', 'CE - Campos Sales', 'CE - Crateus', 'CE - Fortaleza', 'CE - Guaramiranga', 'CE - Iguatu', 'CE - Itapipoca', 'CE - Jaguaribe', 'CE - Jaguaruana', 'CE - Morada Nova', 'CE - Quixeramobim', 'CE - Sobral', 'CE - Taua', 'DF - Aguas Emendadas', 'DF - Brasilia', 'ES - Afonso Claudio', 'ES - Alegre', 'ES - Alfredo Chaves', 'ES - Linhares', 'ES - Nova Venecia', 'ES - Presidente Kenned', 'ES - Santa Teresa', 'ES - Sao Mateus', 'ES - Vitoria', 'GO - Alto Paraiso de Goias', 'GO - Aragarcas', 'GO - Caiaponia', 'GO - Catalao', 'GO - Cristalina', 'GO - Gama (Ponte Alta)', 'GO - Goianesia', 'GO - Goiania', 'GO - Goias', 'GO - Ipora', 'GO - Itapaci', 'GO - Itumbiara', 'GO - Jatai', 'GO - Luziania', 'GO - Mineiros', 'GO - Monte Alegre de Goias', 'GO - Morrinhos', 'GO - Niquelandia', 'GO - Parauna', 'GO - Pires do Rio', 'GO - Posse', 'GO - Rio Verde', 'GO - Sao Simao', 'GO - Silvania', 'MA - Alto Parnaiba', 'MA - Bacabal', 'MA - Balsas', 'MA - Barra do Corda', 'MA - Buriticupu', 'MA - Carolina', 'MA - Caxias', 'MA - Chapadinha', 'MA - Colinas', 'MA - Estreito', 'MA - Farol Preguicas', 'MA - Farol Santana', 'MA - Grajau', 'MA - Imperatriz', 'MA - Sao Luis', 'MA - Turiacu', 'MG - Aguas Vermelhas', 'MG - Aimores', 'MG - Almenara', 'MG - Araxa', 'MG - Barbacena', 'MG - Belo Horizonte - Cercadinho', 'MG - Belo Horizonte - Pampulha', 'MG - Buritis', 'MG - Caldas', 'MG - Campina Verde', 'MG - Capelinha', 'MG - Caratinga', 'MG - Chapada Gaucha', 'MG - Conceicao das Alagoas', 'MG - Coronel Pacheco', 'MG - Curvelo', 'MG - Diamantina', 'MG - Dores do Indaia', 'MG - Espinosa', 'MG - Florestal', 'MG - Formiga', 'MG - Governador Valadares', 'MG - Guanhaes', 'MG - Guarda-Mor', 'MG - Ibirite (Rola Moca', 'MG - Itaobim', 'MG - Ituitaba', 'MG - Joao Pinheiro', 'MG - Juiz de Fora', 'MG - Manhuacu', 'MG - Mantena', 'MG - Maria da Fe', 'MG - Mocambinho', 'MG - Montalvania', 'MG - Montes Claros', 'MG - Monte Verde', 'MG - Muriae', 'MG - Ouro Branco', 'MG - Passa Quatro', 'MG - Passos', 'MG - Patrocionio', 'MG - Pirapora', 'MG - Pompeu', 'MG - Rio Pardo de Minas', 'MG - Sacramento', 'MG - Salinas', 'MG - Sao Joao Del-Rei', 'MG - Sao Romao', 'MG - Sao Sebastiao do Paraiso', 'MG - Serra dos Aimores', 'MG - Teofilo Otoni', 'MG - Timoteo', 'MG - Tres Marias', 'MG - Uberlandia', 'MG - Unai', 'MG - Varginha', 'MG - Vicosa', 'MS - Agua Clara', 'MS - Amambai', 'MS - Aquidauana', 'MS - Bataguassu', 'MS - Bela Vista', 'MS - Campo Grande', 'MS - Cassilandia', 'MS - Chapadao do Sul', 'MS - Corumba', 'MS - Costa Rica', 'MS - Coxim', 'MS - Dourados', 'MS - Itaquirai', 'MS - Ivinhema', 'MS - Jardim', 'MS - Juti', 'MS - Maracaju', 'MS - Miranda', 'MS - Nhumirim', 'MS - Paranaiba', 'MS - Ponta Pora', 'MS - Porto Murtinho', 'MS - Rio Brilhante', 'MS - Sao Gabriel do Oeste', 'MS - Sete Quedas', 'MS - Sidrolandia', 'MS - Sonora', 'MS - Tres Lagoas', 'MT - Agua Boa', 'MT - Alta Floresta', 'MT - Alto Araguaia', 'MT - Alto Taquari', 'MT - Apiacas', 'MT - Caceres', 'MT - Campo Novo dos Parecis', 'MT - Campo Verde', 'MT - Carlinda', 'MT - Comodoro', 'MT - Confresa', 'MT - Cotriguacu', 'MT - Cuiaba', 'MT - Gaucha do Norte', 'MT - Guaranta do Norte', 'MT - Guiratinga', 'MT - Itiquira', 'MT - Juara', 'MT - Juina', 'MT - Nova Maringa', 'MT - Nova Ubirata', 'MT - Novo Mundo', 'MT - Paranatinga', 'MT - Pontes de Lacerda', 'MT - Porto Estrela', 'MT - Querencia', 'MT - Rondonopolis', 'MT - Salto do Ceu', 'MT - Santo Antonio do Leste', 'MT - Sao Felix do Araguaia', 'MT - Sao Jose do Rio Claro', 'MT - Sinop', 'MT - Sorriso', 'MT - Tangara da Serra', 'MT - Vila Bela da Santissima Trindade', 'PA - Belem', 'PA - Braganca', 'PA - Cameta', 'PA - Capitao Poco', 'PA - Castanhal', 'PA - Conceicao do Araguaia', 'PA - Itaituba', 'PA - Maraba', 'PA - Medicilandia', 'PA - Mina Palito', 'PA - Monte Alegre', 'PA - Novo Repartimento', 'PA - Obidos', 'PA - Pacajas', 'PA - Paragominas', 'PA - Placas', 'PA - Rondon do Para', 'PA - Salinopolis', 'PA - Santana do Araguaia', 'PA - Santarem', 'PA - Serra dos Carajas', 'PA - Soure', 'PA - Tome Acu', 'PA - Tucurui', 'PB - Areia', 'PB - Cabaceiras', 'PB - Camaratuba', 'PB - Campina Grande', 'PB - Joao Pessoa', 'PB - Monteiro', 'PB - Patos', 'PB - Sao Goncalo', 'PE - Arco Verde', 'PE - Cabrobo', 'PE - Caruaru', 'PE - Floresta', 'PE - Garanhuns', 'PE - Ibimirim', 'PE - Ouricuri', 'PE - Palmares', 'PE - Petrolina', 'PE - Recife', 'PE - Serra Talhada', 'PE - Surubim', 'PI - Alvorada do Gurgeia', 'PI - Bom Jesus do Piau', 'PI - Canto do Buriti', 'PI - Caracol', 'PI - Castelo do Piaui', 'PI - Esperantina', 'PI - Floriano', 'PI - Gilbues', 'PI - Oeiras', 'PI - Parnaiba', 'PI - Paulistana', 'PI - Picos', 'PI - Piripiri', 'PI - Sao Joao do Piaui', 'PI - Sao Pedro do Piaui', 'PI - Sao Raimundo Nonato', 'PI - Teresina', 'PI - Urucui', 'PI - Valenca do Piaui', 'PR - Castro', 'PR - Cidade Gaucha', 'PR - Clevelandia', 'PR - Curitiba', 'PR - Diamante do Norte', 'PR - Dois Vizinhos', 'PR - Foz do Iguacu', 'PR - General Carneiro', 'PR - Goioere', 'PR - Icaraima', 'PR - Ilha do Mel', 'PR - Inacio Martins', 'PR - Ivai', 'PR - Japira', 'PR - Joaquim Tavora', 'PR - Marechal Candido Rondon', 'PR - Maringa', 'PR - Morretes', 'PR - Nova Fatima', 'PR - Nova Tebas', 'PR - Paranapoema', 'PR - Planalto', 'PR - Sao Mateus do Sul', 'PR - Ventania', 'RJ - Arraial do Cabo', 'RJ - Cambuci', 'RJ - Campos', 'RJ - Campos - Sao Tome', 'RJ - Duque de Caxias - Xerem', 'RJ - Macae', 'RJ - Nova Friburgo-Salinas', 'RJ - Parati', 'RJ - Petropolis - Pico do Couto', 'RJ - Resende', 'RJ - Rio de Janeiro-Forte de Copacabana', 'RJ - Rio de Janeiro - Marambaia', 'RJ - Rio de Janeiro - Vila Militar', 'RJ - Saquarema-Sampaio Correia', 'RJ - Seropedica-Ecologia Agricola', 'RJ - Silva Jardim', 'RJ - Teresopolis - Parque Nacional', 'RJ - Valenca', 'RN - Apodi', 'RN - Caico', 'RN - Calcanhar', 'RN - Macau', 'RN - Mossoro', 'RN - Natal', 'RN - Santa Cruz', 'RO - Ariquemes', 'RO - Cacoal', 'RO - Porto Velho', 'RO - Vilhena', 'RR - Boa Vista', 'RS - Alegrete', 'RS - Bage', 'RS - Bento Goncalves', 'RS - Cacapava do Sul', 'RS - Camaqua', 'RS - Campo Bom', 'RS - Canela', 'RS - Cangucu', 'RS - Chui', 'RS - Cruz Alta', 'RS - Dom Pedrito', 'RS - Erechim', 'RS - Frederico Westphalen', 'RS - Ibiruba', 'RS - Jaguarao', 'RS - Lagoa Vemelha', 'RS - Mostardas', 'RS - Palmeira das Missoes', 'RS - Passo Fundo', 'RS - Porto Alegre', 'RS - Quarai', 'RS - Rio Grande', 'RS - Rio Pardo', 'RS - Santa Maria', 'RS - Santa Rosa', 'RS - Santiago', 'RS - Santo Augusto', 'RS - Sao Borja', 'RS - Sao Gabriel', 'RS - Sao Jose dos Ausentes', 'RS - Sao Luiz Gonzaga', 'RS - Soledade', 'RS - Teutonia', 'RS - Torres', 'RS - Tramandai', 'RS - Uruguaiana', 'RS - Vacaria', 'SC - Ararangua', 'SC - Cacador', 'SC - Curitibanos', 'SC - Dionisio Cerqueira', 'SC - Florianopolis-Sao Jose', 'SC - Indaial', 'SC - Itajai', 'SC - Itapoa', 'SC - Ituporanga', 'SC - Joacaba', 'SC - Lages', 'SC - Major Vieira', 'SC - Morro da Igreja (Bom Jardim da Serra)', 'SC - Novo Horizonte', 'SC - Rio do Campo', 'SC - Rio Negrinho', 'SC - Santa Marta', 'SC - Sao Joaquim', 'SC - Sao Miguel do Oeste', 'SC - Urussanga', 'SC - Xanxere', 'SE - Aracaju', 'SE - Brejo Grande', 'SE - Carira', 'SE - Itabaianinha', 'SE - Poco Verde', 'SP - Ariranha', 'SP - Avare', 'SP - Barra Bonita', 'SP - Barra do Turvo', 'SP - Barretos', 'SP - Barueri', 'SP - Bauru', 'SP - Campos do Jordao', 'SP - Casa Branca', 'SP - Franca', 'SP - Ibitinga', 'SP - Iguape', 'SP - Itapeva', 'SP - Itapira', 'SP - Ituverava', 'SP - Jales', 'SP - Jose Bonifacio', 'SP - Lins', 'SP - Moela', 'SP - Ourinhos', 'SP - Piracicaba', 'SP - Pradopolis', 'SP - Presidente Prudente', 'SP - Rancharia', 'SP - Sao Carlos', 'SP - Sao Luis do Paraitinga', 'SP - Sao Miguel Arcanjo', 'SP - Sao Paulo-Mirante de Santana', 'SP - Sorocaba', 'SP - Taubate', 'SP - Valparaiso', 'SP - Votuporanga', 'TO - Araguacu', 'TO - Araguaina', 'TO - Araguatins', 'TO - Campos Lindos', 'TO - Dianopolis', 'TO - Formoso do Araguaia', 'TO - Gurupi', 'TO - Marianopolis do Tocantins', 'TO - Mateiros', 'TO - Palmas', 'TO - Parana', 'TO - Pedro Afonso', 'TO - Peixe', 'TO - Santa Rosa do Tocantins', 'UY - Colonia', 'UY - Rocha']
sess = requests.Session()

#Variaveis globais de parametros nao fixos:
dateIni = sys.argv[1]
dateEnd = sys.argv[2]

#Criador de nova pasta
folder = str(dateIni).replace("/","_")+'________'+str(dateEnd).replace("/","_")
if not os.path.exists(folder):
	os.makedirs(folder)

for i in xrange(len(arrayStations)):
	
	html = sess.get(url+arrayStations[i]).text	
	a = varExec.getCaptchaUrl(varExec.nameCaptchaUrl(html))
	varExec.searchCaptcha(a)
	codeCaptcha = varExec.aleaValue(varExec.nameCaptchaUrl(html))
	cdoImg = varExec.funcTesseract()
	response = varExec.funcLoop(url,codeCaptcha,cdoImg,dateIni,dateEnd,arrayStations[i])		

	while (response[0] == -1):
		
		logging.warning(' Re-executando estacao: %s \n',arrayNameStations[i])		
		html = sess.get(url+arrayStations[i]).text	
		a = varExec.getCaptchaUrl(varExec.nameCaptchaUrl(html))
		varExec.searchCaptcha(a)
		codeCaptcha = varExec.aleaValue(varExec.nameCaptchaUrl(html))
		cdoImg = varExec.funcTesseract()
		response = varExec.funcLoop(url,codeCaptcha,cdoImg,dateIni,dateEnd,arrayStations[i])
	
	csvData = sess.get('http://www.inmet.gov.br/sonabra/pg_downDadosCodigo.php').text
	removUnicode = unicodedata.normalize('NFKD',csvData).encode('ASCII','ignore').decode('utf-8')		

	varExec.saveHtml(response[1])
	varExec.saveCsv(removUnicode,os.path.join(folder,arrayNameStations[i]),dateIni,dateEnd)
	logging.warning('\nEstacao %s concluido!\n',arrayNameStations[i])