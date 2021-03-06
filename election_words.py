#!/usr/bin/env python
	
import requests
import numpy as np
from BeautifulSoup import BeautifulSoup
import csv
#import urllib.request
import json


def give_score(times, pos, out_of):
	'''give a score to each word depending on how many times one person has been in congress, the position\
	of the words in his counting and how many words I consider from the highest recurring'''
	return times*(out_of-(pos+out_of)%out_of)


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
		'Georgia','Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', \
		'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', \
		'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', \
		'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', \
		'West Virginia', 'Wisconsin', 'Wyoming']

# Momentarily commenitng out to experiment

all_dict = {x: {} for x in all_states}

all_dict_new = {x: {} for x in all_states}

for x in all_states:
	for key in name_count:
		if name_count[key][0] == x:
			all_dict[x][key] = name_count[key][1]


#print all_dict['California']


'''First API call to get the bioguide_id's. I keep in the new dictionary only the names I have ID's of.'''

# Momentarily commenitng out to experiment

n = 0

for x in all_states:
	for key in all_dict[x]:
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
				all_dict_new[x][key]= [all_dict[x][key], data2['response']['legislator']['bioguide_id']]
		

# print all_dict_new['Alabama']


'''Finding the top words'''

all_words = {state: {} for state in all_states}

for state in all_dict_new:
	for key in all_dict_new[state]:
		query_params = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
						 'per_page': 10,
						 'entity_type': 'legislator',
		   				 'entity_value': str(all_dict_new[state][key][1]),
		   				 'sort': 'tfidf desc'
			 			}
		endpoint = "http://capitolwords.org/api/phrases.json"
		response = requests.get(endpoint, params=query_params)
		data = response.json()
		for i in range(len(data)):
			if data[i]['ngram'] not in all_words[state]:
				all_words[state][data[i]['ngram']] = give_score(all_dict_new[state][key][0],i,5)#data[i]['count']]
			else:
				all_words[state][data[i]['ngram']] += give_score(all_dict_new[state][key][0],i,5)


# print all_words['Alabama']

# print sorted(all_words['Alabama'], key=all_words['Alabama'].get)

# print all_words['New_York']

print sorted(all_words['Alaska'], key=all_words['Alaska'].get)
print '\n'


with open('words.txt', 'w') as f:
	for state in all_states:
		f.write(state+' ')
		if len(all_words[state]) >= 10:
			for i in range(10):
				f.write(sorted(all_words[state], key=all_words[state].get)[-(i+1)]+' ')
			f.write('\n')
		else:
			for i in range(len(all_words[state])):
				f.write(sorted(all_words[state], key=all_words[state].get)[-(i+1)]+' ')
			for i in range(10-len(all_words[state])):
				f.write('null ')
			f.write('\n')
		# f.write(', '.join(sorted(all_words[state], key=all_words[state].get)))
		# f.write('\n\n\n')


# with open('words.txt', 'w') as f:
# 	for state in all_states:
# 		f.write(state+'\n')
# 		if len(all_words[state]) >= 5:
# 			for i in range(0,5):
# 				f.write(sorted(all_words[state], key=all_words[state].get)[-(i+1)]+'\n')
# 		else:
# 			for i in range(len(all_words[state])):
# 				f.write(sorted(all_words[state], key=all_words[state].get)[-(i+1)]+'\n')
# 		f.write(', '.join(sorted(all_words[state], key=all_words[state].get)))
# 		f.write('\n\n\n')


# Ala = {}
# Ala_new = {}

# for key in name_count:
# 	if name_count[key][0] == 'New York':
# 		Ala[key] = name_count[key][1]

# n=0

# for key in Ala:
# 	if key!='':
# 		query_params2 = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
# 						 'firstname' : key.split()[0],
# 					  	'lastname' : key.split()[-1]
# 						}
# 		endpoint2 = "http://services.sunlightlabs.com/api/legislators.get.json"
# 		resp2 = requests.get(endpoint2, params = query_params2)
# 		if resp2.content == "No Such Object Exists" or resp2.content == "Multiple Legislators Returned":
# 			n+=1
# 			print '----------- not resolved' +' '+ str(n)
# 			continue
# 		else:
# 			data2 = resp2.json()
# 			# print data2['response']['legislator']['bioguide_id']
# 			Ala_new[key]= [Ala[key], data2['response']['legislator']['bioguide_id']]
		

# '''Finding the top words'''


# words = {}

# for key in Ala_new:
# 	query_params = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
# 					 'per_page': 5,
# 					 'entity_type': 'legislator',
# 		   			 'entity_value': str(Ala_new[key][1]),
# 		   			 'sort': 'tfidf desc'
# 		 			}

# 	endpoint = "http://capitolwords.org/api/phrases.json"
# 	response = requests.get(endpoint, params=query_params)
# 	data = response.json()
# 	for i in range(len(data)):
# 		if data[i]['ngram'] not in words:
# 			words[data[i]['ngram']] = give_score(Ala_new[key][0],i,5)#data[i]['count']]
# 		else:
# 			words[data[i]['ngram']] += give_score(Ala_new[key][0],i,5)


# with open('words.txt', 'w') as f:
# 	#for state in all_states:
# 	f.write('New York\n')
# 	for i in range(0,5):
# 		f.write(sorted(words, key=words.get)[-(i+1)] + '\n')
# 	f.write(' '.join(sorted(words, key=words.get)))
# 	f.write('\n')

# # print words

# print sorted(words, key=words.get)
# print '\n'

# for i in range(0,5):
# 	print sorted(words, key=words.get)[-(i+1)]




# query_params3 = { 'apikey': '2cd8dea668b840f989b145e88cb2be80',
# 				 # 'per_page': 5,
# 				 # 'page': 2,
# 				 'phrase': 'today',
# 				 # 'entity_type': 'state',
# 		   # 		 'entity_value': 'AL',
# 	  			 # 'sort':'count desc'
# 				}

# endpoint = "http://capitolwords.org/api/phrases/state.json"
# response3 = requests.get(endpoint, params=query_params3)
# data3 = response3.json()
# # words3 = [(data3[i]['ngram'],data3[i]['tfidf']) for i in range(len(data3))]


# for i in range(len(data3['results'])):
# 	if data3['results'][i]['state'] == 'AL':
# 		print data3['results'][i]

# print len(words3)

# for x in range(len(words3)):
# 	if words3[x][0] == 'count':
# 		print words3[x][1]
# 	# else:
# 	# 	print '------- could not find it'





