# coding: utf-8

#Dette script er en test af datavask tjenesten fra dawa.aws.dk. Skriv en adresse og få returneret den rigtige adresse, vejkode og koordinater
import urllib
import json

service_url ='http://dawa.aws.dk/datavask/adresser?'

while True:
	adr = raw_input('Skriv en adresse - ')	
	if len(adr) < 1:
		print 'Du skal skrive noget'

	url = service_url + urllib.urlencode({'betegnelse' : adr})
	url_data = urllib.urlopen(url).read()

	js_data = json.loads(url_data)

	#data fra adresseid link
	adr_url = js_data['resultater'][0]['aktueladresse']['href']
	adr_url_data = urllib.urlopen(adr_url).read()
	adresse_js = json.loads(adr_url_data)

	#nøjagtighed
	kategori = js_data['kategori']


	#print statements
	if kategori == 'B':
		print 'Kategori B: Sikkert match'
	elif kategori == 'C':
		print 'Kategori C: Usikkert match'
	else:
		print 'Kategori A: Præcist match'
	#print 'Kategori: ', js_data['kategori']
	#print 'Vejnavn: ', js_data['resultater'][0]['aktueladresse']['vejnavn']
	#print 'Husnr: ', js_data['resultater'][0]['aktueladresse']['husnr']
	#print 'Postnr: ', js_data['resultater'][0]['aktueladresse']['postnr']
	print 'Rigtig adresse: ', adresse_js['adressebetegnelse']
	print 'Vejkode: ', adresse_js['adgangsadresse']['vejstykke']['kode']
	print 'Koordinater: ', adresse_js['adgangsadresse']['adgangspunkt']['koordinater'][0], adresse_js['adgangsadresse']['adgangspunkt']['koordinater'][1]

	#print json.dumps(js_data, indent=4)
	


