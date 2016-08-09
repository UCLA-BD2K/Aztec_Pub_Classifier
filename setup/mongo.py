from pymongo import MongoClient
import string


class DBClient:
    def __init__(self, mongo_url):
        self.client = MongoClient(mongo_url)
        db_name = mongo_url[(mongo_url.rindex('/')+1):]
        self.db = self.client[db_name]

    def queryDOI(self, doi):
        cursor = self.db.numbers.find({'doi':doi})
        results = []
        for doc in cursor:
            results.append(doc)
        return results

    def queryDOIList(self, dois):
        cursor = self.db.numbers.find({'doi': {'$in': dois}})
        results = []
        for doc in cursor:
            results.append(doc)
        return results

    def queryAll(self):
        cursor = self.db.numbers.find({})
        results = []
        for doc in cursor:
            results.append(doc)
        return results

    def insertAbstract(self, abstract):
        obj = {'title':abstract['title'], 'abstract':abstract['abstract'], 'pmid' :abstract['pmid']}
        if 'is_tool' in abstract:
            obj['is_tool'] = abstract['is_tool']

        result = self.db.numbers.update_one({'doi':abstract['doi']},
            {'$set':obj},
            upsert=True)
        return result
