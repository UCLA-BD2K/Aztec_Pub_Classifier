# preprocess

import requests
import csv
import xml.etree.ElementTree as ET
import re

#####################################################################
# INPUT: data.csv with pubmed IDs and 1/0 tool or not tool, e.g:
# 1234567,1
# 9876543,0
#
# OUTPUT: prints text from title and abstract, e.g.:
# 1 <title text from article 1> <abstract text>
# 2 <title text from article 2> <abstract text>
#####################################################################

# TODO: default output to some generic filename if output is not redirected

url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id='
data = [] # data received from query in XML format
pubID = [] # pubmed IDs
vals = [] # binary value, tool or not tool
# titles = [] # article titles
# abstracts = [] # abstract texts
abstracts = [] # all text; titles + abstracts

# read data from .csv
with open('data.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		# x = row[0].find(',')
		pubID.append(row[0])
		vals.append(row[1])

# call the pubmed API with IDs and get the results
for ids in pubID:
	tempURL = url + ids
	r = requests.get(tempURL)
	data.append(r.text)

# parse the xml results and just get the article title and abstract
for datum in data:
	root = ET.fromstring(datum.encode('utf-8'))
	article = root.find('PubmedArticle').find('MedlineCitation').find('Article')
	temp = article.find('ArticleTitle').text
	for section in article.find('Abstract').findall('AbstractText'):
		temp += ' ' + section.text
	abstracts.append(temp)

# output tokenized data
for k in abstracts:
	print(k)