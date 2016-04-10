from PlayByPlay import Play, PlayByPlay
from Game import Game
from bbUtils import GetTeamfromAbb, GetPos
from datetime import date

def ProcessRSLog(filename, con):
    text = open(filename)
    pbp = PlayByPlay()
    currentGame = None
    weather = []
    wp = ''
    lp = ''
    savep = ''
    for line in text:
        line = line.replace('!','')
        row = line.split(',')
        rowType = row[0]
        
        #Game
        if rowType == 'info':
            att = row[1]
            if att == 'visteam':
                pbp.aAbb = row[2].strip()
                if pbp.aTeam == None:
                    pbp.aTeam = GetTeamfromAbb(pbp.aAbb, con)
            elif att == 'hometeam':
                pbp.hAbb = row[2].strip()
                if pbp.hTeam == None:
                    pbp.hTeam = GetTeamfromAbb(pbp.hAbb, con)
            elif att == 'date':
                datePieces = row[2].split('/')
                gameDate = date(int(datePieces[0]),int(datePieces[1]),int(datePieces[2]))
                currentGame = Game(pbp.hTeam, pbp.aTeam, gameDate, con)
            elif att == 'starttime':
                currentGame.time = row[2].strip()
            elif att == 'winddir':
                currentGame.windDir = row[2].strip()
            elif att == 'windspeed':
                currentGame.windSpeed = int(row[2].strip())
            elif att == 'temp':
                currentGame.temp = int(row[2].strip())
            elif att == 'fieldcond':
                weather.append(row[2].strip())
            elif att == 'precip':
                weather.append(row[2].strip())
            elif att == 'sky':
                weather.append(row[2].strip())
                currentGame.weather = 'Field = '+weather[0]+', Prec = '+weather[1]+', Sky = '+weather[2]
            elif att == 'timeofgame':
                currentGame.gameLength = int(row[2].strip())
            elif att == 'umphome':
                currentGame.homeUmp = row[2].strip()
            elif att == 'wp':
                wp = row[2].strip()
            elif att == 'lp':
                lp = row[2].strip()
            elif att == 'save':
                savep = row[2].strip()
            
        #Lineup and Pitch Roster
        elif rowType == 'start':
            userID = row[1]
            playerName = row[2]
            if int(row[3]) == 0:
                team = pbp.aTeam
            else:
                team = pbp.hTeam
            playerBatNum = row[4]
            playerPos = GetPos(row[5])
            pbp.lineup[userID] = Lineup(123, team, playerName, int(playerBatNum), playerPos, userID, con)
            if playerPos == 'P':
                pitchers[userID] = PitchRoster(123, team, playerName, userID, con)
                pitchers[userID].pitcherRole = 'Starter'
                if int(row[3]) == 0:
                    awayPitcher = userID
                else:
                    homePitcher = userID