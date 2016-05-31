# coding: utf-8
#Dette script skal køres i Python 3
#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib.parse
import urllib.request
import json
import csv

service_url ='http://dawa.aws.dk/datavask/adresser?'
inputFilePath = 'C:/Users/jjo4da/Desktop/Python/adresser3.csv'
outputFilePath = 'C:/Users/jjo4da/Desktop/Python/csv_test.csv'

print('Gået i gang!')

#Åbner csv filen, der indeholder de adresser, der skal vaskes
with open(inputFilePath, 'r') as csvFile:
	with open(outputFilePath, 'w') as csvOutput:
		csvOutputWriter = csv.writer(csvOutput, lineterminator='\n')
		csvFileReader = csv.reader(csvFile, delimiter=';')

		#Fjerner headers fra csv filen og gemmer den i en variabel
		headers = next(csvFileReader)

		#tilføjer de nye kolonner til headers listen
		headers.extend(['vejnavnDawa', 'husnrDawa', 'postnrDawa', 'postnrnavnDawa', 'kategoriDawa', 'lat', 'lon'])

		#skrive headers ind i den nye csv fil
		csvOutputWriter.writerow(headers)

		#Loop igennen alle adresser fra csv filen
		for row in csvFileReader:
			url = service_url + urllib.parse.urlencode({'betegnelse' : row[2] + ' ' + row[3] + ' ' + row[4]})
			urlData = urllib.request.urlopen(url).read()
			jsData = json.loads(urlData.decode('utf-8'))

			#Her finder man de forskellige ting i JSON objektet fra API'et og gemmer dem i variabler
			kategori = jsData['kategori']
			vejnavn = jsData['resultater'][0]['adresse']['vejnavn']
			husnr = jsData['resultater'][0]['adresse']['husnr']
			postnr = jsData['resultater'][0]['adresse']['postnr']
			postnrnavn = jsData['resultater'][0]['adresse']['postnrnavn']
			status = jsData['resultater'][0]['aktueladresse']['status']
			#Her finder den koordinaterne for den fundne adresse
			if status == 2 or status == 4:
				csvOutputWriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], vejnavn, husnr, postnr, postnrnavn, kategori])
			else:
				hrefUrl = jsData['resultater'][0]['aktueladresse']['href'] + '?srid=25832'
				hrefUrlData = urllib.request.urlopen(hrefUrl).read()
				hrefJsonData = json.loads(hrefUrlData.decode('utf-8'))

				latitude = hrefJsonData['adgangsadresse']['adgangspunkt']['koordinater'][0]
				longitude = hrefJsonData['adgangsadresse']['adgangspunkt']['koordinater'][1]

				#Skriv hver række og værdierne fra det tilsvarende JSON objekt
				csvOutputWriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], vejnavn, husnr, postnr, postnrnavn, kategori, latitude, longitude])
print('Done!')
