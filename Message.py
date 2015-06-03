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
        fp = open(self.fileLocation, 'r')
        msg = email.message_from_file(fp)
        fp.close()
        for part in msg.walk():
            #print "-------------------"
            #print part.get_content_type()
            if part.get_content_type() == "text/plain":
                self.body = part.get_payload() # prints the raw text
        headers = Parser().parse(open(self.fileLocation, 'r'))
        self.toAddress = headers['to']
        self.fromAddress = headers['from']
        self.subject = headers['subject']

    def stripSignature(self):
#lines that equal '-- \n' (standard email sig delimiter)
#lines that equal '--\n' (people often forget the space in sig delimiter; and this is not that common outside sigs)
#lines that begin with '-----original message-----' (ms outlook default)
#lines that begin with '________________________________' (32 underscores, outlook again)
#lines that begin with 'on ' and end with ' wrote:\n' (os x mail.app default)
#lines that begin with 'from: ' (failsafe four outlook and some other reply formats)
#lines that begin with 'sent from my iphone'
#lines that begin with 'sent from my blackberry'
 
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



## Run the main program
#if __name__ == '__main__':
#    main()

##
######
