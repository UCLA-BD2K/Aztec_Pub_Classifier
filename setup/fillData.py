import json
import pubmed.extract as ex
import mongo
from time import sleep
import numpy as np
import csv



# connect to mongo db
db  = mongo.DBClient('mongodb://BD2K:ucla4444@ds145415.mlab.com:45415/dois')

# #############################################################
# Extract abstracts from Pubmed and insert into database
# ############################################################

abstracts = ex.extractFromFile('./data.csv', 16)

for a in abstracts:
    query = db.queryDOI(a['doi'])
    queriedObject = None

    if len(query) < 1:
        db.insertAbstract(a)
        queriedObject = a
    else:
        queriedObject = query[0]

    if queriedObject['abstract']=='None' or len(queriedObject['abstract']) < 200:
        retry = 0
        while (a['abstract']=='None' or len(a['abstract']) < 200) and retry < 10:
            sleep(3)
            abstract = ex.extractAbstract(a['doi'])
            if abstract is not None or abstract!='None':
                a['abstract'] = abstract
            print(a['doi'], 'Extracted abstract:', (a['abstract']!='None'))
            retry+=1
        db.insertAbstract(a)
# #############################################################
