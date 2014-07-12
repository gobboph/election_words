#!/usr/bin/env python
	
import requests
import numpy as np
from BeautifulSoup import BeautifulSoup
import csv
#import urllib.request
import json



'''Read from csv file and copy into dictionaries for all congresses'''

with open('output104.csv', 'rb') as f04, open('output105.csv', 'rb') as f05, open('output106.csv', 'rb') as f06, \
	open('output107.csv', 'rb') as f07, open('output108.csv', 'rb') as f08, open('output109.csv', 'rb') as f09, \
	open('output110.csv', 'rb') as f10, open('output111.csv', 'rb') as f11, open('output112.csv', 'rb') as f12, \
	open('output113.csv', 'rb') as f13:
	content04, content05, content06, content07, content08, content09, content10, content11, content12, content13 = \
	[csv.reader(f) for f in [f04, f05, f06, f07, f08, f09, f10, f11, f12, f13]]

	names04 = {row[0]: [row[1]] for row in content04}
	names05 = {row[0]: [row[1]] for row in content05}
	names06 = {row[0]: [row[1]] for row in content06}
	names07 = {row[0]: [row[1]] for row in content07}
	names08 = {row[0]: [row[1]] for row in content08}
	names09 = {row[0]: [row[1]] for row in content09}
	names10 = {row[0]: [row[1]] for row in content10}
	names11 = {row[0]: [row[1]] for row in content11}
	names12 = {row[0]: [row[1]] for row in content12}
	names13 = {row[0]: [row[1]] for row in content13}



'''Combine all the names in a new dictionary that counts how many years they spent in congress'''

all_of_them = [names04,names05,names06,names07,names08,names09,names10,names11,names12,names13]

name_count = names04

for key in name_count:
	name_count[key].append(0)

for x in all_of_them:
	for name in x:
		if name in name_count:
			name_count[name][1] += 1
		else:
			name_count[name] = x[name]
			name_count[name].append(1)



'''Initialize a dictionary of dictionaries. The keys of the sub-dictionaries are the states and the values are lists with names and \
	times in congress. I also initialize another dictionary of dictionaries where I will append their bioguide_id'''


all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', \
		'Georgia','Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Lousiana', 'Maine', 'Maryland', \
		'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New_Hampshire', \
		'New_Jersey', 'New_Mexico', 'New_York', 'North_Carolina', 'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', \
		'Rhode_Island', 'South_Carolina', 'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', \
		'West_Virginia', 'Wisconsin', 'Wyoming']

# Momentarily commenitng out to experiment

# all_dict = {x: {} for x in all_states}

# all_dict_new = {x: {} for x in all_states}

# for x in all_states:
# 	for key in name_count:
# 		if name_count[key][0] == x:
# 			all_dict[x][key] = name_count[key][1]


#print all_dict['California']


'''First API call to get the bioguide_id's. I keep in the new dictionary only the names I have ID's of.'''

# Momentarily commenitng out to experiment

# n = 0

# for x in all_states:
# 	for key in all_dict[x]:
# 		if key!='':
# 			query_params2 = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
# 						 	'firstname' : key.split()[0],
# 						  	'lastname' : key.split()[-1]
# 							}
# 			endpoint2 = "http://services.sunlightlabs.com/api/legislators.get.json"
# 			resp2 = requests.get(endpoint2, params = query_params2)
# 			if resp2.content == "No Such Object Exists" or resp2.content == "Multiple Legislators Returned":
# 				n+=1
# 				print '----------- not resolved' +' '+ str(n)
# 				continue
# 			else:
# 				data2 = resp2.json()
# 				# print data2['response']['legislator']['bioguide_id']
# 				all_dict_new[x][key]= [all_dict[x][key], data2['response']['legislator']['bioguide_id']]
		

# print all_dict_new['Alabama']


Alabama = {}
Alabama_new = {}

for key in name_count:
	if name_count[key][0] == 'Alabama':
		Alabama[key] = name_count[key][1]

n=0

for key in Alabama:
	if key!='':
		query_params2 = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
						 'firstname' : key.split()[0],
					  	'lastname' : key.split()[-1]
						}
		endpoint2 = "http://services.sunlightlabs.com/api/legislators.get.json"
		resp2 = requests.get(endpoint2, params = query_params2)
		if resp2.content == "No Such Object Exists" or resp2.content == "Multiple Legislators Returned":
			n+=1
			print '----------- not resolved' +' '+ str(n)
			continue
		else:
			data2 = resp2.json()
			# print data2['response']['legislator']['bioguide_id']
			Alabama_new[key]= [Alabama[key], data2['response']['legislator']['bioguide_id']]
		
# print len(Alabama)

# print len(Alabama_new)

# print Alabama_new



'''Finding the top words'''

words = {key: [Alabama_new[key][0]] for key in Alabama_new}

for key in Alabama_new:
	query_params = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
					 'per_page': 1,
					 'entity_type': 'legislator',
		   			 'entity_value': str(Alabama_new[key][1]),
		   			 'sort': 'tfidf desc' 'count desc'
		 			}

	endpoint = "http://capitolwords.org/api/phrases.json"
	response = requests.get(endpoint, params=query_params)
	data = response.json()
	words[key].append([(data[i]['ngram'],data[i]['count']) for i in range(len(data))])

# query_params = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
# 				 'per_page': 5,
# 				 'entity_type': 'legislator',
# 		   		 'entity_value': 'B001289',
# 	  			 'sort': 'count desc'
# 				}

# endpoint = "http://capitolwords.org/api/phrases.json"
# response = requests.get(endpoint, params=query_params)
# data = response.json()
# words = [(data[i]['ngram'],data[i]['count']) for i in range(len(data))]


# print data

print words






