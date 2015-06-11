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


## Main program
class Message:
    """ Message class for each message in user database """
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation
        self.readEmail()
        print "Created message"

    def readEmail(self):
        fp = open(self.fileLocation, 'U')
        msg = email.message_from_file(fp)
        fp.close()
        for part in msg.walk():
            #print "-------------------"
            print part.get_content_type()
            if part.get_content_type() == "text/plain":
                self.body = part.get_payload() # prints the raw text
                self.stripSignature()
                self.findTokens()
        headers = Parser().parse(open(self.fileLocation, 'U'))
        self.toAddress = headers['to']
        self.fromAddress = headers['from']
        self.subject = headers['subject']
    
    def findTokens(self):
        stopwords = nltk.corpus.stopwords.words('english')
        tempTokens = nltk.word_tokenize(self.body)
        self.tokens = [w for w in tempTokens if not w in stopwords]

    def stripSignature(self):
        signature = False
        parts = self.body.split('\n')
        #print parts
        newBody = ""
        for i in range(len(parts)):
            if (parts[i] == '-- ' or 
                    parts[i] == '--' or 
                    parts[i] == '-----original message-----' or 
                    parts[i] == '________________________________'or
                    parts[i] == 'sent from my iphone' or 
                    parts[i] == 'sent from my blackberry'):
                #print "SIG!!!!!"
                signature = True
            if signature == False:
                newBody = newBody+str(parts[i])+"\n"
        self.body = newBody
        #print "-----"
        #print self.body
        #print "-----"
 
    def getFileLocation(self):
        return self.fileLocation

    def getToAddress(self):
        return self.toAddress

    def getFromAddress(self):
        return self.fromAddress

    def getSubject(self):
        return self.subject

    def getBody(self):
        return self.body

    def getKeywords(self):
        return self.keywords

    def getTokens(self):
        return self.tokens

## Run the main program
#if __name__ == '__main__':
#    main()

##
######
