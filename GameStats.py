import urllib2
from BRParser import LineScoreParser
from datetime import date, time

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
    
    def __init__(self, hTeam, aTeam, date, time):
        self.parkKey = self.GetParkKey(hTeam, date)
        self.homeTeam = hTeam
        self.awayTeam = aTeam
        self.date = date
        self.time = time

    def GetBRRawStats(self):
        b = LineScoreParser()
        url = 'http://www.baseball-reference.com/boxes/LAN/LAN201509150.shtml'
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
        topRESpace = topTeamLine.rfind(' ')
        topHRSpace = topTeamLine[:topRESpace-1].rfind(' ')
        topISSpace = topTeamLine[:topHRSpace-1].rfind(' ')
        botRESpace = botTeamLine.rfind(' ')
        botHRSpace = botTeamLine[:botRESpace-1].rfind(' ')
        botISSpace = botTeamLine[:botHRSpace-1].rfind(' ')
        self.awayErrors = int(topTeamLine[topRESpace:].strip())
        self.awayHits = int(topTeamLine[topHRSpace:topRESpace].strip())
        self.awayRuns = int(topTeamLine[topISSpace:topHRSpace].strip())
        self.homeErrors = int(botTeamLine[botRESpace:].strip())
        self.homeHits = int(botTeamLine[botHRSpace:botRESpace].strip())
        self.homeRuns = int(botTeamLine[botISSpace:botHRSpace].strip())
        print self.awayRuns, self.awayHits, self.awayErrors
        print self.homeRuns, self.homeHits, self.homeErrors

    def InsertStats(self):
        return True

    def GenerateURL(self):
        prefix = 'http://www.baseball-reference.com/boxes/'
        abb = 'LAN'
        abbWithDate = 'LAN201509150.shtml'
        url = prefix+abb+abbWithDate+'.shtml'
        return url

    def GetParkKey(self):
        return 1

testGame = Game(1,2, date(2015,9,15), time(17,23,0))
testGame.GetBRRawStats()
