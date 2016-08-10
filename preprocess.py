import nltk
import fileinput
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
import re
import string
import csv
import argparse
import json
import sys
from nltk.probability import FreqDist
from nltk.tokenize import MWETokenizer

########################################################################
# INPUT: text from title and abstract, e.g.:
# (line 1) <title text from article 1> <abstract text>
# (line 2) <title text from article 2> <abstract text>
#
# OUTPUT: dictionary of training data words to dictionary.csv;
# table of conditional frequency distribution as standard output, e.g.:
# 		word1	word2	word3	...
# pub1		0		1		2
# pub2		2		0		0
# ...
########################################################################

parser = argparse.ArgumentParser(description='Create conditional frequency distribution from a list of texts.')
parser.add_argument('--train', action='store_true',
					help='Use as training data and create dictionary (default: test data)')
args = parser.parse_args()
data = [] # json output from extract.py

for line in fileinput.input(files='-'):
	data = json.loads(line)

miscFeatures = [] # other features
abstracts = []
tool = []
# tokenize the text

# pairs for conditional frequency distribution
pairs = []

tokenizer = MWETokenizer([('web', 'server'), ('software', 'package'), ('R', 'package'), ('freely', 'available'), ('source', 'code')])

for i in range(len(data)):
	# change github, bioconductor, sourceforge urls to unique words
	title = data[i]['title']
	colon = title.find(':')
	miscFeatures.append([])

	if colon >= 0:
		miscFeatures[i].append(1)

		pairs.append((i+1, '-hascolon'))
		a = title[0:colon]
		b = a.lower()
		diff = sum(a[k] != b[k] for k in range(len(a)))
		# ratio = diff/len(a)
		# miscFeatures[i].append(ratio)
		for k in range(diff):
			pairs.append((i+1, '-uppercasechars'))
	else:
		miscFeatures[i].append(0)
		a = title
		b = a.lower()
		diff = sum(a[k] != b[k] for k in range(len(a)))
		# ratio = diff/len(a)
		# miscFeatures[i].append(ratio)
		for k in range(diff):
			pairs.append((i+1, '-uppercasechars'))

	if data[i]['is_tool']:
		tool.append((1, 0))
	else:
		tool.append((0, 1))
	abstracts.append(data[i]['abstract'] + ' ' + data[i]['title'])

	abstracts[i] = re.sub(r'https?:\/\/github\.com\S*', 'githuburl', abstracts[i])
	abstracts[i] = re.sub(r'https?:\/\/bioconductor\.org\S*', 'bioconductorurl', abstracts[i])
	abstracts[i] = re.sub(r'https?:\/\/sourceforge\.net\S*', 'sourceforgeurl', abstracts[i])
	abstracts[i] = re.sub(r'https?:\/\/bitbucket\.org\S*', 'bitbucketurl', abstracts[i])
	# remove all other urls
	abstracts[i] = re.sub(r'https?:\/\/\S*', 'url', abstracts[i])
	abstracts[i] = re.sub(r'www\.\S*', 'url', abstracts[i])
	# remove email addresses
	abstracts[i] = re.sub(r'\S*@\S*', ' ', abstracts[i])
	# change slashes to spaces
	abstracts[i] = re.sub(r'\/', ' ', abstracts[i])
	abstracts[i] = word_tokenize(abstracts[i])
	abstracts[i] = tokenizer.tokenize(abstracts[i])

# filter stopwords and punctuation
stopwords = nltk.corpus.stopwords.words('english')

# lemmatize words
#es = EnglishStemmer()



# dictionary created to be used later when preprocessing testing data
dictionary = set()
fdist = FreqDist()
#if not args.train:
with open('dict.csv', 'r', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader:
		for k in range(len(row)):
			dictionary.add(row[k])
		break

languages = []
with open('language_data.txt', 'r', newline='') as file:
	for line in file:
		languages.append(line.rstrip('\n'))

# results = [[]] * len(abstracts)
for i in range(len(abstracts)):
	miscFeatures[i].append(0)
	for k in abstracts[i]:
		if k.lower() not in stopwords and k not in string.punctuation:
			#word = es.stem(k.lower())
			word = k.lower()
			# remove apostrophes at beginnings of words left from contractions or single quotes
			word = re.sub(r'^\'', '', word)
			if word == 'githuburl' or word == 'bioconductorurl' or word == 'sourceforgeurl' or word == 'bitbucketurl':
				#miscFeatures[i][2] += 1
				pairs.append((i+1, '-repo-url'))
			#if word in languages:
		#		pairs.append((i+1, '-haslanguage'))
			# remove strings that contain ONLY numbers and punctuation
			if re.fullmatch(r'[0-9\!\"\#\$\%\&\'\(\)\*\+\,\-.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~≥]*', word) is None:
				'''
				if args.train:
					pairs.append((i+1, word))
					# dictionary.add(word)
					fdist[word] += 1
					'''
				if word in dictionary:
					pairs.append((i+1, word))

#if args.train:
#	for n in fdist:
#		if fdist[n] >= 15:
#			dictionary.add(n)

for k in dictionary:
	pairs.append((0, k))

cfdist = nltk.ConditionalFreqDist(pairs)
# topwords = [n for n in dictionary]
# topwords.sort()
cfdist.tabulate()
# cfdist.tabulate(samples=topwords)

filename = 'miscfeaturestest.csv'
yfile = 'testY.csv'
if args.train:
	filename = 'miscfeatures.csv'
	yfile = 'trainY.csv'


with open(yfile, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
	for row in tool:
		writer.writerow(row)

# write misc features, i.e. features that aren't word frequency, to file
with open(filename, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for row in miscFeatures:
		writer.writerow(row)

'''
if args.train:
	with open('dictionary.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(dictionary)
# print(results)
# print(cfdist.conditions())
'''