#!/usr/bin/env python
	
import requests
import numpy as np
from BeautifulSoup import BeautifulSoup
# import csv
# #import urllib.request
# import json



with open('words.txt','r') as f:
	words = f.readlines()

words = [line.split() for line in words]
words2 = words

for i in range(len(words)):
	if len(words[i])>11:
		words2[i][0] = ' '.join([words[i][0], words[i][1]])
		del words2[i][1]

words_dict = {words2[i][0]: [words2[i][j] for j in range(1,11)] for i in range(len(words))}

for key in words_dict:
	for i in range(len(words_dict[key])):
		s = list(words_dict[key][i])
		for index, char in enumerate(s):
			if char == '\'':
				s[index] = '\\'+'\''
			elif char == '&':
				s[index] = '-'
		words_dict[key][i] = ''.join(s)


# Load the SVG map
svg = open('states.svg', 'r').read()
# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
# Find states
paths = soup.findAll('path')

# State style
# path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.7;\
# stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;\
# marker-start:none;stroke-linejoin:bevel;fill:'

all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', \
		'Georgia','Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', \
		'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', \
		'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', \
		'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', \
		'West Virginia', 'Wisconsin', 'Wyoming']




# for i in range(len(words_dict['Kentucky'])):
# 	print words_dict['Kentucky'][i]

display = {state: "display1('"+words_dict[state][0]+"'), display2('"+words_dict[state][1]+"'), display3('"+words_dict[state][2]+"'), \
	display4('"+words_dict[state][3]+"'), display5('"+words_dict[state][4]+"'), display6('"+words_dict[state][5]+"'), \
	display7('"+words_dict[state][6]+"'), display8('"+words_dict[state][7]+"'), display9('"+words_dict[state][8]+"'), \
	display10('"+words_dict[state][9]+"')" for state in all_states}

for state in all_states:
	for p in paths:
		if p['id'] == "path57":
			continue
		elif p['id'] == state:
			p['onmouseover']=display[state]



# Output map
new_map = soup.prettify()

#print new_map

f = open('states.svg', 'w')
f.write(new_map)
f.close()









