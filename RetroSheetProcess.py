from PlayByPlay import Play, PlayByPlay
from GameStats import Game
from LineupStats import Lineup
from PitchingStats import PitchRoster
from bbUtils import GetTeamfromAbb, GetPos
from datetime import date

def ProcessRSLog(filename, con):
    text = open(filename,'a')
    text.write('id,dunzo')
    text.close()
    text = open(filename,'r')
    pbp = PlayByPlay()
    currentGame = None
    gameDate = date(1500,1,1)
    weather = []
    wp = ''
    lp = ''
    savep = ''
    playInd = 0
    for line in text:
        line = line.replace('!','')
        row = line.split(',')
        rowType = row[0]
        
        #Game
        if rowType == 'info':
            att = row[1]
            if att == 'visteam':
                pbp.aAbb = row[2].strip()
                if pbp.aTeam == 0:
                    pbp.aTeam = GetTeamfromAbb(pbp.aAbb, con)
            elif att == 'hometeam':
                pbp.hAbb = row[2].strip()
                if pbp.hTeam == 0:
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
                pbp.pitchers[userID] = PitchRoster(123, team, playerName, userID, con)
                pbp.pitchers[userID].pitcherRole = 'Starter'
                if int(row[3]) == 0:
                    pbp.aPitcher = userID
                else:
                    pbp.hPitcher = userID
        
        #Plays            
        elif rowType == 'play':
            userID = row[3].strip()
            playInd += 1
            pbp.plays[playInd] = Play()
            pbp.plays[playInd].hitterID = userID
            
            #Set Inning specific variables
            innPre = 'Top' if row[2]=='0' else 'Bot'
            pbp.plays[playInd].pitcherID = pbp.hPitcher if innPre == 'Top' else pbp.aPitcher
            prevInn = pbp.inning
            pbp.inning = innPre +' '+str(row[1])
            pbp.plays[playInd].inning = pbp.inning
            if pbp.inning != prevInn:
                pbp.outs = 0
                pbp.firstBase = None
                pbp.secondBase = None
                pbp.thirdBase = None
            pbp.plays[playInd].startSit = pbp.ReturnSit()
            
            #Deal with Pitches
            pbp.plays[playInd].pitchSeq = row[5]
            pbp.plays[playInd].strikes = int(row[4][1])
            pbp.plays[playInd].balls = int(row[4][0])
            pbp.ProcessRSPlay(row[6],playInd)
            pbp.plays[playInd].endSit = pbp.ReturnSit()
            pbp.plays[playInd].playNum = playInd
        #Substitutions
        elif rowType == 'sub':
            #Pitching Change
            if int(row[5]) == 1:
                p = pbp.hPitcher if int(row[3]) == 1 else pbp.aPitcher
                pbp.pitchers[p].IP += int(pbp.inning.split(' ')[-1])-1
                for x in pbp.pitchers.keys():
                    if pbp.pitchers[x].team == pbp.pitchers[p].team and x != p:
                        pbp.pitchers[p].IP -= float(pbp.pitchers[x].IP)
                pbp.pitchers[p].IP += int(pbp.outs)/3.0
                if int(row[3]) == 1:
                    pbp.hPitcher = row[1]
                    team = pbp.hTeam
                else:
                    pbp.aPitcher = row[1]
                    team = pbp.aTeam
                pbp.pitchers[row[1]] = PitchRoster(123, team, row[2], row[1], con)
                pbp.pitchers[row[1]].pitcherRole = 'Reliever'
                pbp.lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), 'P', row[1], con)
               
            #Pinch Hitter
            elif int(row[5]) == 11:
                team = pbp.hTeam if int(row[3])==1 else pbp.aTeam
                pbp.lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), 'PH', row[1], con)
                
            #Pinch Runner
            elif int(row[5]) == 12:
                team = pbp.hTeam if int(row[3])==1 else pbp.aTeam
                pbp.lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), 'PR', row[1], con)
                playInd += 1
                pbp.plays[playInd] = Play()
                pbp.plays[playInd].hitterID = row[1]
                pbp.plays[playInd].inning = pbp.inning
                pbp.plays[playInd].pitcherID = pbp.hPitcher if pbp.inning[:3] == 'Top' else pbp.aPitcher
                pbp.plays[playInd].startSit = pbp.plays[playInd].endSit = pbp.ReturnSit()
                pbp.plays[playInd].playType = 'Pinch Runner'
                for guy in pbp.lineup.keys():
                    if pbp.lineup[guy].team == team and pbp.lineup[guy].player_bat_num == int(row[4]) and guy != row[1]:
                        replacee = guy
                        if pbp.firstBase != None and pbp.firstBase[1] == replacee:
                            pbp.firstBase = [playInd, row[1]]
                        elif pbp.secondBase != None and pbp.secondBase[1] == replacee:
                            pbp.secondBase = [playInd, row[1]]
                        elif pbp.thirdBase != None and pbp.thirdBase[1] == replacee:
                            pbp.thirdBase = [playInd, row[1]]
                            
            #Defensive Sub
            else:                            
               team = pbp.hTeam if int(row[3])==1 else pbp.aTeam
               playerPos = GetPos(int(row[5]))
               if row[1] not in pbp.lineup.keys():
                   pbp.lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), playerPos, row[1], con)
                   
        #Earned Runs
        elif rowType == 'data':
            if row[1] == 'er':
                pbp.pitchers[row[2]].earnedRuns += int(row[3])
                
        elif rowType == 'id':
            print(pbp.aAbb+' at '+pbp.hAbb+' - '+gameDate.isoformat())
            if gameDate != date(1500,1,1):
                currentGame.InsertBlankGame(con)
                currentGame.totalInnings = int(pbp.inning.split(' ')[-1])
                pbp.pitchers[pbp.hPitcher].IP += currentGame.totalInnings
                pbp.pitchers[pbp.aPitcher].IP += currentGame.totalInnings
                if pbp.inning[:3] == 'Top':
                    pbp.pitchers[pbp.aPitcher].IP -= 1
                elif pbp.inning[:3] == 'Bot':
                    pbp.pitchers[pbp.aPitcher].IP -= float(3-int(pbp.outs))/3.0
                    
                #Go through Plays
                for x in pbp.plays.values():
                    if x.playType not in ('No Play','Stolen Base','Caught Stealing','Pick Off','Balk','Passed Ball','Wild Pitch','Defensive Indifference','Error on Foul', 'Unknown Runner Activity'):
                        x.CalcPitches()
                        pbp.lineup[x.hitterID].PA += 1
                        pbp.pitchers[x.pitcherID].ContactStrikes += x.contactX
                        pbp.pitchers[x.pitcherID].SwingStrikes += x.swingX
                        pbp.pitchers[x.pitcherID].LookStrikes += x.lookX
                        pbp.pitchers[x.pitcherID].Strikes += x.lookX + x.swingX + x.contactX
                        pbp.pitchers[x.pitcherID].Balls += x.balls
                        pbp.pitchers[x.pitcherID].pitchCount += x.lookX + x.swingX + x.contactX + x.balls
                        if x.ballType in ('Ground Ball', 'Bunt Bround Ball'):
                            pbp.pitchers[x.pitcherID].GB += 1
                        elif x.ballType in ('Line Drive', 'Bunt Line Drive'):
                            pbp.pitchers[x.pitcherID].LD += 1
                        elif x.ballType in ('Fly Ball','Pop Up','Bunt Pop'):
                            pbp.pitchers[x.pitcherID].FB += 1
                        if x.playType in ('Strikeout','Out','Double Play','Triple Play', "Fielders Choice",'Reach On Error','Single','Double','Ground Rule Double','Triple','Home Run'):
                            pbp.lineup[x.hitterID].AB += 1
                            if x.playType in ('Single', 'Double', 'Ground Rule Double', 'Triple', 'Home Run'):
                                pbp.lineup[x.hitterID].Hits += 1
                                pbp.pitchers[x.pitcherID].Hits += 1
                                if x.playType == 'Single':
                                    pbp.lineup[x.hitterID].Single += 1
                                elif x.playType in ('Double', 'Ground Rule Double'):
                                    pbp.lineup[x.hitterID].Double += 1
                                elif x.playType == 'Triple':
                                    pbp.lineup[x.hitterID].Triple += 1
                                elif x.playType == 'Home Run':
                                    pbp.lineup[x.hitterID].HR += 1
                            elif x.playType == 'Strikeout':
                                pbp.pitchers[x.pitcherID].K += 1
                        else:
                            if x.playType in ('Walk', 'Intentional Walk'):
                                pbp.pitchers[x.pitcherID].BB += 1
                                pbp.lineup[x.hitterID].BB += 1
                                pbp.pitchers[x.pitcherID].pitchCount += 1
                            elif x.playType == 'Hit By Pitch':
                                pbp.pitchers[x.pitcherID].HBP += 1
                                pbp.lineup[x.hitterID].HBP += 1
                    if x.inning[:3] == 'Top':
                        if x.hit:
                            currentGame.awayHits +=1
                        currentGame.awayRuns = x.runsScored
                    else:
                        if x.hit:
                            currentGame.homeHits +=1
                        currentGame.homeRuns = x.runsScored
                    x.gameKey = currentGame.gameKey

                    x.InsertPlay(con)
                if currentGame.homeRuns > currentGame.awayRuns:
                    currentGame.homeTeamWin = True
                elif currentGame.homeRuns == currentGame.awayRuns:
                    currentGame.tie = True
                currentGame.UpdateStats(con)
                
                #Go Through Pitchers
                for x in pbp.pitchers.keys():
                    if x == wp:
                        pbp.pitchers[x].Win = True
                    elif x == lp:
                        pbp.pitchers[x].Loss = True
                    elif x == savep:
                        pbp.pitchers[x].Save = True
                    if pbp.pitchers[x].team == pbp.pitchers[pbp.hPitcher].team and x != pbp.hPitcher:
                        pbp.pitchers[pbp.hPitcher].IP -= float(pbp.pitchers[x].IP)
                    if pbp.pitchers[x].team == pbp.pitchers[pbp.aPitcher].team and x != pbp.aPitcher:
                        pbp.pitchers[pbp.aPitcher].IP -= float(pbp.pitchers[x].IP)
                    if pbp.pitchers[x].IP == 9.0:
                        pbp.pitchers[x].CG = True
                        if pbp.pitchers[x].Runs == 0:
                            pbp.pitchers[x].SO = True
                            if pbp.pitchers[x].Hits == 0:
                                pbp.pitchers[x].NH = True
                    pbp.pitchers[x].gameKey = currentGame.gameKey
                    pbp.pitchers[x].InsertRosterRow(con)
                    
                #Go Through Hitters
                for x in pbp.lineup.keys():
                    pbp.lineup[x].game = currentGame.gameKey
                    pbp.lineup[x].InsertLineupRow(con)
                    
            #Clear Variables
            rplays = pbp.plays
            rlineup = pbp.lineup
            rpitchers = pbp.pitchers
            rgame = currentGame                    
                
            pbp = PlayByPlay()
            pbp.lineup = {}
            pbp.plays = {}
            pbp.pitchers = {}
            currentGame = None
            gameDate = date(1500,1,1)
            weather = []
            wp = ''
            lp = ''
            savep = ''
            playInd = 0
    return rplays, rlineup, rpitchers, rgame
                