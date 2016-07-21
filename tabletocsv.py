# table to csv

import fileinput
import csv
import sys

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
filename = 'trainX.csv'

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: python3 tabletocsv.py <output file>")
	exit(1)

first = 0
for line in fileinput.input(files='-'):
	# skip the first 2 rows because we don't want the labels or dummy row
	if first <= 1:
		first += 1
		continue
	# split on whitespace and cast to int
	# TODO: fix hardcoded max
	data.append([int(k)/17 for k in line.split()])

# write the data to a .csv file
with open(filename, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for datum in data:
		# skip first column because we don't want the labels
		del datum[0]
		writer.writerow(datum)