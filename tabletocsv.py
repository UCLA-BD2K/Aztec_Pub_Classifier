# table to csv

import fileinput
import csv
import sys
import argparse
from sklearn import preprocessing
import numpy as np

########################################################################
# INPUT:
# table of conditional frequency distribution as standard input, e.g.:
# 	word1	word2	word3	...
# 1		0		1		2
# 2		2		0		0
# ...
#
# OUTPUT: to frequencydata.csv where each row has the word frequencies
# for one particular article, e.g.:
# (line 1) 0 1 2 0 ...
# (line 2) 1 0 1 0 ...
########################################################################

data = []

parser = argparse.ArgumentParser(description='Convert frequency distribution table into a .csv file that can be fed into the classifier')
parser.add_argument('--features', '-f', nargs=1, default=None,
					help='Any additional features in a .csv file')
parser.add_argument('output', nargs=1,
					help='Name of output file for X data')
args = parser.parse_args()

first = 0
for line in fileinput.input(files='-'):
	# skip the first 2 rows because we don't want the labels or dummy row
	if first <= 1:
		first += 1
		continue
	# split on whitespace and cast to int
	data.append([int(k) for k in line.split()])

with open(args.features[0], 'r', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	k = 0
	for row in reader:
		data[k].append(row[0])
		data[k].append(row[1])
		k += 1

# scale data with sklearn
X = np.array(data)
X = np.delete(X, 0, 1)
scaler = preprocessing.MaxAbsScaler()
X = scaler.fit_transform(X)

# write the data to a .csv file
with open(args.output[0], 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for datum in X:
		# skip first column because we don't want the labels
		writer.writerow(datum)