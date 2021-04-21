# coding: utf-8
#Dette script skal køres i Python 3
#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib.parse
import urllib.request
import json
import csv

service_url ='http://dawa.aws.dk/datavask/adresser?'
inputFilePath = 'W:/qgis/Produktion/GIS/Daniel/_kollegaer/Uffe_CEI/kommunale_bygninger_v3.csv' #Indtast stien til din egen csv fil
outputFilePath = 'W:/qgis/Produktion/GIS/Daniel/_kollegaer/Uffe_CEI/csv_test.csv' #Indtast sti til din output csv fil. Hvis den ikke eksistere, bliver der lavet en ny.

print('Gået i gang!')

#Åbner csv filen, der indeholder de adresser, der skal vaskes
with open(inputFilePath, 'r') as csvFile:
	with open(outputFilePath, 'w') as csvOutput:
		csvOutputWriter = csv.writer(csvOutput, lineterminator='\n')
		csvFileReader = csv.reader(csvFile, delimiter=';') #Her skal man være opmærksom på, hvilken delimiter filen bruger. De mest almindelige er et komma eller en semikolon

		#Fjerner headers fra csv filen og gemmer den i en variabel
		headers = next(csvFileReader)

		#tilføjer de nye kolonner til headers listen
		headers.extend(['vejnavnDawa', 'husnrDawa', 'postnrDawa', 'postnrnavnDawa', 'kategoriDawa', 'lat', 'lon'])

		#skrive headers ind i den nye csv fil
		csvOutputWriter.writerow(headers)

		#Loop igennen alle adresser fra csv filen
		for row in csvFileReader:
			try:
				url = service_url + urllib.parse.urlencode({'betegnelse' : row[3] + ' ' + row[4] + ' ' + row[5] + ' ' + row[6]}) #Her skal adressekolonnen specificeres. Hvis vejnavn, husnr og postnr står i flere kolonner, så skal de tilføjes
				urlData = urllib.request.urlopen(url).read()
				jsData = json.loads(urlData.decode('utf-8'))

				#Her finder man de forskellige ting i JSON objektet fra API'et og gemmer dem i variabler
				kategori = jsData['kategori']
				vejnavn = jsData['resultater'][0]['adresse']['vejnavn']
				husnr = jsData['resultater'][0]['adresse']['husnr']
				postnr = jsData['resultater'][0]['adresse']['postnr']
				postnrnavn = jsData['resultater'][0]['adresse']['postnrnavn']
				status = jsData['resultater'][0]['aktueladresse']['status']
				kommentar = 'Behandlet'

				#Her finder den koordinaterne for den fundne adresse
				if status == 2 or status == 4:
					newcol = [vejnavn,husnr, postnr, postnrnavn, kategori]
					row.extend(newcol)
					csvOutputWriter.writerow(row)
				else:
					hrefUrl = jsData['resultater'][0]['aktueladresse']['href'] + '?srid=25832'
					hrefUrlData = urllib.request.urlopen(hrefUrl).read()
					hrefJsonData = json.loads(hrefUrlData.decode('utf-8'))

					utm_x = hrefJsonData['adgangsadresse']['adgangspunkt']['koordinater'][0]
					utm_y = hrefJsonData['adgangsadresse']['adgangspunkt']['koordinater'][1]

					newcol = [vejnavn,husnr, postnr, postnrnavn, kategori, utm_x, utm_y, kommentar]
					row.extend(newcol)

					#Skriv hver række og værdierne fra det tilsvarende JSON objekt
					csvOutputWriter.writerow(row)
			except KeyError as e:
				kommentar = 'Fejlet - KeyError "%s"' % str(e) + 'Adressen kunne ikke findes i DAWA'
				newcol = ['','', '', '', '', '', '', kommentar]
				row.extend(newcol)
				csvOutputWriter.writerow(row)
print('Done!')
