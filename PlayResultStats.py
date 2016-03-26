from bbUtils import GetGameKeys, GetHitterKeyfromLU, GetTeamfromAbb, GetPos
import psycopg2
from datetime import date
from GameStats import Game
from LineupStats import Lineup
from PitchingStats import PitchRoster

def ProcessPlayLog(filename, con):
    text = open(filename)
    lineup = {}
    pitchers = {}
    startSit = 1
    awayTeam = None
    homeTeam = None
    homeTeamAbb = ''
    awayTeamAbb = ''
    windDir = ''
    windSpeed = 0
    weather = []
    gameDate = None
    gameTime = None
    gameLength = 0
    gameTemp = 0
    homeUmp = ''
    gameKey = None
    awayPitcherKey = None
    homePitcherKey = None
    for line in text:
        row = line.split(',')
        rowType = row[0]
        gameIndex = 0
        
        
        #Grab game info and create game row
        if rowType == 'info':
            att = row[1]
            if att == 'visteam':
                awayTeamAbb = row[2].strip()
                if awayTeam == None:
                    awayTeam = GetTeamfromAbb(awayTeamAbb, con)
                    if awayTeam == None:
                        print(awayTeamAbb)
            elif att == 'hometeam':
                homeTeamAbb = row[2].strip() 
                if homeTeam == None:
                    homeTeam = GetTeamfromAbb(homeTeamAbb, con)
            elif att == 'date':
                datePieces = row[2].split('/')
                gameDate = date(int(datePieces[0]),int(datePieces[1]),int(datePieces[2]))
            elif att == 'starttime':
                gameTime = row[2]
            elif att == 'winddir':
                windDir = row[2]
            elif att == 'windspeed':
                windSpeed = int(row[2])
            elif att == "temp":
                gameTemp = int(row[2])
            elif att == "fieldcond":
                weather[0] = row[2]
            elif att == "precip":
                weather[1] = row[2]
            elif att == "sky":
                weather[2] = row[2]
            elif att == "timeofgame":
                gameLength = int(row[2])
            elif att == "umphome":
                homeUmp = row[2]
                
        elif gameKey == None and gameDate != None and homeTeam != None and awayTeam != None:
            currentGame = Game(homeTeam, awayTeam, gameDate, con)
            currentGame.time = gameTime
            currentGame.temp = gameTemp
            currentGame.windDir = windDir
            currentGame.windSpeed = windSpeed
            currentGame.weather = 'Field = '+weather[0]+', Prec = '+weather[1]+', Sky = '+weather[2]
            currentGame.gameLength = gameLength
            currentGame.totalInnings = 9 
            currentGame.homeHits = 0 
            currentGame.awayHits = 0 
            currentGame.homeRuns = 0 
            currentGame.awayRuns = 0 
            currentGame.homeErrors = 0 
            currentGame.awayErrors = 0 
            currentGame.homeTeamWin = False 
            currentGame.tie = False
            currentGame.homeUmp = homeUmp
            currentGame.InsertStats(con)
            gameKey = currentGame.gameKey
           
        #Grab hitter and starting pitcher keys from lineup
        elif rowType == 'start':
            userID = row[1]
            playerName = row[2]
            if row[3] == 0:
                team = awayTeam
            else:
                team = homeTeam
            playerBatNum = row[4]
            playerPos = GetPos(row[5])
            if playerPos != 'P':
                lineup[userID] = Lineup(gameKey, team, playerName, playerBatNum, playerPos, userID, con)
            else:
                pitchers[userID] = PitchRoster(gameKey, team, playerName, userID, con)
                pitchers[userID].pitcherRole = 'Starter'
                if row[3] == 0:
                    awayPitcherKey = pitchers[userID].pitcherKey
                else:
                    homePitcherKey = pitchers[userID].pitcherKey
                
        #Grab play-by-play stuff
        elif rowType == 'play':
           pitchSeq = row[5]
           innPre = 'Top' if row[2]== '0' else 'Bot'
           inning = innPre + ' '+str(row[1])
           hitterKey = lineup[row[1]].player
           if innPre == 'Top':
               pitcherKey = homePitcherKey
           else:
               pitcherKey = awayPitcherKey
           ballCount = int(row[4][0])
           strikeCount= int(row[4][1])
           
           
        #New game found, reset everything   
        elif rowType == 'id':
            startSit = 1
            awayTeam = None
            homeTeam = None
            homeTeamAbb = ''
            awayTeamAbb = ''
            windDir = ''
            windSpeed = 0
            weather = []
            gameDate = None
            gameTime = None
            gameLength = 0
            gameTemp = 0
            homeUmp = ''
            gameKey = None
            awayPitcherKey = None
            homePitcherKey = None
            userID = ''
            playerName = ''
            team = None
            playerBatNum = 0
            playerPos = ''
            lineup = {}
            pitchers = {}


class PitchResult:
    gameKey = 0 #done
    hitterKey = 0 #done
    pitcherKey = 0 #done
    startSituationKey = 0
    inning = '' #done
    strikeCount = 0 #done
    ballCount = 0 #done
    pitchSeq = '' #done
    contactStrikes = 0
    swingStrikes = 0
    lookStrikes = 0
    playType = ''
    hit = False
    resultOuts = 0
    endSituationKey = 0
    ballLoc = ''
    ballType = ''
    runScored = False
    RBI = 0
    
    def __init__(self, gk, hk, pk, sk):
        self.gameKey = gk
        self.hitterKey = hk
        self.pitcherKey = pk
        self.startSituationKey = sk
        
    def ProcessPitchSeq(self):
        if self.pitchSeq != '':
            pass
    
    def ProcessEventString(self):
        
    
        
    
pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
processPlayLog('.\\Play by Play Logs\\2015DET.EVA', con)