# !/usr/bin/python

''' Testing using GenSim utility '''
import logging
from math import *

from gensim import corpora, models, similarities
import nltk


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# # Main program


def main():
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error "
                 "measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering",
                 "Graph minors A survey"]
    # print documents
    tokens = [None] * len(documents)
    for i in range(len(documents)):
        tokens[i] = nltk.word_tokenize(documents[i])
    # print tokens
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
    print corpus

# # Run the main program
if __name__ == '__main__':
    main()

# #
######
