#!/usr/bin/env python
'''
Main program that runs to process email, create dictionaries and corpuses and
checks similarity matching
'''

from Message import Message
import os
from time import time
import warnings

from sklearn.metrics.pairwise import linear_kernel

from GenSimModel import GenSimModel
import ProcessEmail
from SciKitModel import SciKitModel


def main():

    path = ["/Users/zschiller/Desktop/Clinton/",
            "/Users/zschiller/Desktop/20News/",
            "/Users/zschiller/Desktop/WorkEmails/",
            "/Users/zschiller/Desktop/PersonalEmails/"]
    corpusName = [
        "ClintonCorpus", "20NewsCorpus", "ZackWorkCorpus", "ZackCorpus"]

    pick = 3
    warnings.filterwarnings("ignore")

    # Uncomment to create keyword text for an archive
    # print createKeywordText(path[pick], corpusName[pick])

    # Uncomment to check each doc in a dataset against model for comparisons
    # datasetCheck(path[pick], corpusName[pick])

    # Uncomment to check the results of a new email saved as a text file
    # print getMatch(0, path[pick], corpusName[pick]).getFileLocation()
    new = Message('lastEmail.txt')
    multiCheck(path[pick], corpusName[pick], new)  # Results printed to file.


def emailCheck(path, corpusName, modelToUse, tool, query, models):
    ''' This function is used for replying to a specific email '''
    if tool == "gensim":
        if models is None:
            gs = GenSimModel(path, corpusName)
            models = gs
        else:
            gs = models

        if modelToUse == "tfidf":
            result = genSimCheck(
                gs.getDictionary(), gs.getTfidfIndex(), gs.getTfidf(), query)
        elif modelToUse == "lsa":
            result = genSimCheck(
                gs.getDictionary(), gs.getLsaIndex(), gs.getLsa(), query)
        elif modelToUse == "lda":
            result = genSimCheck(
                gs.getDictionary(), gs.getLdaIndex(), gs.getLda(), query)
    elif tool == "scikit":
        if models is None:
            sk = SciKitModel(path, corpusName, query)
            models = sk
        else:
            sk = SciKitModel(path, corpusName, query)

        if modelToUse == "tfidf":
            result = sciKitCheck(sk.getTfidf())
        elif modelToUse == "lsa":
            result = sciKitCheck(sk.getLsa())
        elif modelToUse == "lda":
            result = sciKitCheck(sk.getLda())

    return getMatch(result[0][0], path, corpusName), result[0][1], models


def multiCheck(path, corpusName, new):
    ''' Check all tools and models for matching INCOMING MAIL'''
    t1 = time()
    resultFile = open('results.txt', 'w')

    sk = SciKitModel(path, corpusName, new)
    gs = GenSimModel(path, corpusName)

    resultFile.write("Sci Kit TFIDF: \n")
    matches = sciKitCheck(sk.getTfidf())
    resultFile.write(str(matches) + '\n\n')
    resultFile.write("Sci Kit LSA: \n")
    matches = sciKitCheck(sk.getLsa())
    resultFile.write(str(matches) + '\n\n')
    resultFile.write("Sci Kit LDA: \n")
    matches = sciKitCheck(sk.getLda())
    resultFile.write(str(matches) + '\n\n')
    resultFile.write("Gen Sim TFIDF: \n")
    matches = genSimCheck(
        gs.getDictionary(), gs.getTfidfIndex(), gs.getTfidf(), new)
    resultFile.write(str(matches) + '\n\n')
    resultFile.write("Gen Sim LSA: \n")
    matches = genSimCheck(
        gs.getDictionary(), gs.getLsaIndex(), gs.getLsa(), new)
    resultFile.write(str(matches) + '\n\n')
    resultFile.write("Gen Sim LDA: \n")
    matches = genSimCheck(
        gs.getDictionary(), gs.getLdaIndex(), gs.getLda(), new)
    resultFile.write(str(matches))
    resultFile.close()
    print("All tools and models checked in %0.3fs." % (time() - t1))


def datasetCheck(path, corpusName):
    ''' Go through dataset comparing all documents to corpus '''
    print "Setting up all models and tools..."
    t1 = time()
    t0 = time()
    sk = SciKitModel(path, corpusName)
    gs = GenSimModel(path, corpusName)
    print("Tools and models set up in %0.3fs." % (time() - t1))
    resultFile = open(corpusName + 'Results.csv', 'w')
    resultFile.write(
        "Filename,Tool,Model,Result 1,Result 1 Sim,Result 2,Result 2 Sim," +
        "Result 3,Result 3 Sim,Result 4,Result 4 Sim,Result 5,Result 5 Sim\n")
    i = 0
    l = len(os.listdir(path))
    for filename in os.listdir(path):
        print "Working on", str(filename)
        new = Message(path + filename)
        resultFile.write(filename + ",SciKit," + "tfidf")
        res = sciKitCheck(sk.getTfidf(), i)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')

        resultFile.write(filename + ",SciKit," + "lsa")
        res = sciKitCheck(sk.getLsa(), i)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')

        resultFile.write(filename + ",SciKit," + "lda")
        res = sciKitCheck(sk.getTfidf(), i)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')

        resultFile.write(filename + ",GenSim," + "tfidf")
        res = genSimCheck(
            gs.getDictionary(), gs.getTfidfIndex(), gs.getTfidf(), new)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')

        resultFile.write(filename + ",GenSim," + "lsa")
        res = genSimCheck(
            gs.getDictionary(), gs.getLsaIndex(), gs.getLsa(), new)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')

        resultFile.write(filename + ",GenSim," + "lda")
        res = genSimCheck(
            gs.getDictionary(), gs.getLdaIndex(), gs.getLda(), new)
        for j in range(len(res)):
            resultFile.write(',' + str(res[j][0]) + ',')
            resultFile.write(str(res[j][1]))
        resultFile.write('\n')
        i += 1
        print("Completed " + str(i) + " of " + str(l) + '\n')
    resultFile.close()
    print("Created .csv of matches for dataset in %0.3fs." % (time() - t0))


def sciKitCheck(model, query=None):
    ''' Uses the SciKit-Learn tool for corpus creation and similarity check '''
    if query is None:
        query = -1
    query = model[query]
    try:
        # This raises a small warning
        cosine_similarities = linear_kernel(query, model).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-7:-1]
        sims = cosine_similarities[related_docs_indices]
        # Format result
        result = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for n in range(1, 6):
            result[n - 1][0] = related_docs_indices[n]
            result[n - 1][1] = round((sims[n] * 100), 1)
        return result
    except:
        return [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]


def genSimCheck(dic, index, model, query):
    ''' Uses the GenSim tool for corpus creation and similarity check '''
    try:
        vec_bow = dic.doc2bow(query.getTokens())
        vectorModel = model[vec_bow]
        sims = index[vectorModel]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # Format result
        result = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for n in range(1, 6):
            result[n - 1][0] = sims[n][0]
            result[n - 1][1] = round((sims[n][1] * 100), 1)
        return result
    except:
        return [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]


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
    return True


def setup():
    ''' Get initial information from the user about haivng a .mbox
    or where the email files are stored. Then runs the setup process
    finally returning the list of locations where the emails are '''
    print ("Welcome to AMR! AMR helps you by automatically sending you reply"
           " suggestions for each of your new emails!")
    mbox = 'i'
    while (mbox == 'i'):
        mbox = raw_input("Do you have a .mbox archive of your email to use? "
                         "(y/n/i=moreinfo): ")
        if mbox == 'y':
            fileLoc = raw_input("Please enter the location and name of your "
                                ".mbox file (ex: /users/you/Downlods/myEmails"
                                ".mbox): ")
            path = raw_input("Please enter the location that you "
                             "would like to save these emails "
                             "(ex: /users/you/Documents/myEmails/): ")
            cont = raw_input("This process will split the archive into "
                             "individual email files. This will make a lot "
                             "of files. (y/n): ")
            if cont == 'y':
                try:
                    splitEmails(fileLoc, path)
                except:
                    print ("There was a problem with the files."
                           " Please try again.")
                    mbox = 'i'
        elif mbox == 'i':
            print ("You can export your email from most common email "
                   "clients, including Gmail, to an archived .mbox file. "
                   "This program can read that to build your archive to "
                   "search through!")
    corpusName = raw_input("Next AMR will build the corpus text based on all"
                           " of your emails. This will take some time as each"
                           " email will be checked. Please enter what you"
                           " would like to name this corpus (i.e. myEmails):")
    print createKeywordText(path, corpusName)
    cont = raw_input("You are all set and ready to run AMR!\n"
                     "Would you like to run AMR now? (y/n): ")
    if cont == 'y':
        ProcessEmail.ProcessEmail(path, corpusName)
    else:
        print ("To start the AMR system later run the ProcessEmail.py program"
               " along with the path to the messages and your corpus name.")


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
    return True


def splitMultiMbox(path, locToSave):
    ''' Function to split multiple .mbox files up into individual files '''
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
    # Uncomment to run AMR for first time to set up models and archives
    setup()

    # Uncomment to run specific tasks such as checking one message only
    # main()
