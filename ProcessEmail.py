#!/usr/bin/env python
'''
This program is designed to run constantly. Receiving emails, adding them to
the models and sending a response email out.
'''

from Message import Message
import email
import getpass
import imaplib
import smtplib
import time
import warnings

import main


class ProcessEmail:

    def __init__(self, path=None, corpusName=None):
        self.login()
        self.path = path
        # self.path = "/Users/zschiller/Desktop/Clinton/"

        self.corpusName = corpusName
        # self.corpusName = "ClintonCorpus"
        run = True
        last_email_id = 0
        self.models = None
        while run:
            warnings.filterwarnings("ignore")
            # print self.mail.list()
            # Out: list of "folders" aka labels in gmail.
            self.mail.select("inbox")  # connect to inbox.
            result, data = self.mail.search(None, "ALL")

            ids = data[0]  # data is a list.
            id_list = ids.split()  # ids is a space separated string
            latest_email_id = id_list[-1]  # get the latest

            result, data = self.mail.fetch(latest_email_id, "(RFC822)")
            msg = email.message_from_string(data[0][1])
            msgSubject = msg['subject']
            msgFrom = msg['from']
            if ((self.user not in msgFrom) and
                    ("AMR Response:" not in msgSubject) and
                    (last_email_id != latest_email_id)):
                last_email_id = latest_email_id
                # fetch the email body (RFC822) for the given ID
                msg = email.message_from_string(data[0][1])
                fout = open('lastEmail.txt', 'w')
                fout.write(str(msg))
                fout.close()
                replied = self.createResponse()
                if replied:
                    print ("The time is " + str(time.strftime("%I:%M:%S")) +
                           ". AMR response created and sent.")
                else:
                    print ("The time is " + str(time.strftime("%I:%M:%S")) +
                           ". AMR match percentage is too low to send.")
            else:
                print ("The time is " + str(time.strftime("%I:%M:%S")) +
                       ". No new mail. Will check again in 30 seconds.")
            time.sleep(30)

    def send(self, message, subject):
        server = 'smtp.gmail.com'

        recipient = self.user
        sender = self.user

        newMessage = "To: " + recipient + "\n" + "From: " + \
            sender + "\n" + "Subject: " + subject + "\n" + message

        session = smtplib.SMTP(server)
        session.ehlo()
        session.starttls()

        session.login(self.user, self.pswd)
        session.sendmail(sender, recipient, newMessage)

    def login(self):
        ''' Get login info from user '''
        # self.user = "zacheryschiller@gmail.com"
        self.user = raw_input("Please enter your email address: ")
        self.pswd = getpass.getpass("Please enter your password: ")
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.user, self.pswd)

    def createResponse(self):
        ''' Get response from similarity check. If good, send reply '''
        new = Message('lastEmail.txt')
        # print "Incoming Mail: " + '\n' + new.getBody()
        subject = new.getSubject()
        subject = "AMR Response: " + subject
        # print new.getBody()
        tool = 's'  # Chose g for Gensim or s for Scikit Learn
        modelToUse = "lda"
        if tool == 'g':
            match, accuracy, self.models = main.emailCheck(
                self.path, self.corpusName, modelToUse, "gensim",
                new, self.models)
        elif tool == 's':
            match, accuracy, self.models = main.emailCheck(
                self.path, self.corpusName, modelToUse, "scikit",
                new, self.models)
        else:
            match, accuracy = None, None

        if match is not None:
            # print "Outgoing Mail: " + '\n' + match.getBody()
            reply = self.buildReply(match, accuracy)
            # print reply
            self.send(reply, subject)
            return True
        return False

    def buildReply(self, match, accuracy):
        ''' Create text of reply email '''
        if match.getDate() is None:
            date = ""
        else:
            date = match.getDate()
        if match.getSubject() is None:
            subj = ""
        else:
            subj = match.getSubject()
        if match.getToAddress() is None:
            toAddr = ""
        else:
            toAddr = match.getToAddress()
        if match.getFromAddress() is None:
            fromAddr = ""
        else:
            fromAddr = match.getFromAddress()
        if match.getOriginalBody() is None:
            origBody = ""
        else:
            origBody = match.getOriginalBody()
        reply = ("This is an AMR response! The accuracy of this match is " +
                 str(accuracy) + '%\n\n' +
                 "Date: " + date + '\n' +
                 "Subject: " + subj + '\n' +
                 "To: " + toAddr + '\n' +
                 "From: " + fromAddr + '\n\n' +
                 origBody)
        # print match.getTokens()
        return reply


if __name__ == '__main__':
    path = raw_input("Please enter the location that you saved your emails to "
                     "(ex: /users/you/Documents/myEmails/): ")
    corpus = raw_input(
        "Please enter what the name of your corpus text (i.e. myEmails): ")
    proc = ProcessEmail(path, corpus)
