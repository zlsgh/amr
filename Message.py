# !/usr/bin/python

'''
This is the Message Class which uses the NLTK and Email
libraries to create a message for an email with
important data extracted so that it can be recalled
'''
import email
from email.parser import Parser
import string

import nltk


class Message:
    ''' Message class for each message in user database '''

    def __init__(self, fileLocation):
        ''' Gets file location and creates Message '''
        self.fileLocation = fileLocation
        self.error = False
        self.readEmail()
        # print "Created message"

    def readEmail(self):
        ''' Walks through the email pulling out important features '''
        hasBody = False
        fp = open(self.fileLocation, 'U')
        msg = email.message_from_file(fp)
        fp.close()
        headers = Parser().parse(open(self.fileLocation, 'U'))
        self.toAddress = headers['to']
        # print self.toAddress
        if self.toAddress is not None:
            if "'" in self.toAddress:
                try:
                    addressParts = self.toAddress.split("'")
                    self.toAddress = addressParts[1]
                except:
                    print "Error with To Address"
                    self.error = True
        else:
            self.toAddress = ""
        self.fromAddress = headers['from']
        if self.fromAddress is None:
            self.fromAddress = ""
        self.subject = headers['subject']
        if self.subject is None:
            self.subject = ""
        self.date = headers['date']
        if self.date is None:
            self.date = headers['sent']
        for part in msg.walk():
            # print "-------------------"
            # print part.get_content_type()
            if part.get_content_type() == "text/plain":
                self.body = part.get_payload()  # prints the raw text
                self.originalBody = self.body  # Save original with signature
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
        if not hasBody:
            self.body = ""
            self.findTokens(False)

    def findTokens(self, encode):
        ''' Uses the Natural Language Toolkit to turn words into tokens '''
        stopwords = nltk.corpus.stopwords.words('english')
        addedStopWords = [u'http', 'http', u'https', 'https', u're', 're',
                          u'sent', 'sent', u'to', 'to', u'from', 'from',
                          u'subject', 'subject', 'original',
                          u'original', u'message', 'message', 'i', u'i',
                          '-from', '--from', u'-from', u'--from', '-original',
                          '--original', u'-origina', u'--original']
        punctuations = list(string.punctuation)
        if self.subject is None or self.toAddress is None:
            tempBody = self.body
        else:
            tempBody = self.body + self.toAddress + '\n' + self.subject
        if encode:
            # 'utf-8', errors='ignore')
            tempBody = tempBody.decode('ascii', errors='ignore')
        # print tempBody
        tempTokens = nltk.word_tokenize(tempBody)
        tempTokens = [w.lower() for w in tempTokens if (
            w not in punctuations and len(w) < 50)]
        tempTokens = [w.lower() for w in tempTokens if w not in addedStopWords]
        # print tempTokens
        self.tokens = [w.lower() for w in tempTokens if w not in stopwords]

    def stripSignature(self):
        ''' Removes the signatures and old messages from the email '''
        signature = False
        # possibleSig = False
        # possibleSigDelete = 0
        parts = self.body.split('\n')
        newBody = ""
        for i in range(len(parts)):
            if (parts[i] == '-- ' or
                    parts[i] == '--' or
                    parts[i] == '-----original message-----' or
                    parts[i] == '----- original message -----' or
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
            if not signature:
                newBody = newBody + str(parts[i]) + "\n"
        self.body = newBody

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

    def getOriginalBody(self):
        return self.originalBody

    def getBody(self):
        return self.body

    def getKeywords(self):
        return self.keywords

    def getTokens(self):
        return self.tokens

    def getError(self):
        return self.error
