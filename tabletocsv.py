# table to csv

import fileinput
import csv

########################################################################
# INPUT:
# table of conditional frequency distribution as standard output, e.g.:
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

first = 0
for line in fileinput.input():
	# skip the first row because we don't want the labels
	if first == 0:
		first = 1
		continue
	# split on whitespace and cast to int
	data.append([int(k) for k in line.split()])

# write the data to a .csv file
with open('frequencydata.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for datum in data:
		# skip first column because we don't want the labels
		del datum[0]
		writer.writerow(datum)