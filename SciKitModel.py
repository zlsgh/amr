# !/usr/bin/python

import codecs
from time import time

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition.truncated_svd import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import Normalizer


class SciKitModel:

    def __init__(self, path, corpusName, query=None):
        self.query = query
        documents = (line.lower().split() for line in codecs.open(
            corpusName + ".txt", mode='r', encoding='utf-8', errors='ignore'))
        self.corpus = [' '.join(i) for i in documents]
        if self.query is not None:
            self.corpus.append(' '.join(query.getTokens()))

        # Make models
        t0 = time()
        print "Creating SciKit TF-IDF Model"
        self.tfidfModel = TfidfVectorizer().fit_transform(self.corpus)
        print("Done in %0.3fs." % (time() - t0))

        print "Creating SciKit LSA Model"
        t0 = time()
        lsa = TruncatedSVD(n_components=300)
        self.lsaModel = lsa.fit_transform(self.tfidfModel)
        self.lsaModel = Normalizer(copy=False).fit_transform(self.lsaModel)
        print("Done in %0.3fs." % (time() - t0))

        print "Creating SciKit LDA Model"
        # Use tf (raw term count) features for LDA.
        print("Extracting tf features for LDA")
        tf_vectorizer = CountVectorizer(max_features=1000)
        t0 = time()
        tf = tf_vectorizer.fit_transform(self.corpus)
        print("Done in %0.3fs." % (time() - t0))
        print("Fitting LDA model")
        lda = LatentDirichletAllocation(n_topics=300, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        t0 = time()
        self.ldaModel = lda.fit_transform(tf)
        self.ldaModel = Normalizer(copy=False).fit_transform(self.ldaModel)
        print("Done in %0.3fs." % (time() - t0))

    def getCorpus(self):
        return self.corpus

    def getTfidf(self):
        return self.tfidfModel

    def getLsa(self):
        return self.lsaModel

    def getLda(self):
        return self.ldaModel
