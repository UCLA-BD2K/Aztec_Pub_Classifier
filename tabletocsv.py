# table to csv

import fileinput
import csv
import sys
import argparse

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
print(args.features)
print(args.output)

first = 0
for line in fileinput.input(files='-'):
	# skip the first 2 rows because we don't want the labels or dummy row
	if first <= 1:
		first += 1
		continue
	# split on whitespace and cast to int
	# TODO: fix hardcoded max
	data.append([int(k)/17 for k in line.split()])

with open(args.features[0], 'r', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	k = 0
	for row in reader:
		data[k].append(row[0])
		data[k].append(row[1])
		k += 1

# write the data to a .csv file
with open(args.output[0], 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for datum in data:
		# skip first column because we don't want the labels
		del datum[0]
		writer.writerow(datum)