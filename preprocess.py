import nltk
import fileinput
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
import re
import string
import csv
import argparse

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
abstracts = [] # all text from title and abstract

for line in fileinput.input(files='-'):
	abstracts.append(line)

miscFeatures = [] # other features

# tokenize the text
for i in range(len(abstracts)):
	# change github, bioconductor, sourceforge urls to unique words
	title = abstracts[i].split('#')[0]
	colon = title.find(':')
	miscFeatures.append([])
	if colon >= 0:
		miscFeatures[i].append(1)
		a = title[0:colon]
		b = a.lower()
		diff = sum(a[k] != b[k] for k in range(len(a)))
		ratio = diff/len(a)
		miscFeatures[i].append(ratio)
	else:
		miscFeatures[i].append(0)
		a = title
		b = a.lower()
		diff = sum(a[k] != b[k] for k in range(len(a)))
		ratio = diff/len(a)
		miscFeatures[i].append(ratio)

	abstracts[i] = re.sub(r'https?:\/\/github\.com\S*', 'githuburl', abstracts[i])
	abstracts[i] = re.sub(r'https?:\/\/bioconductor\.org\S*', 'bioconductorurl', abstracts[i])
	abstracts[i] = re.sub(r'https?:\/\/sourceforge\.net\S*', 'sourceforgeurl', abstracts[i])
	# remove all other urls
	abstracts[i] = re.sub(r'https?:\/\/\S*', 'url', abstracts[i])
	abstracts[i] = re.sub(r'www\.\S*', 'url', abstracts[i])
	# remove email addresses
	abstracts[i] = re.sub(r'\S*@\S*', ' ', abstracts[i])
	# change slashes to spaces
	abstracts[i] = re.sub(r'\/', ' ', abstracts[i])
	abstracts[i] = word_tokenize(abstracts[i])

# filter stopwords and punctuation
stopwords = nltk.corpus.stopwords.words('english')
# lemmatize words
es = EnglishStemmer()
# pairs for conditional frequency distribution
pairs = []

# dictionary created to be used later when preprocessing testing data
dictionary = set([])
if not args.train:
	with open('dictionary.csv', 'r', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in reader:
			for k in range(len(row)):
				dictionary.add(row[k])

# write misc features to file
with open('miscfeatures.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for row in miscFeatures:
		writer.writerow(row)

# results = [[]] * len(abstracts)
for i in range(len(abstracts)):
	for k in abstracts[i]:
		if k.lower() not in stopwords and k not in string.punctuation:
			word = es.stem(k.lower())
			# remove apostrophes at beginnings of words left from contractions or single quotes
			word = re.sub(r'^\'', '', word)
			# remove strings that contain ONLY numbers and punctuation
			if re.fullmatch(r'[0-9\!\"\#\$\%\&\'\(\)\*\+\,\-.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~≥]*', word) is None:
				if args.train:
					dictionary.add(word)
					pairs.append((i+1, word))
				elif word in dictionary:
					pairs.append((i+1, word))

for k in dictionary:
	pairs.append((0, k))

cfdist = nltk.ConditionalFreqDist(pairs)
cfdist.tabulate()

if args.train:
	with open('dictionary.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(dictionary)
# print(results)
# print(cfdist.conditions())
