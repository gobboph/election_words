#!/usr/bin/env python

import requests
import numpy as np
from BeautifulSoup import BeautifulSoup
import csv



def WriteToCSV(number):

	endpoint = "http://en.wikipedia.org/wiki/" + str(number) + "th_United_States_Congress"

	response = requests.get(endpoint)

	#print response.content
	#print response.encoding

	f = open('file.txt','w')

	f.write(response.content)

	f.close()


	fr = open('file.txt','r')

	soup = BeautifulSoup(fr)

	dasoup = open('dasoup.txt','w')
	dasoup.write(soup.prettify())
	dasoup.close()

	all_states = ['Alabama_2', 'Alaska_2', 'Arizona_2', 'Arkansas_2', 'California_2', 'Colorado_2', 'Connecticut_2', 'Delaware_2', 'Florida_2', \
		'Georgia_2','Hawaii_2', 'Idaho_2', 'Illinois_2', 'Indiana_2', 'Iowa_2', 'Kansas_2', 'Kentucky_2', 'Lousiana_2', 'Maine_2', 'Maryland_2', \
		'Massachusetts_2', 'Michigan_2', 'Minnesota_2', 'Mississippi_2', 'Missouri_2', 'Montana_2', 'Nebraska_2', 'Nevada_2', 'New_Hampshire_2', \
		'New_Jersey_2', 'New_Mexico_2', 'New_York_2', 'North_Carolina_2', 'North_Dakota_2', 'Ohio_2', 'Oklahoma_2', 'Oregon_2', 'Pennsylvania_2', \
		'Rhode_Island_2', 'South_Carolina_2', 'South_Dakota_2', 'Tennessee_2', 'Texas_2', 'Utah_2', 'Vermont_2', 'Virginia_2', 'Washington_2', \
		'West_Virginia_2', 'Wisconsin_2', 'Wyoming_2']


	LIST = []

	for x in soup.findAll('h4'):
		for state in all_states:
			if x.span.get('id') == state:
				#print state
				if number <= 107:
					for y in x.nextSibling.nextSibling.findAll('li'):
						try:
							if y.a.string.isdigit() or y.a.string == 'At-large':
								if number == 105:
									#print y.a.nextSibling.nextSibling.string + ' ' + x.span.string
									LIST.append([y.a.nextSibling.nextSibling.string, x.span.string])
								else:
									#print y.a.nextSibling.nextSibling.string + ' ' + x.span.a.string
									LIST.append([y.a.nextSibling.nextSibling.string, x.span.a.string]) #y.a.nextSibling.nextSibling.nextSibling.replace('(','').replace(')','')
							else:
								if number == 105:
									#print y.a.string +' '+ x.span.string
									LIST.append([y.a.string, x.span.string])
								else:
									#print y.a.string +' '+ x.span.a.string
									LIST.append([y.a.string, x.span.a.string]) #y.a.nextSibling.replace('(','').replace(')','')
							pass
						except Exception:
							continue
				else:
					try:
						for y in x.nextSibling.nextSibling.nextSibling.nextSibling.findAll('li'):
							if y.a.string.isdigit() or y.a.string == 'At-large':
								if number == 105:
									#print y.a.nextSibling.nextSibling.string + ' ' + x.span.string
									LIST.append([y.a.nextSibling.nextSibling.string, x.span.string])
								else:
									#print y.a.nextSibling.nextSibling.string + ' ' + x.span.a.string
									LIST.append([y.a.nextSibling.nextSibling.string, x.span.a.string]) #y.a.nextSibling.nextSibling.nextSibling.replace('(','').replace(')','')
							else:
								if number == 105:
									#print y.a.string +' '+ x.span.string
									LIST.append([y.a.string, x.span.string])
								else:
									#print y.a.string +' '+ x.span.a.string
									LIST.append([y.a.string, x.span.a.string]) #y.a.nextSibling.replace('(','').replace(')','')
						pass
					except Exception:
						continue
							
					

	# print LIST

	with open("output"+str(number)+".csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(LIST)


	fr.close()

	print '\n'
	print 'Done with Congress number ' + str(number) + '\n'




for n in range(104,114):
	WriteToCSV(n)


