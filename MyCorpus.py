# !/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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

## Main program
class MyCorpus:
    def __init__(self):
        self.documents = (line.lower().split() for line in open('mycorpus.txt'))
        #for document in self.documents: print document
        self.dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
        #self.corpus = self.dictionary.doc2bow(self.documents)
    
    def getDictionary(self):
        return self.dictionary

    def getCorpus(self):
        return self.corpus

## Run the main program
#if __name__ == '__main__':
#    main()

##
######
