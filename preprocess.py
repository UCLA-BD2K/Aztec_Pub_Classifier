import nltk
import fileinput
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
import re
import string
import csv

########################################################################
# INPUT: text from title and abstract, e.g.:
# (line 1) <title text from article 1> <abstract text>
# (line 2) <title text from article 2> <abstract text>
#
# OUTPUT: dictionary of training data words to dictionary.csv;
# table of conditional frequency distribution as standard output, e.g.:
# 	word1	word2	word3	...
# 1		0		1		2
# 2		2		0		0
# ...
########################################################################

abstracts = [] # all text from title and abstract

for line in fileinput.input():
	abstracts.append(line)

# tokenize the text
for i in range(len(abstracts)):
	# remove urls
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

# results = [[]] * len(abstracts)
for i in range(len(abstracts)):
	for j in range(len(abstracts[i])):
		# remove apostrophes at beginnings of words left from contractions or single quotes
		abstracts[i][j] = re.sub(r'^\'', '', abstracts[i][j]) 
	for k in abstracts[i]:
		if k.lower() not in stopwords and k not in string.punctuation:
			word = es.stem(k.lower())
			# results[i].append(word)
			dictionary.add(word)
			pairs.append((i, word))

cfdist = nltk.ConditionalFreqDist(pairs)
cfdist.tabulate()

with open('dictionary.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(dictionary)
# print(results)
# print(cfdist.conditions())
