import json
import pubmed.extract as ex
import mongo
import classification as cl
from time import sleep
import numpy as np
import csv

# Features

# Feature 1: check for colon
class Feature1(cl.Feature):
    def getFeature(self, obj):
        title = obj['title']
        return [(title.find(':') > 0)]

# Feature 2: Check for technical terms
class Feature2(cl.Feature):
    def __init__(self, word_list):
        super(Feature2, self).__init__()
        self.word_list = word_list
    # word_list = ['package', 'c++', 'java', 'software', 'r package', 'webserver', 'service', 'platform', 'database', 'tool', 'algorithm', 'implementation', 'available', 'download', 'script', 'input', 'output']
    def getFeature(self, obj):
        abstract = obj['abstract'].lower()
        features = []
        for word in self.word_list:
            count = 0
            temp = abstract
            index = temp.find(word)
            while index > 0:
                count += 1
                temp = temp[index+1:]
                index = temp.find(word)
            features.append(count)
        return features
# Feature 3: check for code repos
class Feature3(cl.Feature):
    word_list = ['github', 'github.com','sourceforge', 'sourceforge.net', 'bioconductor', 'bioconductor.org']
    def getFeature(self, obj):
        abstract = obj['abstract'].lower()
        features = []
        for word in self.word_list:
            features.append(cl.toBinary((abstract.find(word) > 0)))
        return features


# connect to mongo db
db  = mongo.DBClient('mongodb://BD2K:ucla4444@ds145415.mlab.com:45415/dois')

# #############################################################
# Extract abstracts from Pubmed and insert into database
# ############################################################
#
# abstracts = ex.extractFromFile('../data.csv', 16)
# print(abstracts)

# for a in abstracts:
#     query = db.queryDOI(a['doi'])
#     if query[0]['abstract']=='None':
#         retry = 0
#         while a['abstract']=='None' and retry < 10:
#             sleep(retry*0.5)
#             abstract = ex.extractAbstract(a['doi'])
#             if abstract is not None or abstract!='None':
#                 a['abstract'] = abstract
#             print(a['doi'], 'Extracted abstract:', (a['abstract']!='None'))
#             retry+=1
#         db.insertAbstract(a)
# #############################################################

# #############################################################
# Create features from training set and apply logistic regression
# ############################################################
papers = db.queryAll()
# papers = db.queryDOI('10.1093/bioinformatics/btv187')

# get word list from file
word_list = []
with open('dict.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for k in range(len(row)):
            word_list.append(row[k])

# features
f1 = Feature1()
f2 = Feature2(word_list)
f3 = Feature3()
feature_list = [f1,f2,f3]

# prepare classification model
classifier = cl.Classification(feature_list, papers)
'''
(all_features, labels) = classifier.buildFeatures()
train = cl.Trainer(0.01, 25000, 100, 100)
train.setInputDataSize(len(all_features[0]), 2)
for i in range(len(all_features)):
    print(all_features[i], labels[i])
train.runLogisticReg(all_features[0:400], labels[0:400], all_features[400:500], labels[400:500])
'''

train = cl.Trainer(0.01, 10000, 100, 100)
trainX = np.genfromtxt("trainX.csv", delimiter=" ")
trainY = np.genfromtxt("trainY.csv", delimiter=" ")
testX = np.genfromtxt("testX.csv", delimiter=" ")
testY = np.genfromtxt("testY.csv", delimiter=" ")
train.setInputDataSize(len(trainX[0]), 2)
train.runLogisticReg(trainX, trainY, testX, testY)