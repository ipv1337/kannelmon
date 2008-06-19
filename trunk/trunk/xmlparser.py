from xml.parsers import expat

class Parser:

    def __init__(self):
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.inSmsc = 0
        self.inId = 0
        self.inQueued = 0
        self.mapping = {}

    def feed(self, data):
        if data:
            self._parser.Parse(data, 0)
            return self.mapping

    def close(self):
        self._parser.Parse("", 1) # end of data
        del self._parser # get rid of circular references

    def start(self, tag, attr):
        if tag == 'smsc':
            self.inSmsc = 1
        elif tag == 'id':
            self.inId= 1
        elif tag == 'queued':
            self.inQueued= 1
            
    def data(self, data):
        if self.inSmsc:
            if self.inId:
                self.smscId = data
            elif self.inQueued:
                self.queued = data

    def end(self, tag):
        if self.inId:
            self.inId = 0
        elif self.inQueued:
            self.inQueued = 0
        elif self.inSmsc:
            self.inSmsc = 0
            self.mapping['hola'] = self.queued
