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
import nltk
import email
from email.parser import Parser

## Main program
def main():
    fp = open("0.txt")
    msg = email.message_from_file(fp)
    fp.close()
    for part in msg.walk():
        print part
    

    #headers = Parser().parse(open("0.txt", 'r'))
    #print 'To: %s' % headers['to']
    #print 'From: %s' % headers['from']
    #print 'Subject: %s' % headers['subject']
    #print 'Message: %s' % headers['body']
    sentence = """This is a test sentence to see if it can be parsed simply."""
    tokens = nltk.word_tokenize(sentence)
    print tokens

## Run the main program
if __name__ == '__main__':
    main()

##
######
