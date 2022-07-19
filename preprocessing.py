import math
import re
import sys
import glob
from lib2to3.pgen2 import token
from collections import defaultdict
from functools import reduce
from nbformat import read
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords = ['a','is' ,'the','of' ,'all','and' ,'to','can','be','as','once' ,'for','at',
'am','are','has','have','had','up','his','her','in','on','no','we','do','(',')','"','!',
'@','#','$','%','^','&','*','[',']','-',',','.','?', '/']

#file = "files/*"

docs=dict()
size = 0
voc = set()
postings = {} #defaultdict(dict)
doc_freq = defaultdict(int)
length = defaultdict(float)
lemmatizer=WordNetLemmatizer()
file = "files/*"

def read_files():
    global docs, size

    # Fetch list of document names in corpus
    documents = glob.glob(file)

    # Set size of corpus
    size = len(documents)

    # Dictionary having doc id as key and document name as value
    docs = dict(zip(range(size), documents))

def preprocess(token):
    token=lemmatizer.lemmatize(token)
    """ Removing special characters and digits using regex substitution """
    regex = re.compile(r"[^a-zA-Z0-9\s]")
    regex = re.compile(r"\d")
    return re.sub(regex, "", token)

def initialize():
    """Read files and tokenizes it(list of terms), add new terms to global vocab
    and add the doc in posting list for each term with value equal to term frequency in document"""

    global voc, postings
    for id in docs:

        # Read the document
        with open(docs[id], "r") as f:
            document = f.read()

        # Remove all special characters from the document
        document = preprocess(document)

        # Tokenize the document
        terms = tokenize(document)

        # Remove duplicates from the terms
        unique_terms = set(terms)

        # Add unique terms to the vocabulary
        voc = voc.union(unique_terms)

        #Indexing to store each term
        f=open("index.txt", 'w')
        f.write(str(voc))
        f.close()
        
        # For every unique term
        for term in unique_terms:

            # The value is the frequency of the term in the document
            postings.setdefault(term,{})
            postings[term][id] = terms.count(term)
            #print(postings[term][id])
        f=open("posting.txt", 'w')
        f.write(str(postings))
        f.close()

def tokenize(document):
    """returns list of separate terms in document"""
    """returns list of lowercase tokens after removing stopwords"""

    # Tokenize text into terms
    terms = word_tokenize(document)

   #removing stopwords and converting to lowercase
    terms = [t.lower() for t in terms if t not in stopwords]

    return terms

def main():
    read_files()
    initialize()

if __name__ == "__main__":
    main()