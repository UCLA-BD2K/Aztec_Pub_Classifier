# find most frequent words that exist only in publications containing tools

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import nltk
import json
import fileinput
import string
import re

for line in fileinput.input(files='-'):
	data = json.loads(line)

toolfdist = FreqDist()
nontoolfdist = FreqDist()

stopwords = nltk.corpus.stopwords.words('english')

for i in range(len(data)):
	text = word_tokenize(data[i]['abstract'])
	if data[i]['is_tool']:
		for word in text:
			word = word.lower()
			if word not in stopwords and word not in string.punctuation and re.fullmatch(r'[0-9\!\"\#\$\%\&\'\(\)\*\+\,\-.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~≥]*', word) is None:
				toolfdist[word] += 1
	else:
		for word in text:
			word = word.lower()
			if word not in stopwords and word not in string.punctuation and re.fullmatch(r'[0-9\!\"\#\$\%\&\'\(\)\*\+\,\-.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~≥]*', word) is None:
				nontoolfdist[word] += 1

for word in toolfdist:
	if word in nontoolfdist:
		toolfdist[word] -= 10*nontoolfdist[word]
		#toolfdist[word] = 0

toolfdist.tabulate(200)