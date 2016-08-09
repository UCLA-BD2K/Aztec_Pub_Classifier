# extract.py
# author: Allison Ko

#####################################################################
# INPUT: data.csv with pubmed IDs and 1/0 tool or not tool, e.g:
# 1234567,1
# 9876543,0
#
# OUTPUT: json object including pmid, text from title and abstract, e.g.:
# [{pmid:<int>, is_tool:<true,false>, title:<string>, abstract:<string>},...]
#####################################################################

# Dependencies
import pubmed.extract as ex
import argparse



#######################################################################
#
#                   Command Line Script
#
#######################################################################

parser = argparse.ArgumentParser(description='Create conditional frequency distribution from a list of texts.')

parser.add_argument('-i', '--input', type=str, default='data.csv',
					help='Input file with PMIDs and classification [default: data.csv]')

parser.add_argument('-o', '--output', type=str, default='values.json',
					help='Output file that will contain an array of Abstract JSON data [default: values.json]')

parser.add_argument('-j', '--journal', type=str, default=None,
					help='Name of the journal')

args = parser.parse_args()

input = str(args.input)
output = str(args.output)
journal = args.journal
if not args.journal:
    print(ex.extractFromFile(input, output))
else:
    print(ex.extractFromJournal(journal))
