#!/usr/bin/env python
'''
This class is designed to receive emails, add them to database,
and send a response email out.
'''

import smtplib
import imaplib
import getpass
from Message import Message
import email

class ProcessEmail:
	def __init__(self):
		self.login()
		#print self.mail.list()
		# Out: list of "folders" aka labels in gmail.
		self.mail.select("inbox") # connect to inbox.
		result, data = self.mail.search(None, "ALL")

		ids = data[0] # data is a list.
		id_list = ids.split() # ids is a space separated string
		latest_email_id = id_list[-1] # get the latest

		# fetch the email body (RFC822) for the given ID
		result, data = self.mail.fetch(latest_email_id, "(RFC822)") 
		
		msg = email.message_from_string(data[0][1])
		#print msg
		#raw_email = data[0][1] # here's the body, which is raw text of the whole email	
		fout = open('lastEmail.txt','w')
		fout.write(str(msg))
		fout.close()
		# including headers and alternate payloads

		'''
		server = 'mail.server.com'
		user = ''
		password = ''

		recipients = ['user@mail.com', 'other@mail.com']
		sender = 'you@mail.com'
		message = 'Hello World'listen for new messages in a loop.

		session = smtplib.SMTP(server)
		# if your SMTP server doesn't need authentications,
		# you don't need the following line:
		session.login(user, password)
		session.sendmail(sender, recipients, message)
		'''
	def login(self):
		user = getpass.getuser("Please enter your email address:")
		pswd = getpass.getpass("Please enter your password:")
		self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
		self.mail.login(user, pswd)
		pswd = None

if __name__ == '__main__':
	proc = ProcessEmail()
	new = Message('lastEmail.txt')
	print new.getBody()
