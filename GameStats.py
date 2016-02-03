import urllib2
from BRParser import LineScoreParser, GamesParser, GameWeatherParser, GameTimeParser
from datetime import date, time
from bbUtils import GetTeamKey, GetParkKey, GetParkTZ

def GetGames(date, con):
    url = "http://www.baseball-reference.com/games/standings.cgi?date="+date.strftime('%Y-%m-%d')
    b = GamesParser()
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    games = []
    for game in b.games:
        myGame = Game(game[0], game[1], date, con)
        myGame.GetBRLineScore(game[2])
        myGame.GetBRWeatherInfo(game[2])
        myGame.GetBRGameTime(game[2], con)
        games.append(myGame)
    return games


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
                self.windSpeed == int(x.replace('mph',''))
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
        self.time = tempTime+' '+GetParkTZ(self.parkKey, con)
        
    def InsertStats(self):
        return True

    def GetParkKey(self):
        return 1




