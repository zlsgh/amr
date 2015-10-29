# !/usr/bin/python

'''
This program is used to convert Secretary Clinton's emails into the standard format for use with the standard AMR project.
'''
import nltk
from nltk.corpus import stopwords
import email
from email.parser import Parser
from Message import Message
import string
import os
import re


def convert(fileLocation):
    fin = open("/Users/zschiller/Desktop/hillary_text/"+fileLocation, 'r')
    data = fin.read()
    fin.close()

    # Formatting for messups in conversion    
    data = data.replace(" From:","\nFrom:")
    data = data.replace(" Sent:","\nSent:")
    data = data.replace(" To:","\nTo:")
    data = data.replace(" Subject:","\nSubject:")
    data = data.replace(" Attachments:","\nAttachments:")
    data = data.replace("06/30/2015","06/30/2015\n")
    data = data.replace("07/31/2015","07/31/2015\n")
    data = data.replace("08/31/2015","08/31/2015\n")
    data = data.replace(" UNCLASSIFIED","\nUNCLASSIFIED")

    data = data.splitlines()
    fout = open(("/Users/zschiller/Desktop/fixed/"+fileLocation), 'w')
    fout.write("Content-Type: text/plain; charset=UTF-8\n")
    for i in range(len(data)):
        # Fix leading space
        data[i] = data[i].lstrip()
        if data[i].strip() == '':
            pass
        elif data[i][0:12] == "UNCLASSIFIED":
            pass
        elif data[i][0:7] == "RELEASE":
            pass
        elif data[i][0:5] == "file:":
            pass
        elif data[i][0:2] == "B5":
            pass
        elif data[i][0:2] == "B6":
            pass
        else:
            fout.write(data[i]+'\n')
    fout.close()


    new = Message("/Users/zschiller/Desktop/fixed/"+fileLocation)
    if new.getError():
        fout2 = open(("/Users/zschiller/Desktop/errors/"+fileLocation), 'w')
    else:
        fout2 = open(("/Users/zschiller/Desktop/fixedMessages/"+fileLocation), 'w')
    if  (new.getToAddress() != None):
        fout2.write( "----------------------------------------------------\n")
        fout2.write( "TO--------------------------------------------------\n")
        fout2.write( new.getToAddress()+'\n')
    if  (new.getFromAddress() != None):
        fout2.write( "FROM------------------------------------------------\n")
        fout2.write( new.getFromAddress()+'\n')
    if  (new.getDate() != None):
        fout2.write( "DATE------------------------------------------------\n")
        fout2.write( new.getDate()+'\n')
    if  (new.getSubject() != None):
        fout2.write( "SUBJECT---------------------------------------------\n")
        fout2.write( new.getSubject()+'\n')
    if  (new.getBody() != None):
        fout2.write( "BODY------------------------------------------------\n")
        fout2.write( new.getBody()+'\n')
    if  (new.getTokens() != None):
        fout2.write( "TOKENS----------------------------------------------\n")
        fout2.write( str(new.getTokens())+'\n')
    fout2.close()
    return new.getError()

path = "/Users/zschiller/Desktop/hillary_text/"
i = 0
j=0
l = len(os.listdir(path))

for filename in os.listdir(path):
    print "Working on", str(filename)
    if filename == ".DS_Store":
        pass
    elif j==10:
        break
    else:
        result = convert(filename)
        if result:
            j += 1
    i += 1
    print("completed "+str(i)+" of "+str(l)+'\n')
print "Errors = " + str(j)
