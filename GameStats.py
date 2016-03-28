from bbUtils import GetTeamfromAbb, GetParkKey, GetGameKey

class Game:
    gameKey = None 
    parkKey = None
    homeTeam = None
    awayTeam = None
    date = None 
    time = None 
    temp = None 
    windDir = None 
    windSpeed = 0 
    weather = ''
    gameLength = 0
    totalInnings = 9 
    homeHits = 0 
    awayHits = 0 
    homeRuns = 0 
    awayRuns = 0 
    homeErrors = 0 
    awayErrors = 0 
    homeTeamWin = False 
    tie = False
    homeUmp = ''
    
    def __init__(self, hTeam, aTeam, date, con):
        self.homeTeam = GetTeamfromAbb(hTeam, con)
        self.awayTeam = GetTeamfromAbb(aTeam, con)
        self.date = date
        
    def GetGamePark(self, date, con):
        self.parkKey = GetParkKey(self.homeTeam, date, con)
              
    def InsertStats(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "GAME" VALUES (default, %s, \'%s\', \'%s\', \'%s\', %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \'%s\');' % \
        (self.parkKey, self.date.strftime('%Y-%m-%d'), self.time, self.windDir, self.windSpeed, self.weather, self.totalInnings, self.homeHits, self.awayHits, self.homeRuns, self.awayRuns, self.homeErrors, self.awayErrors, self.homeTeam, self.awayTeam, self.temp, self.homeTeamWin, self.tie, self.gameLength, self.homeUmp )
        self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if self.gameKey == None:
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        return True
        
    def CheckForRow(self, con):
        gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if gameKey == None:
            return False
        else:
            return True

    def UpdateStats(self, con):
        return True




