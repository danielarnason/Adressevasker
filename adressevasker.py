# coding: utf-8
#Dette script skal køres i Python 3
#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib.parse
import urllib.request
import json
import csv

service_url ='http://dawa.aws.dk/datavask/adresser?'

with open('/Users/danielarnason/Documents/adresse.csv', 'r') as csv_file:
	for row in csv_file:
		url = service_url + urllib.parse.urlencode({'betegnelse' : row})
		url_data = urllib.request.urlopen(url).read()
		js_data = json.dumps(url_data)
	print(js_data)

	# for row in reader:
	# 	print row.encode('utf-8')

	#
	# url = service_url + urllib.urlencode({'betegnelse' : adr})
	# url_data = urllib.urlopen(url).read()
	#
	# js_data = json.loads(url_data)
	# print js_data
