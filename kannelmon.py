import threading
import daemon
import logging
import time
import socket
import urllib2
from xmlparser2 import *
from sendemail import *
from urllib2 import *

class ThreadedMonitor(threading.Thread):
    
    ERROR_COULD_NOT_CONNECT = 'Could not connect to Kannel status URL.'
    ERROR_XML_PARSING = 'Could not parse Kannel status XML.'
    ERROR_SMSC_OFFLINE = 'SMSC is re-connecting: '
    ERROR_SMSC_DEAD = 'SMSC is dead: '
    
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            url = 'http://localhost:13000/status.xml'
            req = Request(url)
            timeout = 10
            socket.setdefaulttimeout(timeout)
            response = urlopen(req)
            xml = response.read()
            logging.info('Fetching Kannel status from ' + url)
        except:
            logging.info(self.ERROR_COULD_NOT_CONNECT)
        else:
            logging.info('Kannel status fetched succesfully.')

            if xml:
                xml_parser = Parser()
                array = xml_parser.feed(xml)
                xml_parser.close()
                
                if array:
                    logging.info('SMSC Status')
                    for x in array.keys():
                        if array[x] == 're-connecting':
                            text = self.ERROR_SMSC_OFFLINE + x
                            emailthread = SendEmail(text)
                            emailthread.start()
                            logging.info('Sending alert notification email...')

                        elif array[x] == 'dead':
                            text = self.ERROR_SMSC_DEAD + x
                            emailthread = SendEmail(text)
                            emailthread.start()
                            logging.info('Sending alert notification email...')

                        logging.info(x + ': ' + array[x])
            else:
                logging.info(self.ERROR_XML_PARSING)
        
class SendEmail(threading.Thread):
    def __init__(self, text):
        self.text = text
        threading.Thread.__init__(self)

    def run(self):
        sendresult = sendMail('eduardoraad@gmail.com', 'SMS Gateway Alert', self.text, 'eduardoraad@gmail.com', 'er51802204')
        if sendresult:
            logging.info('Alert email notification sent succesfully.')
        else:
            logging.info('Alert email notification failed.')

class HelloDaemon(daemon.Daemon):
    default_conf = 'kannelmon.conf'
    section = 'kannelmon'

    def run(self):
        while True:
            mythread = ThreadedMonitor()
            mythread.start()
            time.sleep(20)

if __name__ == '__main__':
    HelloDaemon().main()
    
