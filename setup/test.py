import json
import pubmed.extract as ex
import mongo
import classification as cl

class Feature1(cl.Feature):
    def getFeature(self, obj):
        title = obj['title']
        return (title.find('alignment') > 0)


db  = mongo.DBClient('mongodb://BD2K:ucla4444@ds145415.mlab.com:45415/dois')
# db.queryDOI('10.1093/bioinformatics/btv089')
dois = ['10.1093/bioinformatics/btv089', '10.1093/bioinformatics/btv271', '10.1093/bioinformatics/btu854', '10.1093/bioinformatics/btw486']
doi = '10.1093/bioinformatics/btv089'
# abstract = ex.retrievePub(['25681254'])
# print(db.insertAbstract(abstract[0]))
obj = db.queryDOI(doi)
print(obj)
f1 = Feature1()
c = cl.Classification([f1], obj[0])
print(c.buildFeatures())
