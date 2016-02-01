import urllib2
from BRParser import LineScoreParser, GamesParser
from datetime import date, time
from bbUtils import GetTeamKey, GetParkKey

def GetGames(date, con):
    url = "http://www.baseball-reference.com/games/standings.cgi?date="+date.strftime('%Y-%m-%d')
    b = GamesParser()
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    games = []
    for game in b.games:
        print(game[1]+' at '+game[0]+'  --  '+game[2])
        myGame = Game(game[0], game[1], date, con)
        myGame.GetBRLineScore(game[2])
        games.append(myGame)
    return games


class Game:
    parkKey = None
    homeTeam = None
    awayTeam = None
    date = None
    time = None
    temp = None
    windDir = None
    windSpeed = 0
    weather = None
    totalInnings = 9
    homeHits = 0
    awayHits = 0
    homeRuns = 0
    awayRuns = 0
    homeErrors = 0
    awayErrors = 0
    homeTeamWin = False
    tie = False
    
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
        
    def InsertStats(self):
        return True

    def GetParkKey(self):
        return 1




