# !/usr/bin/python

import codecs
from time import time

from gensim import corpora, models, similarities, logging


class GenSimModel:

    def __init__(self, path, corpusName):
        ''' This function creates a GenSim corpus and dictionary based on the
        texts kept in file '''
        # Get documents out of mycorpus.txt file
        self.documents = (line.lower().split() for line in codecs.open(
            corpusName + ".txt", mode='r', encoding='utf-8', errors='ignore'))

        # Create Dictionary from documents
        self.dictionary = corpora.Dictionary(line.lower().split() for line in
                                             codecs.open(corpusName + ".txt",
                                                         mode='r',
                                                         encoding='utf-8',
                                                         errors='ignore'))

        # Filter out the keywords that are only in the corpus once
        once_ids = [tokenid for tokenid,
                    docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)

        # This removes gaps after removing tokens
        self.dictionary.compactify()

        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.documents]

        # Create TF-IDF
        t0 = time()
        print "Creating GenSim TF-IDF Model and Index"
        self.tfidfModel = models.TfidfModel(self.corpus)
        print("Done in %0.3fs." % (time() - t0))
        tempCorpus = self.tfidfModel[self.corpus]
        # Create Index
        self.tfidfIndex = similarities.MatrixSimilarity(tempCorpus)
        print("Done in %0.3fs." % (time() - t0))

        # Create LSA
        t0 = time()
        print "Creating GenSim LSA Model and Index"
        self.lsaModel = models.LsiModel(
            self.corpus, id2word=self.dictionary, num_topics=300)
        tempCorpus = self.lsaModel[self.corpus]
        # Create Index
        self.lsaIndex = similarities.MatrixSimilarity(tempCorpus)
        print("Done in %0.3fs." % (time() - t0))

        # Create LDA
        t0 = time()
        print "Creating GenSim LDA Model and Index"
        self.ldaModel = models.LdaModel(
            self.corpus, id2word=self.dictionary, num_topics=300,
            update_every=1, chunksize=2000, passes=5)
        tempCorpus = self.ldaModel[self.corpus]
        # Create Index
        self.ldaIndex = similarities.MatrixSimilarity(tempCorpus)
        print("Done in %0.3fs." % (time() - t0))

    def getCorpus(self):
        return self.corpus

    def getDictionary(self):
        return self.dictionary

    def getTfidf(self):
        return self.tfidfModel

    def getLsa(self):
        return self.lsaModel

    def getLda(self):
        return self.ldaModel

    def getTfidfIndex(self):
        return self.tfidfIndex

    def getLsaIndex(self):
        return self.lsaIndex

    def getLdaIndex(self):
        return self.ldaIndex
