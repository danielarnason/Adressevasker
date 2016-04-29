# coding: utf-8
#Dette script skal køres i Python 3
#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib.parse
import urllib.request
import json
import csv

service_url ='http://dawa.aws.dk/datavask/adresser?'

with open('/Users/danielarnason/Documents/adresser.csv', 'r') as csv_file:
	#Næste linie skal være tilstede, hvis der er headers i csv filen.
	#next(csv_file)
	for row in csv_file:
		url = service_url + urllib.parse.urlencode({'betegnelse' : row})
		url = url[:-3] # Fjerner det underlige newline character symbol %0A fra enden af hvert url
		# url_data = urllib.request.urlopen(url).read()
		# js_data = json.loads(url_data.decode('utf-8'))
		print(url)
