import csv

# combines X and Y data into format used in tensorflow's contrib.learn API with the datasets.base.load_csv function
# output:
# <num examples> <num features>
# <data>


train = []
test = []

with open('trainX.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader:
		train.append(row)

with open('testX.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in reader:
		test.append(row)

with open('trainY.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i = 0
	for row in reader:
		train[i].append(row[0])
		i += 1

with open('testY.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i = 0
	for row in reader:
		test[i].append(row[0])
		i += 1

with open('train.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|')
	writer.writerow([len(train), len(train[0])-1])
	for row in train:
		writer.writerow(row)

with open('test.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|')
	writer.writerow([len(test), len(test[0])-1])
	for row in test:
		writer.writerow(row)