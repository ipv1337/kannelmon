import urllib2
import threading
import daemon
import logging
import time
from xmlparser2 import *
from sendemail import *

class ThreadedMonitor(threading.Thread):
    def run(self):
        url = 'http://localhost:13000/status.xml'

        response = urllib2.urlopen(url)
        xml = response.read()

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
    default_conf = 'hellodaemon.conf'
    section = 'hello'

    def run(self):
        while True:
            mythread = ThreadedMonitor()
            mythread.start()
            time.sleep(60)

if __name__ == '__main__':
    HelloDaemon().main()
    
