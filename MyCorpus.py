# !/usr/bin/python

################################  Information ################################
##
## Title: 
##
## Author: Zachery Schiller
## Email: zacheryschiller@gmail.com
## Github: https://github.com/zacheryschiller/
## 
##############################################################################

###### 
## 

## Imports
from math import *
import nltk
from nltk.corpus import stopwords
import email
from email.parser import Parser
import string
from gensim import corpora, models, similarities

## New instance of corpus gets the documents out of mycorpus.txt file
class MyCorpus:
    def __init__(self):
        # Get documents out of mycorpus.txt file
        self.documents = (line.lower().split() for line in open('mycorpus.txt'))

        # Create Dictionary from documents
        self.dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))

        # Filter out the keywords that are only in the corpus once
        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)

        # This removes gaps after removing tokens
        self.dictionary.compactify()

        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.documents]
        #self.corpus = [self.dictionary.doc2bow(text) for text in texts]
   
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



##
######
