import threading
import daemon
import logging
import time
import socket
import urllib2
from xmlparser2 import *
from sendemail import *
from urllib2 import Request, urlopen, URLError, HTTPError

print 'hello'
try:
    url = 'http://localhost:13000/status.xml'
    req = Request(url)
    timeout = 10
    socket.setdefaulttimeout(timeout)
    response = urlopen(req)
except IOError,  e:
    if hasattr(e, 'reason'):
        print 'Reason: fuckfuck',  e.reason
    elif hasattr(e,  'code'):
        print 'Code: ',  e.code
except socket.error,  e:
    print 'unexpected error'
else:
    xml = response.read()
    print 'Fetching Kannel status from ',  url

    if xml:
        xml_parser = Parser()
        array = xml_parser.feed(xml)
        xml_parser.close()
        
        if array:
            logging.info('SMSC Status')
            for x in array.keys():
                if array[x] == 're-connecting':
                    text = x + ' is offline...'
                    emailthread = SendEmail(text)
                    emailthread.start()
                    logging.info('Sending alert notification email... (offline)')

                elif array[x] == 'dead':
                    text = x + ' is dead...'
                    emailthread = SendEmail(text)
                    emailthread.start()
                    logging.info('Sending alert notificacion email... (dead)')

                logging.info(x + ': ' + array[x])
    else:
        logging.info('error with xml format')
logging.info('finished...')
