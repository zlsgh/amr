# !/usr/bin/python

################################  Information ################################
# #
# # Title: 
# #
# # Author: Zachery Schiller
# # Email: zacheryschiller@gmail.com
# # Github: https://github.com/zacheryschiller/
# # 
##############################################################################

###### 
# # 

# # Imports
import email
from email.parser import Parser
from math import *
import string

import nltk
from nltk.corpus import stopwords


# # Main program
class Message:
    """ Message class for each message in user database """
    def __init__(self, fileLocation):
        self.fileLocation = fileLocation
        self.error = False
        self.readEmail()
        # print "Created message"

    def readEmail(self):
        hasBody = False
        fp = open(self.fileLocation, 'U')
        msg = email.message_from_file(fp)
        fp.close()
        headers = Parser().parse(open(self.fileLocation, 'U'))
        self.toAddress = headers['to']
        # print self.toAddress
        if self.toAddress != None:
            if "'" in self.toAddress:
                try:
                    addressParts = self.toAddress.split("'")
                    self.toAddress = addressParts[1]
                except:
                    print "Error with To Address"
                    self.error = True
        self.fromAddress = headers['from']
        self.subject = headers['subject']
        self.date = headers['date']
        if self.date == None:
            self.date = headers['sent']
        for part in msg.walk():
            # print "-------------------"
            # print part.get_content_type()
            if part.get_content_type() == "text/plain":
                self.body = part.get_payload()  # prints the raw text
                self.stripSignature()
                try:
                    self.findTokens(False)
                except:
                    try:
                        self.findTokens(True)
                    except:
                        print "Error making tokens"
                        self.error = True
                        self.tokens = []
                hasBody = True
        if hasBody == False:
            self.body = ""
            self.findTokens(False)
            
    def findTokens(self, encode):
        stopwords = nltk.corpus.stopwords.words('english')
        addedStopWords = [u'http', 'http', u'https', 'https', u're', 're', u'sent', 'sent', u'to', 'to', u'from', 'from', u'subject', 'subject', 'original', u'original', u'message', 'message', 'i', u'i', '-from', '--from', u'-from', u'--from', '-original', '--original', u'-origina', u'--original']
        punctuations = list(string.punctuation)
        if self.subject is None or self.toAddress is None:
             tempBody = self.body
        else:
            tempBody = self.body + self.toAddress + '\n' + self.subject
        if encode:
            tempBody = tempBody.decode('ascii', errors='ignore')  # 'utf-8', errors='ignore')
        # print tempBody
        tempTokens = nltk.word_tokenize(tempBody)
        tempTokens = [w.lower() for w in tempTokens if (not w in punctuations and len(w) < 50)]
        tempTokens = [w.lower() for w in tempTokens if not w in addedStopWords]
        # print tempTokens
        self.tokens = [w.lower() for w in tempTokens if not w in stopwords]

    def stripSignature(self):
        signature = False
        # possibleSig = False
        # possibleSigDelete = 0
        parts = self.body.split('\n')
        # print parts
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
                # print "SIG!!!!!"
                signature = True
            elif parts[i].startswith('On ') and parts[i].endswith('wrote:'):
                signature = True
            # if parts[i].startswith('On '):
            #    possibleSig = True
            # elif (parts[i].endswith('wrote:') and possibleSig == True):
            #    signature = True
            #    print "LINE!!!" + str(possibleSigDelete)
            # elif possibleSig == True:
            #    possibleSigDelete += 1
            if signature == False:
                newBody = newBody + str(parts[i]) + "\n"
        self.body = newBody
        # print "-----"
        # print self.body
        # print "-----"
 
    def getFileLocation(self):
        return self.fileLocation

    def getToAddress(self):
        return self.toAddress

    def getFromAddress(self):
        return self.fromAddress

    def getSubject(self):
        return self.subject

    def getDate(self):
        return self.date

    def getBody(self):
        return self.body

    def getKeywords(self):
        return self.keywords

    def getTokens(self):
        return self.tokens

    def getError(self):
        return self.error

# # Run the main program
# if __name__ == '__main__':
#    main()

# #
#####
# !/usr/bin/python
