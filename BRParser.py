import HTMLParser, re

class GameTeamsParser(HTMLParser.HTMLParser):
    awayTeamAbb = ''
    homeTeamAbb = ''
    startData = False
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.startData = True
        elif self.startData and tag == 'a':
            for x in attrs:
                if x[0] == 'href':
                    if self.awayTeamAbb == '':
                        self.awayTeamAbb = x[1].split('/')[2]
                    else:
                        self.homeTeamAbb = x[1].split('/')[2]
        
    def handle_endtag(self, tag):
        if tag == 'pre':
            self.startData = False
    
    def handle_data(self, data):
        pass

class GameTimeParser(HTMLParser.HTMLParser):
    startData = False
    startData1 = False
    time = ''
    gamelen = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.time == '':
            for att in attrs:
                if att[0] == 'class' and att[1] =='bold_text float_left':
                    self.startData = True
        elif tag == 'div' and self.gamelen == '':
            for att in attrs:
                if att[0] == 'id' and att[1] == 'gametime':
                    self.startData1 = True
        
    def handle_endtag(self, tag):
        if tag == 'div' and self.startData:
            self.startData = False
        elif tag == 'div' and self.startData:
            self.startData1 = False
    
    def handle_data(self, data):
        if self.startData:
            self.time = str(re.search('[0-9]{1,2}:[0-9]{2} ?[ap]m', data, flags=re.IGNORECASE).group(0))
        if self.startData1:
            if re.search('[0-9]{1,2}:[0-9]{2}', data) != None:
                self.gamelen = str(re.search('[0-9]{1,2}:[0-9]{2}', data).group(0))

class GameWeatherParser(HTMLParser.HTMLParser):
    startData = False
    startData1 = False
    weather = ''
    field = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for att in attrs:
                if att[0]== 'id' and att[1]== 'weather':
                    self.startData = True
                elif att[0]=='id' and att[1]== 'fieldcond':
                    self.startData1 = True
        
    def handle_endtag(self, tag):
        if tag == 'div' and self.startData:
            self.startData = False
        elif tag == 'div' and self.startData1:
            self.startData1 = False
        
    def handle_data(self, data):
        if self.startData:
            self.weather += data
        elif self.startData1:
            self.field += data

class GameUmpParser(HTMLParser.HTMLParser):
    startData = False
    homeump = ''
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for x in attrs:
                if x[0] == 'id' and x[1] == 'Umpires':
                    self.startData = True                    
                    
    def handle_endtag(self, tag):
        if tag == 'div' and self.startData:
            self.startData = False
    
    def handle_data(self, data):
        if self.startData:
            self.homeUmp = re.search('HP - (.*), 1B',data)
    
class GameWinLossSaveParser(HTMLParser.HTMLParser):
    startData = False
    startWin = False
    startLoss = False
    startSave = False
    winPitch = ''
    lossPitch = ''
    savePitch = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for x in attrs:
                if x[0] == 'class' and x[1] == 'padding_left small_text':
                    self.startData = True
                    
    def handle_endtag(self, tag):
        if self.startData and tag == 'td':
            self.startData = False
    
    def handle_data(self, data):
        if self.startData:
            if data == 'W:':
                self.startWin = True
            elif self.startWin and data.strip() != '':
                self.winPitch = data
                self.startWin = False
            elif data == 'L:':
                self.startLoss = True
            elif self.startLoss and data.strip() != '':
                self.lossPitch = data
                self.startLoss = False
            elif data == 'S:':
                self.startSave = True
            elif self.startSave and data.strip() != '':
                self.savePitch = data
                self.startSave = False
            
class GamesParser(HTMLParser.HTMLParser):
    foundh2 = False
    startData = False
    games = []
    BRabbrevs = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
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
            if data in self.BRabbrevs:
                if self.lastIn == 'H':
                    self.a = data
                    self.lastIn = 'A'
                elif self.lastIn == 'A':
                    self.h = data
                    self.lastIn = 'H'
            elif data.strip('@') in self.BRabbrevs:
                if self.lastIn == 'H':
                    self.a = data.strip(' ').strip('@')
                    self.lastIn = 'A'
                elif self.lastIn == 'A':
                    self.h = data.strip(' ').strip('@')
                    self.lastIn = 'H'


    def handle_endtag(self,tag):
        if tag == 'h2':
            self.foundh2 = False