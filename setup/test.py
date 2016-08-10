import json
import pubmed.extract as ex
import mongo
import classification as cl
from time import sleep
import numpy as np


# Features

# Feature 1: check for colon
class Feature1(cl.Feature):
    def getFeature(self, obj):
        title = obj['title']
        return [(title.find(':') > 0)]

# Feature 2: Check for technical terms
class Feature2(cl.Feature):
    word_list = ['package', 'c++', 'java', 'software', 'r package', 'webserver', 'service', 'platform', 'database', 'tool', 'algorithm', 'implementation', 'available', 'download', 'script', 'input', 'output']
    def getFeature(self, obj):
        abstract = obj['abstract'].lower()
        features = []
        for word in self.word_list:
            features.append(cl.toBinary((abstract.find(word) > 0)))
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

# features
f1 = Feature1()
f2 = Feature2()
f3 = Feature3()
feature_list = [f1,f2,f3]

# prepare classification model
classifier = cl.Classification(feature_list, papers)

(all_features, labels) = classifier.buildFeatures()
train = cl.Trainer(0.01, 500, 100, 50)
train.setInputDataSize(len(all_features[0]), 1)

train.runLogisticReg(all_features[0:300], labels[0:300], all_features[300:500], labels[300:500])
