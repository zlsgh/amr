#!/usr/bin/env python
'''
This class is designed to receive emails, add them to database,
and send a response email out.
'''

from Message import Message
import email
import getpass
import imaplib
import smtplib
import time
from main import genSimCheck


class ProcessEmail:

    def __init__(self):
        self.login()
        run = True
        last_email_id = 0
        while run:
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
            if (("zacheryschiller@gmail.com" not in msgFrom) and
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

        recipient = 'zacheryschiller@gmail.com'
        sender = 'zacheryschiller@gmail.com'

        newMessage = "To: " + recipient + "\n" + "From: " + \
            sender + "\n" + "Subject: " + subject + "\n" + message

        session = smtplib.SMTP(server)
        session.ehlo()
        session.starttls()

        session.login(self.user, self.pswd)
        session.sendmail(sender, recipient, newMessage)

    def login(self):
        ''' Get login info from user '''
        self.user = "zacheryschiller@gmail.com"
        # getpass.getuser("Please enter your email address:")
        self.pswd = getpass.getpass("Please enter your password:")
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.user, self.pswd)

    def createResponse(self):
        ''' Get response from similarity check. If good, send reply '''
        new = Message('lastEmail.txt')
        print "Incoming Mail: " + '\n' + new.getBody()
        subject = new.getSubject()
        subject = "AMR Response: " + subject
        print new.getBody()
        reply, accuracy = genSimCheck(
            "/Users/zschiller/Desktop/PersonalEmails/",
            "ZackCorpus", new.getBody())
        if reply is not None:
            print "Outgoing Mail: " + '\n' + reply
            reply = "Accuracy = " + accuracy + '\n' + reply
            self.send(reply, subject)
            return True
        return False

if __name__ == '__main__':
    proc = ProcessEmail()
