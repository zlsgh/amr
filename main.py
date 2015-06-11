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
from math import *
#import MySQLdb
import nltk
import email
from email.parser import Parser
from Message import Message

## Main program
def main():
    #fn = "0.txt"
    fn = "/users/zschiller/desktop/myEmails/email1.txt"
    messages = Message(fn)
    print messages.getBody()

    #tokens = nltk.word_tokenize(messages.getBody())
    print messages.getTokens()

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


## Run the main program
if __name__ == '__main__':
    #getInfo()
    main()
##
######
