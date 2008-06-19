from xml.parsers import expat

class Parser:

    def __init__(self):
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.inStatus = 0
        self.inSmsc = 0
        self.inId = 0
        self.status = ''
        self.id = ''
        self.lastId = ''
        self.mapping = {}
        self.properties = {}

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
        elif tag == 'status':
            self.inStatus = 1
        elif tag == 'id':
            self.inId = 1
            
    def data(self, data):
        if self.inSmsc:
            if self.inStatus:                self.status = data
            if self.inId:
                self.id = data
                self.lastId = self.id

    def end(self, tag):
        if tag == 'id':
            self.inId = 0
        elif tag == 'status':
            self.inStatus = 0
        elif tag == 'smsc':
            self.inSmsc = 0
            self.mapping[self.lastId] = self.status
