#!/usr/bin/env python
	
import requests
import numpy as np
from BeautifulSoup import BeautifulSoup
import csv



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
	# print len(set(names04).intersection(set(names05)).intersection(set(names06)))

all_of_them = [names04,names05,names06,names07,names08,names09,names10,names11,names12,names13]

name_count = names04

for key in name_count:
	name_count[key].append(0)

# print name_count['Lloyd Doggett'][1]
# name_count['Lloyd Doggett'][1]+=1
# print name_count['Lloyd Doggett'][1]
for x in all_of_them:
	for name in x:
		if name in name_count:
			name_count[name][1] += 1
		else:
			name_count[name] = x[name]
			name_count[name].append(1)

print len(name_count)



all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', \
		'Georgia','Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Lousiana', 'Maine', 'Maryland', \
		'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New_Hampshire', \
		'New_Jersey', 'New_Mexico', 'New_York', 'North_Carolina', 'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', \
		'Rhode_Island', 'South_Carolina', 'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', \
		'West_Virginia', 'Wisconsin', 'Wyoming']


for key in name_count:
	if name_count[key][0] == 'Pennsylvania':
		print key + ' ' + str(name_count[key][1])




