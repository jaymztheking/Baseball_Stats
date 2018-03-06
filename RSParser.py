import html.parser
import re
from datetime import datetime

class PlayerInfoParser(html.parser.HTMLParser):
    startData = False
    firstGameFound = False
    getFirstGame = False
    birthDate = None
    debutDate = None
    batHand = ''
    throwHand = ''
    height = 0
    weight = 0
    tempData = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.startData = True
        elif self.firstGameFound and tag == 'a':
            self.getFirstGame = True
        
    def handle_endtag(self, tag):
        if tag == 'table' and self.startData:
            self.startData = False
        elif self.getFirstGame and tag == 'a':
            self.getFirstGame = False
            self.firstGameFound = False
    
    def handle_data(self, data):
        if self.startData:
            if re.match('Born [^(as)]',data):
                bornPiece = data.split()
                dateStr = bornPiece[1] + bornPiece[2].replace(',','')+bornPiece[3].replace(',','')
                self.birthDate = datetime.strptime(dateStr, '%B%d%Y').date()
            elif re.match('First Game', data) != None:
                self.tempData = data
                self.firstGameFound = True
            elif self.getFirstGame:
                debutPiece = data.split()
                dateStr = debutPiece[0]+debutPiece[1].replace(',','')+debutPiece[2]
                self.debutDate = datetime.strptime(dateStr, '%B%d%Y').date()
            elif re.match('Bat: ', data) != None:
                if self.firstGameFound and self.debutDate == None:
                    debutPiece = self.tempData.split()[2:]
                    dateStr = debutPiece[0]+debutPiece[1].replace(',','')+debutPiece[2]
                    self.debutDate = datetime.strptime(dateStr, '%B%d%Y').date()
                self.firstGameFound = False
                pieces = data.split()
                self.batHand = pieces[1][0]
                self.throwHand = pieces[3][0]
                self.height = int(pieces[5].strip("'"))*12+int(round(float(pieces[6].strip('"'))))
                self.weight = int(pieces[8])
                

