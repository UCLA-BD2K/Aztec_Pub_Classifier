# Aztec Pub Classifier
Classify publications as those which contain a software tool, and those which do not.

# Setup
* Python 3.5.1
* Install dependencies:
```
$ sudo pip3 install nltk
$ sudo pip3 install requests
```
* Download punkt, stopwords, and udhr using nltk.download()

# Run
```
$ python3 getdata.py | python3 preprocess.py | python3 tabletocsv.py
```
Outputs to frequencydata.csv and creates dictionary.csv
