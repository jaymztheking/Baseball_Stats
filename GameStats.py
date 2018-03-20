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
        sql = 'insert into game (game_key, park_key, game_date, game_time, home_team_key, away_team_key)  VALUES (default, %s, \'%s\', \'%s\', %s, %s)' % \
        (pk ,self.date.strftime('%Y-%m-%d'), self.time, self.homeTeam, self.awayTeam)
        self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        if self.gameKey == None:
            cur.execute(sql)
            cur.execute('COMMIT;')
            self.gameKey = GetGameKey(self.homeTeam, self.awayTeam, self.date, self.time, con)
        return True

    def UpdateStats(self, con):
        cur = con.cursor()

        sql = 'update game set (wind_dir, wind_speed_mph, weather_condition, total_innings, home_hits,' \
              'away_hits, home_runs, away_runs, game_temp_f, home_team_win, ' \
              'tie, game_time_minutes, home_ump_id) = (\'%s\',%s,\'%s\', %s, %s, ' \
              '%s, %s, %s, %s, \'%s\', ' \
              '\'%s\', %s, \'%s\') WHERE game_key = %s' % \
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





