import HTMLParser

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
            
            
