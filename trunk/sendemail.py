'''
Thanks to http://codecomments.blogspot.com/ for the Gmail SMTP code.
'''

import os
import smtplib

def sendMail(to, subject, text, username, password):
    gmailUser = username
    gmailPassword = password
    recipient = to

    headers = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n' % (username, to, subject)
    message = headers + text

    try:
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, message)
        mailServer.close()
        return True
    except Exception, e:
        return None
