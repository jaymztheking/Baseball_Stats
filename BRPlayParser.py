import HTMLParser

class BRPlayParser(HTMLParser.HTMLParser):
    startData = False
    insideTable = False
    subRow = False
    index = 0
    playNum = 0
    lineup = {}
    pitchers = {}
    plays = {}
    subs = []
    
    def handle_starttag(self, tag, attrs):
        for att in attrs:
            if att[0] == 'id' and att[1][:6] == 'event_':
                self.startData = True
                self.playNum = int(att[1].split('_')[1])
                self.plays[self.playNum] = ['','','','','','','','','','','','']
            if tag == 'td' and self.startData:
                self.insideTable = True
            if tag == 'span' and att[0] == 'class' and att[1] == 'ingame_substitution':
                self.subRow = True
        
    def handle_data(self, data):
        if self.startData and self.insideTable:    
            self.plays[self.playNum][self.index] = data
        if self.subRow:
            self.subs.append([self.playNum,data])
        
    def handle_endtag(self, tag):
        if tag == 'tr' and self.startData:
            self.startData = False
            self.index = 0
        elif tag == 'td' and self.insideTable:
            self.insideTable = False
            self.index += 1
        elif tag == 'span' and self.subRow:
            self.subRow = False
            
        