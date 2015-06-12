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


## Main program
class Message:
    """ Message class for each message in user database """
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation
        self.readEmail()
        #print "Created message"

    def readEmail(self):
        hasBody = False
        fp = open(self.fileLocation, 'U')
        msg = email.message_from_file(fp)
        fp.close()
        headers = Parser().parse(open(self.fileLocation, 'U'))
        self.toAddress = headers['to']
        self.fromAddress = headers['from']
        self.subject = headers['subject']
        for part in msg.walk():
            #print "-------------------"
            #print part.get_content_type()
            if part.get_content_type() == "text/plain":
                self.body = part.get_payload() # prints the raw text
                self.stripSignature()
                self.findTokens()
                hasBody = True
        if hasBody == False:
            self.body = ""
            self.findTokens()
    
    def findTokens(self):
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append(u'http')
        stopwords.append(u'https')
        punctuations = list(string.punctuation)
        if self.subject is None or self.toAddress is None:
             tempBody = self.body
        else:
            tempBody = self.body + self.toAddress+ '\n' + self.subject          
        #print tempBody
        tempTokens = nltk.word_tokenize(tempBody)
        tempTokens = [w for w in tempTokens if (not w in punctuations and len(w)<50)]
        self.tokens = [w.lower() for w in tempTokens if not w in stopwords]

    def stripSignature(self):
        signature = False
        #possibleSig = False
        #possibleSigDelete = 0
        parts = self.body.split('\n')
        #print parts
        newBody = ""
        for i in range(len(parts)):
            if (parts[i] == '-- ' or 
                    parts[i] == '--' or 
                    parts[i] == '-----original message-----' or 
                    parts[i] == '________________________________'or
                    parts[i] == 'sent from my iphone' or 
                    parts[i] == 'sent from my blackberry' or
                    parts[i].startswith('> ') or
                    parts[i].startswith('On Mon,') or 
                    parts[i].startswith('On Tue,') or 
                    parts[i].startswith('On Wed,') or 
                    parts[i].startswith('On Thu,') or 
                    parts[i].startswith('On Fri,') or 
                    parts[i].startswith('On Sat,') or 
                    parts[i].startswith('On Sun,')):
                #print "SIG!!!!!"
                signature = True
            elif parts[i].startswith('On ') and parts[i].endswith('wrote:'):
                signature = True
            #if parts[i].startswith('On '):
            #    possibleSig = True
            #    possibleSigDelete = 1
            #elif (parts[i].endswith('wrote:') and possibleSig == True):
            #    signature = True
            #    print "LINE!!!" + str(possibleSigDelete)
            #elif possibleSig == True:
            #    possibleSigDelete += 1
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
