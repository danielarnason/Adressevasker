# coding: utf-8
#Dette script skal køres i Python 3
#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib.parse
import urllib.request
import json
import csv

service_url ='http://dawa.aws.dk/datavask/adresser?'

#Åbner csv filen, der indeholder de adresser, der skal vaskes
with open('/Users/danielarnason/Documents/adresser.csv', 'r') as csvFile:
	with open('/Users/danielarnason/Documents/csv_test.csv', 'w') as csvOutput:
		csvOutputWriter = csv.writer(csvOutput)
		csvFileReader = csv.reader(csvFile)

		#Fjerner headers fra csv filen og gemmer den i en variabel
		headers = next(csvFileReader)

		#tilføjer de nye kolonner til headers listen
		headers.extend(['vejnavnDawa', 'postnrDawa', 'kategoriDawa'])

		#skrive headers ind i den nye csv fil
		csvOutputWriter.writerow(headers)

		#Loop igennen alle adresser fra csv filen
		for row in csvFileReader:
			url = service_url + urllib.parse.urlencode({'betegnelse' : row[0]})
			urlData = urllib.request.urlopen(url).read()
			jsData = json.loads(urlData.decode('utf-8'))

			#Her finder man de forskellige ting i JSON objektet fra API'et og gemmer dem i variabler
			kategori = jsData['kategori']
			vejnavn = jsData['resultater'][0]['adresse']['vejnavn']
			postnr = jsData['resultater'][0]['adresse']['postnr']

			#Skriv hver række og værdierne fra det tilsvarende JSON objekt
			csvOutputWriter.writerow([row[0], vejnavn, postnr, kategori])
