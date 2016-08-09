import json
import pubmed.extract as ex
import mongo
import classification as cl
from time import sleep
import numpy as np

class Feature1(cl.Feature):
    def getFeature(self, obj):
        title = obj['title']
        return (title.find(':') > 0)

class Feature2(cl.Feature):
    self.word_list = ['package', 'c++', 'java', 'software', 'r package', 'webserver', 'service', 'platform', 'database', 'tool', 'algorithm', 'implementation', 'available', 'download', 'script']
    def getFeature(self, obj):
        abstract = obj['abstract'].lower()
        features = []
        for word in word_list:
            features.append(cl.toBinary((abstract.find(word) > 0)))
        return features

class Feature3(cl.Feature):
    self.word_list = ['github', 'github.com','sourceforge', 'sourceforge.net', 'bioconductor', 'bioconductor.org']
    def getFeature(self, obj):
        abstract = obj['abstract'].lower()
        features = []
        for word in word_list:
            features.append(cl.toBinary((abstract.find(word) > 0)))
        return features



db  = mongo.DBClient('mongodb://BD2K:ucla4444@ds145415.mlab.com:45415/dois')
# db.queryDOI('10.1093/bioinformatics/btv089')
dois = ['10.1093/bioinformatics/btv089', '10.1093/bioinformatics/btv271', '10.1093/bioinformatics/btu854', '10.1093/bioinformatics/btw486']
doi = '10.1093/bioinformatics/btv089'
# abstract = ex.retrievePub(['26048599'])
# print(abstract)
# print(db.insertAbstract(abstract[0]))
# obj = db.queryDOI(doi)
# print(obj)
# f1 = Feature1()
# c = cl.Classification([f1], obj[0])
# print(c.buildFeatures())
# print(ex.extractAbstract('10.1093/bioinformatics/btv089'))
abstracts = ex.extractFromFile('../data.csv', 16)
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

papers = db.queryAll()

features = np.array([])
f1 = Feature1()
f2 = Feature2()
f3 = Feature3()


for paper in papers:
    
