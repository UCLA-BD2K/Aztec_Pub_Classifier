# extract.py
# author: Allison Ko

#####################################################################
# INPUT: data.csv with pubmed IDs and 1/0 tool or not tool, e.g:
# 1234567,1
# 9876543,0
#
# OUTPUT: json object including pmid, text from title and abstract, e.g.:
# {pmid:<int>, is_tool:<true,false>, title:<string>, abstract:<string>}
#####################################################################

# Dependencies
import requests
import csv
import xml.etree.ElementTree as ET
import re
import sys
import json
from bs4 import BeautifulSoup



class PubmedExtract:
    """Extract publication data from Pubmed"""
    PUBMED_ID_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id='
    DOI_ID_URL = 'http://dx.doi.org/'
    def __init__(self, journal=None):
        self.m_journal = journal


    def extract(self, input='data.csv', output='values.json'):
        # read data from .csv
        results = [] # return array of objects

        pubIDs = []
        pub_dict = dict() # keeps track of [pmid, obj(id, title, abstract, is_tool)] values

        # parse values from input file and store in dictionary
        with open(input) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                pubIDs.append(row[0])
                obj = {}
                obj['pmid'] = int(row[0])
                obj['is_tool'] = (True if int(row[1]) == 1 else False)
                pub_dict[row[0]] = obj

        # call the pubmed API with IDs and get the results
        xml_data = [] # data received from query in XML format
        for id in pubIDs:
        	tempURL = self.PUBMED_ID_URL + id
        	r = requests.get(tempURL)
        	xml_data.append(r.text)

        # parse the xml results and just get the article title and abstract
        for data in xml_data:
            root = ET.fromstring(data.encode('utf-8'))
            pmid = root.find('PubmedArticle').find('MedlineCitation').find('PMID').text
            article = root.find('PubmedArticle').find('MedlineCitation').find('Article')
            obj = pub_dict[pmid]
            obj['title'] = article.find('ArticleTitle').text
            obj['abstract'] = ''

            full_info_count = 0 # keeps track of how many sections were found in pubmed
            abstract = article.find('Abstract')
            if abstract is not None:
                for section in abstract.findall('AbstractText'):
                    if section.text is not None:
                        full_info_count+=1
                        obj['abstract'] += section.text + " "
            obj['doi'] = article.find('ELocationID').text
            if len(obj['doi']) < 10:
                obj['doi'] = '10.1093/bioinformatics/' + obj['doi']

            # if pubmed does not have the abstract or if it seems like it is missing info, extract abstract from website
            if obj['abstract'] == '' or full_info_count < 4:
                obj['abstract'] = self.extractAbstract(obj['doi'])
            results.append(obj)

        # write objects to output file
        with open(output, 'w') as jsonfile:
        	json.dump(results, jsonfile)

        return results

    def extractAbstract(self, doi):
        doi_url = self.DOI_ID_URL+str(doi)

        # make request for abstract
        r = requests.get(doi_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # parse and extract abstract from webpage
        abstract = BeautifulSoup(str(soup.find(id='abstract-1')), 'html.parser')

        return abstract.get_text()


#######################################################################
#
#                   Command Line Script
#
#######################################################################


if len(sys.argv) != 3:
	print("Usage: python3 extract.py <data file> <value output file>")
	exit(1)
else:
    input = str(sys.argv[1])
    output = str(sys.argv[2])
    ex = PubmedExtract()
    print(ex.extract(input, output))
