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
    fn = "0.txt"
    messages = Message(fn)
    print messages.getBody()

def readEmail():
    fp = open("0.txt", 'r')
    msg = email.message_from_file(fp)
    fp.close()
    for part in msg.walk():
        #print "-------------------"
        #print part.get_content_type()
        if part.get_content_type() == "text/plain":
            body = part.get_payload() # prints the raw text
            print body
    headers = Parser().parse(open("0.txt", 'r'))
    print 'To: %s' % headers['to']
    print 'From: %s' % headers['from']
    print 'Subject: %s' % headers['subject']
    #print 'Message: %s' % headers['body']
    #sentence = """This is a test sentence to see if it can be parsed simply."""
    #tokens = nltk.word_tokenize(sentence)
    #print tokens

## Run the main program
if __name__ == '__main__':
    main()
    #readEmail()

##
######
