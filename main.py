# !/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

################################  Information ################################
##
## Title: Auto Mail Reply (amr) 
##
## Author: Zachery Schiller
## Email: zacheryschiller@gmail.com
## Github: https://github.com/zacheryschiller/
## 
##############################################################################
 
###### 
## 

## Imports
## These are the imports needed to run the program, including GenSim
from math import *
import nltk
import email
from email.parser import Parser
from Message import Message
from MyCorpus import MyCorpus
from gensim import corpora, models, similarities

## Main program
def main():

    #Good Stuff
    # Uncomment to create keyword text
    #createKeywordText("/users/zschiller/desktop/myEmails/",17724)
    # uncomment to load from mycorpus.txt file
    #corpus_saved = MyCorpus()
    #corpus_saved.saveDic()
    #corpus_saved.saveCorpus()
    #dic = corpus_saved.getDictionary()
    #corpus = corpus_saved.getCorpus()

    corpus = corpora.MmCorpus('savedCorpus.mm')
    dic = corpora.Dictionary.load("savedDictionary.dict")

    lsi = models.LsiModel(corpus, id2word=dic, num_topics=2)
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('saved.index')
    index = similarities.MatrixSimilarity.load('saved.index')

    newEmail = Message("0.txt")
    doc = newEmail.getTokens()
    print doc
    vec_bow = dic.doc2bow(doc)
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for i in range(10):
        print sims[i]

    #msg = Message("/users/zschiller/desktop/trash/myEmails/email2287.txt")
    #print msg.getBody()


    #corp = corpus_saved.getCorpus()
    #print corp
    #dic.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)
    #print keywords
    #dictionary = corpora.Dictionary(keywords)
    #corpus = [dictionary.doc2bow(keyword) for keyword in keywords]
    #print dictionary.token2id
    #print corpus

## This function takes in the location of the email files
## and finds the keywords from all of the fiels and saves
## the corpus to a text file that can eb read later
def createKeywordText(fileLoc, numFiles):
    saveCorpus = open('mycorpus.txt','w')
    messages = []
    keywords = []
    numErrors = 0
    for i in range(numFiles):
        fn = fileLoc + "email" + str(i) + ".txt"
        #print fn
        messages.append(Message(fn))
        if messages[i].getError():
            numErrors +=1
        l = ' '.join(map(str,messages[i].getTokens()))
        saveCorpus.write(l+'\n')
        print "Done " + str(i) + " of " + str(numFiles-1)
        #keywords.append(messages[i].getTokens())
        #print "______________BODY______________"
        #print messages[0].getBody()
        #print  "______________Keywords______________"
        #print messages[i].getTokens()
        #print l
        #fout = "/users/zschiller/desktop/myEmailsTokens/email" + str(i) + "_tokens.txt"
        #w = open(fout,'w')
        #w.write(l)
        #w.close()
    saveCorpus.close()
    print "Created corpus file with only " + str(numErrors) + " errors!"

## Get initial information from the user about haivng a .mbox
## or where the email files are stored. Then runs the setup process
## finally returning the list of locations where the emails are
def getInfo():
    print "This program tells you which emails are similar to one another."
    mbox = 'i'
    while (mbox == 'i'):
        mbox = raw_input(("Do you have a .mbox archive of your email to use? "
        "(y/n/i=moreinfo): "))
        if mbox == 'y':
            fileLoc = raw_input(("Please enter the location and name of your "
            ".mbox file (ex: /users/you/Downlods/myEmails.mbox): "))
            locToSave =  raw_input(("Please enter the location that you "
            "would like to save these emails "
            "(ex: /users/you/Documents/myEmails/): "))
            cont = raw_input(("Are you sure you want to use your .mbox? This "
            "will split the archive into individual email files. Careful "
            "as this does make a lot of files... (y/n): "))
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
    "if files are email0.txt, email1.txt, etc. please enter email.txt): ")) 
    dot = fileNames.index('.')
    listEmails = []
    for i in range(int(numEmails)):
        print "checking " + str(i)
        name = fileNames[:dot] + str(i)
        listEmails.append(fileLoc+fileNames[:dot]+str(i)+fileNames[dot:])
    return listEmails

## Split .mbox into individual files
## Careful as this does make a lot of files...
def splitEmails(filename, locToSave):
    fin = open(filename, 'r')
    data = fin.readlines()
    listEmails = []
    start = True
    for line in data:
        if start == True:
            name = locToSave+'email0.txt'
            listEmails.append(name)
            fout = open(name, 'w')
            count = 0
            start = False
        elif (line[:5] == "From "):
            count = count+1
            fout.close()
            name = locToSave+'email'+str(count)+'.txt'
            listEmails.append(name)
            fout = open(name, 'w')
        fout.write(line)
    fout.close()
    fin.close()
    print "Created " + str(count) + " files from emails."
    return listEmails

def compareEmail(newEmailLoc):
    newEmail = Message(newEmailLoc)
    print newEmail.getTokens()

def checkSimilarity(texts, doc):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    vec_bow = dictionary.doc2bow(doc)
    vec_lsi = lsi[vec_bow]

    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sims

## Run the main program
if __name__ == '__main__':
    #getInfo()
    main()
##
######
