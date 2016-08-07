from pymongo import MongoClient
import string


class DBClient:
    def __init__(self, mongo_url):
        self.client = MongoClient(mongo_url)
        db_name = mongo_url[(mongo_url.rindex('/')+1):]
        self.db = self.client[db_name]

    def queryDOI(self, doi):
        cursor = self.db.numbers.find({'doi':doi})
        print(cursor)
        for doc in cursor:
            print(doc)

    def queryDOIList(self, doi):
        cursor = self.db.numbers.find({'doi': {'$in': dois}})
        print(cursor)
        for doc in cursor:
            print(doc)

db  = DBClient('mongodb://BD2K:ucla4444@ds145415.mlab.com:45415/dois')
# db.queryDOI('10.1093/bioinformatics/btv089')
dois = ['10.1093/bioinformatics/btv089', '10.1093/bioinformatics/btv271', '10.1093/bioinformatics/btu854', '10.1093/bioinformatics/btw486']
db.queryDOIList(dois)
