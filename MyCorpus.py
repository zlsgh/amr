# !/usr/bin/python

'''
My Corpus class used to create the gensim corpus from the token data tored in a corpus.txt file.
'''
# # Imports
import codecs
import email
from email.parser import Parser
from math import *
import string

from gensim import corpora, models, similarities
import nltk
from nltk.corpus import stopwords


# # New instance of corpus gets the documents out of mycorpus.txt file
class MyCorpus:
    def __init__(self, corpusName):
        # Get documents out of mycorpus.txt file
        self.documents = (line.lower().split() for line in codecs.open(corpusName, mode='r', encoding='utf-8', errors='ignore'))

        # Create Dictionary from documents
        self.dictionary = corpora.Dictionary(line.lower().split() for line in codecs.open(corpusName, mode='r', encoding='utf-8', errors='ignore'))

        # Filter out the keywords that are only in the corpus once
        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)

        # This removes gaps after removing tokens
        self.dictionary.compactify()

        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.documents]
        # self.corpus = [self.dictionary.doc2bow(text) for text in texts]
   
    def getDictionary(self):
        return self.dictionary

    def getCorpus(self):
        return self.corpus

    def saveDic(self):
        self.dictionary.save('savedDictionary.dict')

    def saveCorpusMM(self):
        corpora.MmCorpus.serialize('savedCorpus.mm', self.corpus)

    def saveCorpusLDA(self):
        corpora.BleiCorpus.serialize('savedCorpus.lda-c', self.corpus)



# #
######
