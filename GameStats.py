from bbUtils import GetParkKey, GetGameKey

class Game:
    gameKey = None  #done
    parkKey = None
    homeTeam = None #done
    awayTeam = None #done
    date = None  #done
    time = None  #done
    temp = None #done 
    windDir = None #done
    windSpeed = 0 #done
    weather = '' #done
    gameLength = 0 #done
    totalInnings = 9 
    homeHits = 0 
    awayHits = 0 
    homeRuns = 0 
    awayRuns = 0 
    homeTeamWin = False 
    tie = False
    homeUmp = ''
    
    def __init__(self, hTeam, aTeam, date, con):
        self.homeTeam = hTeam
        self.awayTeam = aTeam
        self.date = date
        
    def InsertBlankGame(self, con):
        cur = con.cursor()
        pk = GetParkKey(self.homeTeam, self.date, con)
        sql = 'insert into "GAME" ("GAME_KEY", "PARK_KEY", "GAME_DATE","GAME_TIME","HOME_TEAM_KEY","AWAY_TEAM_KEY")  VALUES (default, %s, \'%s\', \'%s\', %s, %s)' % \
        (pk ,self.date.strftime('%Y-%m-%d'), self.time, self.homeTeam, self.awayTeam)
        self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if self.gameKey == None:
            cur.execute(sql)
            cur.execute('COMMIT;')
            self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        return True
        
    def InsertFullStats(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "GAME" VALUES (default, %s, \'%s\', \'%s\', \'%s\', %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \'%s\');' % \
        (self.parkKey, self.date.strftime('%Y-%m-%d'), self.time, self.windDir, self.windSpeed, self.weather, self.totalInnings, self.homeHits, self.awayHits, self.homeRuns, self.awayRuns, self.homeTeam, self.awayTeam, self.temp, self.homeTeamWin, self.tie, self.gameLength, self.homeUmp )
        self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if self.gameKey == None:
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        return True
        
    def UpdateStats(self, con):
        cur = con.cursor()

        sql = 'update "GAME" set ("WIND_DIR","WIND_SPEED_MPH","WEATHER_CONDITION","TOTAL_INNINGS","HOME_HITS",' \
              '"AWAY_HITS","HOME_RUNS","AWAY_RUNS","GAME_TEMP_F","HOME_TEAM_WIN?",' \
              '"TIE?","GAME_TIME_MINUTES","HOME_UMP_ID") = (\'%s\',%s,\'%s\', %s, %s, ' \
              '%s, %s, %s, %s, \'%s\', ' \
              '\'%s\', %s, \'%s\') WHERE "GAME_KEY" = %s' % \
         (self.windDir, self.windSpeed, self.weather, self.totalInnings, self.homeHits,
         self.awayHits, self.homeRuns, self.awayRuns, self.temp, self.homeTeamWin,
         self.tie, self.gameLength, self.homeUmp, self.gameKey)

        cur.execute(sql)
        cur.execute('COMMIT;')
        
    def CheckForRow(self, con):
        gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if gameKey == None:
            return False
        else:
            return True





