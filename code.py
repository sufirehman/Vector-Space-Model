"""Vector space model for information retrieval
Ranked Retrieval of documents in decreasing order of cosine similarity matching the searched query"
"""

import math
import re
import sys
import glob
import ast
from lib2to3.pgen2 import token
from collections import defaultdict
from functools import reduce
from tkinter import messagebox, simpledialog
import tkinter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
route=tkinter.Tk()
route.withdraw()
stopwords = ['a','is' ,'the','of' ,'all','and' ,'to','can','be','as','once' ,'for','at',
'am','are','has','have','had','up','his','her','in','on','no','we','do','(',')','"','!',
'@','#','$','%','^','&','*','[',']','-',',','.','?', '/']

file = "files/*"

docid=[]

docs=dict()
size = 0
f=open("index.txt", 'r')
voc=f.read()
voc=ast.literal_eval(voc)
#print(voc)
f=open("posting.txt", 'r')
postings=f.read()
postings=ast.literal_eval(postings)
doc_freq = defaultdict(int)
length = defaultdict(float)
lemmatizer=WordNetLemmatizer()

def read_files():
    global docs, size

    # Fetch list of document names in corpus
    documents = glob.glob(file)

    # Set size of corpus
    size = len(documents)

    # Dictionary having doc id as key and document name as value
    docs = dict(zip(range(size), documents))
    
def process():
    """Function to process query and return the documents score in sorted order"""

    query=simpledialog.askstring(title="VSM Model", prompt="Search Query: ")     #tkinter gui for input from user
    query = tokenize(query)

    # Return if query is empty
    if query == []:
        sys.exit()
    scores = sorted(
        [(id, similarity(query, id)) for id in range(size)],
        key=lambda c: c[1],
        reverse=True,
    )

    return scores

def doc_frequency():
    """count for each term it appears in the number of documents
     and store the value in doc_frequency[term]"""

    global doc_freq
    for term in voc:
        #print(term)
        #if(term not in postings):
            #print(term)
        doc_freq[term] = len(postings[term])


def init_length():
    """ Computes the length of each document """
    #print("hello")
    global length
    for id in docs:
        s = 0
        for term in voc:
            s += term_freq(term, id) ** 2
        length[id] = math.sqrt(s)
        #print(length[id])

def tokenize(document):
    """returns list of separate terms in document"""
    """returns list of lowercase tokens after removing stopwords"""

    # Tokenize text into terms
    terms = word_tokenize(document)

   #removing stopwords and converting to lowercase
    terms = [t.lower() for t in terms if t not in stopwords]

    return terms

def term_freq(term, id):
    """returns the frequency of term in document id 
    and returns 0 if term is not in document """

    if id in postings[term]:
        return postings[term][id]
    else:
        return 0.0


def idf(term):
    """Returns the inverse document frequency of term.if
    term isn't in the vocabulary then returns 0"""

    if term in voc:
        return math.log(size / doc_freq[term
        ], 2)
    else:
        return 0.0


def print_result(scores):

    print("Document")
    print("-" * 42)
    resultset=[]
    for (id, score) in scores:
        if score != 0.0:
            #docid.append(docs[id])
            resultset.append(docs[id])
            #print(docs[id])
    #print(resultset)
    messagebox.showinfo("Document id: ", resultset)
    print("\n")

def similarity(query, id):
    """Returns the cosine similarity between query and document id.
    we don't bother dividing by the length of the query, 
    as this doesn't make any difference to the ordering of search results"""

    similar = 0.0
    alpha=0.001

    for term in query:

        if term in voc:

            # For every term in query which is also in the global vocabulary,
            # calculate its tf-idf score and add to similarity
            similar += term_freq(term, id) * idf(term)

    similar = similar / length[id]
    if(similar > alpha):
        return similar
    else:
        return 0


def main():
    # Get details about files
    read_files()

    # Setting document frequency for each terms
    doc_frequency()

    # Setting documents lengths
    init_length()

    # Allowing for search
    while True:

        # Retrieve sorted list of documents
        scores = process()

        # Printing the results
        print_result(scores)

if __name__ == "__main__":
    main()
