#!/usr/bin/env python
'''
Main program that runs to process email, create dictionaries and corpuses and
checks similarity matching
'''

from Message import Message
import codecs
import os
from time import time

from gensim import models, similarities, logging
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition.nmf import NMF
from sklearn.decomposition.truncated_svd import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import Normalizer

from MyCorpus import MyCorpus


def main():

    path = ["/Users/zschiller/Desktop/Clinton/",
            "/Users/zschiller/Desktop/20News/",
            "/Users/zschiller/Desktop/WorkEmails/",
            "/Users/zschiller/Desktop/PersonalEmails/"]
    corpusName = [
        "ClintonCorpus", "20NewsCorpus", "ZackWorkCorpus", "ZackCorpus"]
    # messages = createKeywordText(path, corpusName)

    pick = 3
    new = Message('lastEmail.txt')
    l, p = sciKitCheck(path[pick], corpusName[pick], "lda", new)
    # l, p = genSimCheck(path[pick], corpusName[pick], "lda", new)
    print l.getBody()
    print "Percentage = ", p


def sciKitCheck(path, corpusName, modelToUse, query):
    ''' Uses the SciKit-Learn tool for corpus creation and similarity check '''
    documents = (line.lower().split() for line in codecs.open(
        corpusName + ".txt", mode='r', encoding='utf-8', errors='ignore'))
    corpus = [' '.join(i) for i in documents]

    # Add the query to end of the corpus
    corpus.append(' '.join(query.getTokens()))

    # Determine model to use
    if modelToUse == "tfidf":
        model = TfidfVectorizer().fit_transform(corpus)
    elif modelToUse == "lsa":
        print "Creating SciKit LSA Model"
        t0 = time()
        tfidf = TfidfVectorizer().fit_transform(corpus)
        lsa = TruncatedSVD(n_components=300)
        model = lsa.fit_transform(tfidf)
        model = Normalizer(copy=False).fit_transform(model)
        print("Done in %0.3fs." % (time() - t0))
    elif modelToUse == "lda":
        n_samples = 2000
        n_features = 1000
        n_topics = 300
        # Use tf (raw term count) features for LDA.
        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_features=n_features)
        t0 = time()
        tf = tf_vectorizer.fit_transform(corpus)
        print("Done in %0.3fs." % (time() - t0))

        print("Fitting LDA models with tf f, n_samples=%d and n_features=%d..."
              % (n_samples, n_features))
        lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        t0 = time()
        model = lda.fit_transform(tf)
        model = Normalizer(copy=False).fit_transform(model)
        print("Done in %0.3fs." % (time() - t0))
    else:
        return None, None

    query = model[-1]
    # print query  # print query vector
    cosine_similarities = linear_kernel(query, model).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    print related_docs_indices
    sims = cosine_similarities[related_docs_indices]
    print sims
    # old = getMatch(33, path, corpusName)
    if sims[1] > 0.10:
        # Check highest value match
        matchLocation = related_docs_indices[1]
        return getMatch(matchLocation, path, corpusName), sims[1]
    else:
        return None, sims[1]


def genSimCheck(path, corpusName, modelToUse, query):
    ''' Uses the GenSim tool for corpus creation and similarity check '''

    # Uncomment to enable GenSim logging
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
    #    level=logging.INFO)
    # Create corpus based on topic model
    dic, corpus = createCorpus(corpusName)
    if modelToUse == "tfidf":
        model = models.TfidfModel(corpus)
    elif modelToUse == "lsa":
        model = models.LsiModel(corpus, id2word=dic, num_topics=300)
    elif modelToUse == "lda":
        model = models.LdaModel(corpus, id2word=dic, num_topics=300)
    else:
        return None, None
    t0 = time()
    print "Creating GenSim Corpus"
    corpus = model[corpus]
    print("Done in %0.3fs." % (time() - t0))
    # Create Index
    index = similarities.MatrixSimilarity(corpus)
    index.save(corpusName + modelToUse + ".index")
    # Similarity check against query
    vec_bow = dic.doc2bow(query.getTokens())
    vectorModel = model[vec_bow]
    sims = index[vectorModel]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print sims[:5]
    if sims[0][1] > 0.10:
        # Check highest value match
        matchLocation = sims[0][0]
        return getMatch(matchLocation, path, corpusName), sims[0][1]
    else:
        return None, sims[0][1]


def createCorpus(corpusName):
    ''' This function creates a GenSim corpus and dictionary
    based on the texts kept in file '''
    corpus_saved = MyCorpus(corpusName)
    corpus_saved.saveDic()
    # corpus_saved.saveCorpusLDA()
    dic = corpus_saved.getDictionary()
    corpus = corpus_saved.getCorpus()
    return (dic, corpus)


def getMatch(matchLocation, path, corpusName):
    ''' This function returns the top match from the similarities '''
    fin = open(corpusName + ".index", 'r')
    data = fin.readlines()
    matchName = data[matchLocation]
    fin.close()
    match = Message(path + matchName.strip())
    return match


def createKeywordText(path, corpusName):
    ''' This function takes in the location of the email files and finds the
    keywords from all of the files and saves the corpus to a text file that
    can be read later '''
    saveCorpus = open(corpusName + ".txt", 'w')
    saveCorpusIndex = open(corpusName + ".index", 'w')
    messages = []
    i = 0
    errors = 0
    l = len(os.listdir(path))

    for filename in os.listdir(path):
        print "Working on", str(filename)
        if errors == 10:
            print "More than 10 errors. Stopping."
            break
        else:
            new = Message(path + filename)
            messages.append(new)
            result = new.getError()
            tokens = ' '.join(map(str, messages[i].getTokens()))
            saveCorpus.write(tokens + '\n')
            saveCorpusIndex.write(filename + '\n')

            if result:
                errors += 1
        i += 1
        print("Completed " + str(i) + " of " + str(l) + '\n')
    saveCorpus.close()
    saveCorpusIndex.close()
    print "Errors creating keyword text = " + str(errors)
    return messages


def getInfo():
    ''' Get initial information from the user about haivng a .mbox
    or where the email files are stored. Then runs the setup process
    finally returning the list of locations where the emails are '''
    print "This program tells you which emails are similar to one another."
    mbox = 'i'
    while (mbox == 'i'):
        mbox = raw_input(("Do you have a .mbox archive of your email to use? "
                          "(y/n/i=moreinfo): "))
        if mbox == 'y':
            fileLoc = raw_input(("Please enter the location and name of your "
                                 ".mbox file (ex: /users/you/Downlods/myEmails"
                                 ".mbox): "))
            locToSave = raw_input(("Please enter the location that you "
                                   "would like to save these emails "
                                   "(ex: /users/you/Documents/myEmails/): "))
            cont = raw_input(("Are you sure you want to use your .mbox? This "
                              "will split the archive into individual email "
                              "files. Careful as this does make a lot of files"
                              " (y/n): "))
            if cont == 'y':
                listEmails = splitEmails(fileLoc, locToSave)
                return listEmails
        elif mbox == 'i':
            print ("You can export your email from most common email "
                   "clients, including gmail, to an archived .mbox file. "
                   "This program can read that to build your archive to "
                   "search through!")
    numEmails = raw_input("Please input the number of emails you have: ")
    fileLoc = raw_input(("Please enter the location of the emails you would "
                         "like to add to the archive database: "))
    fileNames = raw_input(("Please enter the name of the files (ex: "
                           "if files are email0.txt, email1.txt, etc. please "
                           "enter email.txt): "))
    dot = fileNames.index('.')
    listEmails = []
    for i in range(int(numEmails)):
        print "checking " + str(i)
        name = fileNames[:dot] + str(i)
        listEmails.append(fileLoc + fileNames[:dot] + str(i) + fileNames[dot:])
    return listEmails


def splitEmails(filename, locToSave):
    ''' Split .mbox into individual files.
    Careful as this does make a lot of files. '''
    fin = open(filename, 'r')
    data = fin.readlines()
    listEmails = []
    start = True
    for line in data:
        if start:
            name = locToSave + 'email0.txt'
            listEmails.append(name)
            fout = open(name, 'w')
            count = 0
            start = False
        elif (line[:5] == "From "):
            count = count + 1
            fout.close()
            name = locToSave + 'email' + str(count) + '.txt'
            listEmails.append(name)
            fout = open(name, 'w')
        fout.write(line)
    fout.close()
    fin.close()
    print "Created " + str(count) + " files from emails."
    return listEmails


def splitMultiMbox(path, locToSave):
    ''' Funtion to split multiple .mbox files up into individual files '''
    count = 0
    i = 0
    l = len(os.listdir(path))
    for filename in os.listdir(path):
        print "Working on", str(filename)
        if filename == ".DS_Store":
            pass
        else:
            fin = open(path + filename, 'r')
            data = fin.readlines()
            start = True
            for line in data:
                if start:
                    name = locToSave + 'email' + str(count) + '.txt'
                    fout = open(name, 'w')
                    start = False
                elif (line[:5] == "From "):
                    count = count + 1
                    fout.close()
                    name = locToSave + 'email' + str(count) + '.txt'
                    fout = open(name, 'w')
                fout.write(line)
            fout.close()
            fin.close()
            print "Created " + str(count) + " files from emails."
        i += 1
        print("Completed " + str(i) + " of " + str(l) + '\n')
    return True


def testMessages(msg):
    new = [Message(msg)]
    for i in range(len(new)):
        print "----------------------------------------------------"
        print "TO--------------------------------------------------"
        print new[i].getToAddress()
        print "FROM------------------------------------------------"
        print new[i].getFromAddress()
        print "DATE------------------------------------------------"
        print new[i].getDate()
        print "SUBJECT---------------------------------------------"
        print new[i].getSubject()
        print "BODY------------------------------------------------"
        print new[i].getBody()
        print "TOKENS----------------------------------------------"
        print new[i].getTokens()


if __name__ == '__main__':
    # getInfo()
    main()
