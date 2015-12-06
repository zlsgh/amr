#!/usr/bin/env python

'''
NOT PART OF RUNNING AMR
Testing Scikit Learn Python module
'''

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def main():
    twenty = fetch_20newsgroups()
    tfidf = TfidfVectorizer().fit_transform(twenty.data)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    print related_docs_indices
    print cosine_similarities[related_docs_indices]
    # vectorizer = CountVectorizer(min_df=1)
    # corpus = [
    # 'This is the first document.',
    # 'This is the second second document.',
    # 'And the third one.',
    # 'Is this the first document?',
    # ]

    # tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    # tfs = tfidf.fit_transform(token_dict.values())

    train_set = ("The sky is blue.", "The sun is bright.")
    test_set = ("The sun in the sky is bright.",
                "We can see the shining sun, the bright sun.")
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit_transform(train_set)
    print "Vocabulary:", count_vectorizer.vocabulary
    # Vocabulary: {'blue': 0, 'sun': 1, 'bright': 2, 'sky': 3}
    freq_term_matrix = count_vectorizer.transform(test_set)
    print freq_term_matrix.todense()
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(freq_term_matrix)
    print "IDF:", tfidf.idf_
    tf_idf_matrix = tfidf.transform(freq_term_matrix)
    print tf_idf_matrix.todense()

# Run the main program
if __name__ == '__main__':
    main()
