import HTMLParser

class TestParser(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass
    def handle_charref(self, name):
        print(name)
    
    def handle_data(self, data):
        print(data)
    
    def handle_endtag(self, data):
        pass

class GameTimeParser(HTMLParser.HTMLParser):
    startData = False
    time = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.time == '':
            for att in attrs:
                if att[0] == 'class' and att[1] =='bold_text float_left':
                    self.startData = True
        
    def handle_endtag(self, tag):
        if tag == 'div' and self.startData:
            self.startData = False
    
    def handle_data(self, data):
        if self.startData:
            self.time = data

class GameWeatherParser(HTMLParser.HTMLParser):
    startData = False
    weather = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for att in attrs:
                if att[0]== 'id' and att[1]== 'weather':
                    self.startData = True
        
    def handle_endtag(self, tag):
        if tag == 'div' and self.startData:
            self.startData = False
        
    def handle_data(self, data):
        if self.startData:
            self.weather += data

class LineScoreParser(HTMLParser.HTMLParser):
    startData = False
    lineScore = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for att in attrs:
                if att[0] == 'colspan' and att[1] == '4':
                    for att in attrs:
                        if att[0] == 'class' and att[1] == 'padding_top':
                            self.startData = True
    def handle_endtag(self, tag):
        if tag == 'td' and self.startData == True:
            self.startData = False
            return self.lineScore
    def handle_data(self, data):
        if self.startData == True:
            self.lineScore += data
       

class GamesParser(HTMLParser.HTMLParser):
    foundh2 = False
    startData = False
    games = []
    abbrevs = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
    a = ''
    h = ''
    lastIn = 'H'
    
    def handle_starttag(self, tag, attrs):
        prefix = "http://www.baseball-reference.com"
        if self.startData and tag == 'a':
            for att in attrs:
                if att[0] == 'href' and att[1][:6]=='/boxes':
                    self.games.append([self.h,self.a,prefix+att[1]])
            

        elif tag == 'h2':
            self.foundh2 = True

    def handle_data(self, data):
        if self.foundh2 and data[:19] == 'Standings and Games':
            self.startData = True
        elif data == 'Standings Up to and Including this Date':
            self.startData = False
        elif self.startData:
            data = data.replace(' ','').strip('@').strip('\n')
            if data in self.abbrevs:
                if self.lastIn == 'H':
                    self.a = data
                    self.lastIn = 'A'
                elif self.lastIn == 'A':
                    self.h = data
                    self.lastIn = 'H'
            elif data.strip('@') in self.abbrevs:
                if self.lastIn == 'H':
                    self.a = data.strip(' ').strip('@')
                    self.lastIn = 'A'
                elif self.lastIn == 'A':
                    self.h = data.strip(' ').strip('@')
                    self.lastIn = 'H'


    def handle_endtag(self,tag):
        if tag == 'h2':
            self.foundh2 = False
            
            
class LineupParser(HTMLParser.HTMLParser):
    startData = False
    foundh2 = False    
    pieces = []
    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.foundh2 = True
        elif tag == 'div':
            for att in attrs:
                if att[0] == 'id' and att[1] == 'wrap_wpa_chart':
                    self.startData = False
                    self.foundh2 = False
        elif tag == 'a' and self.startData:
            for att in attrs:
                if att[0] == 'href':
                    self.pieces.append(att[1])
            
    def handle_data(self, data):
        if self.foundh2 and data == 'Starting Lineups':
            self.startData = True
        elif self.startData and data.strip() != '':
            self.pieces.append(data)
        
    def handle_endtag(self, data):
        pass
    
class BattingDataParser(HTMLParser.HTMLParser):
    startData = False
    startText = False
    rowData = []
    allRows = []
    lastAtag = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for att in attrs:
                if att[0] == 'id' and att[1][-7:] == 'batting':
                    self.startData = True
        elif tag == 'a':
            for att in attrs:
                if att[0] == 'href' and att[1][:9] == '/players/':
                    self.lastAtag = att[1].split('/')[-1].replace('.shtml','')
        elif tag == 'td' and self.startData:
                for att in attrs:
                    if att[0] == 'align' and att[1] not in ('left', 'right'):
                        self.startText = True
        
                    
    def handle_data(self, data):
        if self.startData:
            piece = data.strip()
            if piece != '':
                self.rowData.append(piece)
        
        
    def handle_endtag(self, tag):
        if tag == 'table' and self.startData:
            self.startData = False
        elif tag == 'tr' and self.startData:
            self.startText = False
            self.rowData.insert(0, self.lastAtag)
            self.allRows.append(self.rowData)
            self.rowData = []
            
class PitchRosterParser(HTMLParser.HTMLParser):
    startData = False
    allRows = []
    rowData = []
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for att in attrs:
                if att[0] == 'id' and att[1][-8:] == 'pitching':
                    self.startData = True
    
    def handle_data(self,data):
        if self.startData:
            piece = data.strip()
            if piece != '':
                self.rowData.append(piece)
    
    def handle_endtag(self,tag):
        if tag == 'table' and self.startData:
            self.startData = False
        elif tag == 'tr' and self.startData:
            self.startText = False
            self.allRows.append(self.rowData)
            self.rowData = []