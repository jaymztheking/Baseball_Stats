import urllib2
from BRParser import LineScoreParser, GameWeatherParser, GameTimeParser, LineupParser
from datetime import date, time
from bbUtils import GetTeamKey, GetParkKey, GetParkTZ
from LineupStats import Lineup

class Game:
    parkKey = None #done
    homeTeam = None #done
    awayTeam = None #done
    date = None #done
    time = None #done
    temp = None #done
    windDir = None #done
    windSpeed = 0 #done
    weather = '' #done
    totalInnings = 9 #done
    homeHits = 0 #done
    awayHits = 0 #done
    homeRuns = 0 #done
    awayRuns = 0 #done
    homeErrors = 0 #done
    awayErrors = 0 #done
    homeTeamWin = False #done
    tie = False #done
    
    def __init__(self, hTeam, aTeam, date, con):
        self.homeTeam = GetTeamKey(hTeam, con)
        self.awayTeam = GetTeamKey(aTeam, con)
        self.date = date
        self.parkKey = GetParkKey(self.homeTeam, date, con)

    def GetBRLineScore(self, url):
        b = LineScoreParser()
        html = urllib2.urlopen(url).read().decode('utf-8')
        b.feed(html)
        pos = 0
        for i in range(0,3):
            newPos = b.lineScore.find('\n',pos) + 1
            pos = newPos
        topTeamStart = pos
        topTeamEnd = b.lineScore.find('\n',pos+1)
        botTeamStart = topTeamEnd + 1
        botTeamEnd = b.lineScore.find('\n',botTeamStart+1)
        topTeamLine = b.lineScore[topTeamStart:topTeamEnd]
        botTeamLine = b.lineScore[botTeamStart:botTeamEnd]
        topTeam = topTeamLine.split(' ')
        botTeam = botTeamLine.split(' ')
        topTeamNums = []
        botTeamNums = []
        for x in topTeam:
            if x.isdigit():
                topTeamNums.append(x)
        for x in botTeam:
            if x.isdigit():
                botTeamNums.append(x)
        self.awayRuns = int(topTeamNums[-3])
        self.homeRuns = int(botTeamNums[-3])
        self.awayHits = int(topTeamNums[-2])
        self.homeHits = int(botTeamNums[-2])
        self.awayErrors = int(topTeamNums[-1])
        self.homeErrors = int(botTeamNums[-1])
        self.totalInnings = int(len(topTeamNums)-3)
        if self.homeRuns > self.awayRuns:
            self.homeTeamWin = True
        elif self.homeRuns == self.awayRuns:
            self.tie = True
            
    def GetBRWeatherInfo(self, url):
        b = GameWeatherParser()
        weatherString = ""
        html = urllib2.urlopen(url).read().decode('utf-8')
        b.feed(html)
        weatherString = b.weather
        for x in weatherString.split(' '):
            if x.isdigit():
                self.temp = int(x)
            elif x[-3:] == 'mph':
                self.windSpeed = int(x.replace('mph',''))
        weatherList = weatherString.split(',')
        windString = weatherList[1]
        self.windDir = windString[windString.find('mph')+4:]
        for x in weatherList[2:]:
            self.weather += str(x)
            
    def GetBRGameTime(self, url, con):
        b= GameTimeParser()
        tempTime = ""
        html = urllib2.urlopen(url).read().decode('utf-8')
        b.feed(html)
        tempTime = b.time.split(',')[-1].strip()  
        if tempTime != "":        
            self.time = tempTime+' '+GetParkTZ(self.parkKey, con)
        else:
            self.time = '11:59 pm '+GetParkTZ(self.parkKey, con)
        
    def InsertStats(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "GAME" VALUES (default, %s, \'%s\', \'%s\', \'%s\', %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' % \
        (self.parkKey, self.date.strftime('%Y-%m-%d'), self.time, self.windDir, self.windSpeed, self.weather, self.totalInnings, self.homeHits, self.awayHits, self.homeRuns, self.awayRuns, self.homeErrors, self.awayErrors, self.homeTeam, self.awayTeam, self.temp, self.homeTeamWin, self.tie )
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            return True
        return False
    
    def CheckForRow(self, con):
        cur = con.cursor()        
        checkSQL = 'select "GAME_KEY" from "GAME" where "PARK_KEY" = %s and "HOME_TEAM_KEY" = %s and "AWAY_TEAM_KEY" = %s and "GAME_DATE" = \'%s\' and "GAME_TIME" = \'%s\'' % \
        (self.parkKey, self.homeTeam, self.awayTeam, self.date.strftime('%Y-%m-%d'), self.time)
        cur.execute(checkSQL)
        results = cur.fetchall()
        if len(results) == 0:
            return False
        else:
            return True
            
    def GetLineupInfo(self, url, con):
        batnum = 0
        userid = ''
        pos = ''
        name = ''
        parms = 0
        b = LineupParser()
        html = urllib2.urlopen(url).read().decode('utf-8')
        b.feed(html)
        for i in range(2,len(b.pieces)):
            if i.isdigit():
                batnum = b.pieces[i]
                parms += 1
            elif i[:9] == '/players/'
                userid = b.pieces[i].split('/')[-1].replace('.shtml','')
                parms += 1

    def UpdateStats(self, con):
        return True




