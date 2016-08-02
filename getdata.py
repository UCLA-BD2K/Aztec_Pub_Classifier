import requests
import csv
import xml.etree.ElementTree as ET
import re
import sys

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

filename = 'data.csv'
outfile = 'values.csv'

if len(sys.argv) == 3:
	filename = str(sys.argv[1])
	outfile = str(sys.argv[2])

if len(sys.argv) != 3:
	print("Usage: python3 getdata.py <data file> <value output file>")
	exit(1)

# read data from .csv
with open(filename) as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		# x = row[0].find(',')
		pubID.append(row[0])
		vals.append((int(row[1]), 0 if int(row[1]) == 1 else 1))

# call the pubmed API with IDs and get the results
for ids in pubID:
	tempURL = url + ids
	r = requests.get(tempURL)
	data.append(r.text)

# parse the xml results and just get the article title and abstract
z = 0
for datum in data:
	root = ET.fromstring(datum.encode('utf-8'))
	article = root.find('PubmedArticle').find('MedlineCitation').find('Article')
	temp = article.find('ArticleTitle').text + ' # '
	for section in article.find('Abstract').findall('AbstractText'):
		if section.text is not None:
			temp += section.text
	abstracts.append(temp)
	z += 1

# put values in Y file
with open(outfile, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
	for val in vals:
		writer.writerow(val)

# output tokenized data
for k in abstracts:
	print(k)