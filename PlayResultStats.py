from bbUtils import GetGameKeys, GetHitterKeyfromLU, GetTeamfromAbb, GetPos
import psycopg2
import re
from datetime import date
from GameStats import Game
from LineupStats import Lineup
from PitchingStats import PitchRoster

def ProcessPlayLog(filename, con):
    text = open(filename)
    lineup = {}
    pitchers = {}
    plays = {}
    endSit = 1
    startSit = 0
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
    awayPitcher = ''
    homePitcher = ''
    inning = ''
    for line in text:
        row = line.split(',')
        rowType = row[0]
         
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
                weather.append(row[2])
            elif att == "precip":
                weather.append(row[2])
            elif att == "sky":
                weather.append(row[2])
            elif att == "timeofgame":
                gameLength = int(row[2])
            elif att == "umphome":
                homeUmp = row[2]
                
        elif rowType == 'start':
        #First set all the GAME stuff
            currentGame = Game(int(homeTeam), int(awayTeam), gameDate, con)
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
            
        #Get Lineups and Pitchers
            userID = row[1]
            playerName = row[2]
            if row[3] == 0:
                team = awayTeam
            else:
                team = homeTeam
            playerBatNum = row[4]
            playerPos = GetPos(row[5])
            if playerPos != 'P':
                lineup[userID] = Lineup(123, team, playerName, playerBatNum, playerPos, userID, con)
            else:
                pitchers[userID] = PitchRoster(123, team, playerName, userID, con)
                pitchers[userID].pitcherRole = 'Starter'
                if int(row[3]) == 0:
                    awayPitcher = userID
                else:
                    homePitcher = userID
                
        #Grab play-by-play stuff
        elif rowType == 'play':
        #Create PitchResult
            lineup[row[3]].PA += 1
            playInd = lineup[row[3]].userID + str(lineup[row[3]].PA)
            pitcher = homePitcher if row[2] == '1' else awayPitcher
            plays[playInd] = PitchResult(123, lineup[row[3]].userID, pitcher, startSit)           
            
        #Clear Variables
            batEvent = ''
            runEvent = ''
            play = ''
            ballType = ''
            ballLoc = ''
            contactStrikes = 0
            lookStrikes = 0
            swingStrikes = 0
            outs = 0
            firstBase = None
            secondBase = None
            thirdBase = None
            innPre = 'Top' if row[2]== '0' else 'Bot'
            prevInn = inning
            inning = innPre + ' '+str(row[1])
            plays[playInd].inning = inning
            #Inning Changed
            if inning != prevInn:
                startSit = 0
                plays[playInd].startSit = startSit
            else:
                startSit = endSit
            plays[playInd].startSit = startSit
            
        #Pitches
            pitchSeq = row[5]
            hitterID = row[3]
            if innPre == 'Top':
                currentPitcher = homePitcher
            else:
                currentPitcher = awayPitcher
            ballCount = int(row[4][0])
            strikeCount= int(row[4][1])
            for pitch in pitchSeq:
                if pitch in ('F','X','L','O','R','T','Y'):
                    contactStrikes += 1
                elif pitch == 'C':
                    lookStrikes += 1
                elif pitch in ('S','M','Q'):
                    swingStrikes += 1
          
        #Events
            batEvent = row[6].split('.')[0]
            if len(row[6].split('.')) == 2:
                runEvent = row[6].split('.')[1]
            batParts = batEvent.split('/')
            print(batParts[0])
            #Flys/Unassisted Grounders
            if re.match('[0-9]',batParts[0]) != None:
                lineup[hitterID].AB += 1
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += strikeCount
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                outs += 1
                if 'SF' in batParts:
                    play = 'Sac Fly'
                    if 'F' in batParts:
                        ballType = 'Flyball'
                        pitchers[currentPitcher].FB += 1
                    elif 'L' in batParts:
                        ballType = 'Line Drive'
                        pitchers[currentPitcher].LD += 1
                    else:
                        ballType = 'Unknown'
                else:
                    for mod in batParts:
                        if 'F' in mod:
                            play = 'Flyout'
                            ballType = 'Flyball'
                            ballLoc = batParts[0]
                            pitchers[currentPitcher].FB += 1
                            break
                        elif 'L' in mod:
                            play = 'Lineout'
                            ballType = 'Line Drive'
                            ballLoc = batParts[0]
                            pitchers[currentPitcher].LD += 1
                            break
                        elif 'G' in mod:
                            play = 'Groundout'
                            ballType = 'Ground Ball'
                            ballLoc = batParts[0]
                            pitchers[currentPitcher].GB += 1
                            break
                        play = 'Out'
                        ballLoc = batParts[0]
                        ballType = 'Unknown'
                        
            #Groundball outs
            if re.match('[0-9]{2,}',batParts[0]) != None:
                lineup[hitterID].AB += 1
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += strikeCount
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                outs += 1
                for mod in batParts:
                    if 'SH' in mod:
                        play = 'Sacrifice'
                        ballType = 'Unknown'
                        ballLoc = batParts[0][0]
                    elif 'BG' in mod:
                        play = 'Groundout'
                        ballType = 'Bunt'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].GB += 1
                    elif 'G' in mod:
                        play = 'Groundout'
                        ballType = 'Ground Ball'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].GB += 1
                        
            #Hits         
            if re.match('[SDT][0-9]',batParts[0]) != None:
                lineup[hitterID].AB += 1
                lineup[hitterID].Hits += 1
                pitchers[currentPitcher].Hits += 1
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += strikeCount
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                if batParts[0][0] == 'S':
                    play = 'Single'
                    lineup[hitterID].Single += 1
                elif batParts[0][0] == 'D':
                    play = 'Double'
                    lineup[hitterID].Double += 1
                elif batParts[0][0] == 'T':
                    play = 'Triple'
                    lineup[hitterID].Triple += 1
                for mod in batParts:
                    if 'BG' in mod:
                        ballType = 'Bunt'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].GB += 1
                    elif 'G' in mod:
                        ballType = 'Ground Ball'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].GB += 1
                    elif 'L' in mod:
                        ballType = 'Line Drive'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].LD += 1
                    elif 'F' in mod:
                        ballType = 'Flyball'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].FB += 1
                    elif 'BP' in mod:
                        ballType = 'Bunt Pop'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].FB += 1
            
            #Home Runs
            if re.match('HR',batParts[0]) != None:
                lineup[hitterID].AB += 1
                lineup[hitterID].Hits += 1
                lineup[hitterID].HR += 1
                pitchers[currentPitcher].Hits += 1
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += strikeCount
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                play = 'Home Run'
                for mod in batParts:
                    if 'BG' in mod:
                        ballType = 'Bunt'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].GB += 1
                    elif 'G' in mod:
                        ballType = 'Ground Ball'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].GB += 1
                    elif 'L' in mod:
                        ballType = 'Line Drive'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].LD += 1
                    elif 'F' in mod:
                        ballType = 'Flyball'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].FB += 1
                    elif 'BP' in mod:
                        ballType = 'Bunt Pop'
                        ballLoc = batParts[0][1]
                        pitchers[currentPitcher].FB += 1   
            
            #StrikeOuts
            #Ground Double Plays
            #Line Double Plays
            #Fielder's Choice and Force Outs
            #Triple Plays
            #Ground Rule Doubles
            #Hit By Pitch
            #Walk
            #Intentional Walk
            #Stolen Base
            #Caught Stealing
            #Balk
            #Throw Out
            print(play)
        #Determine End Situation
            if outs >= 3:
                endSit = 30
            elif outs != startSit/10:
                endSit = outs * 10
                
            if firstBase != None:
                endSit += 1
            if secondBase != None:
                endSit += 2
            if thirdBase != None:
                endSit += 4
            plays[playInd].playType = play
        #Handle Pinch Hits, Pitcher Changes, and other subs
        elif rowType == 'sub':
            #Pitcher Change
            if int(row[5]) == 1:
                #Home Team
                if row[3] == 1:
                    pitchers[homePitcher].IP = int(inning[-1])-1
                    pitchers[homePitcher].IP += int(outs)/3.0
                    homePitcher = row[1]
                    pitchers[homePitcher] = PitchRoster(123, homeTeam, row[2], row[1], con)
                    pitchers[homePitcher].pitcherRole = 'Reliever'
                #Away Team  
                else:
                    pitchers[awayPitcher].IP = int(inning[-1])-1
                    pitchers[awayPitcher].IP += int(outs)/3.0
                    awayPitcher = row[1]
                    pitchers[awayPitcher] = PitchRoster(123, awayTeam, row[2], row[1], con)
                    pitchers[awayPitcher].pitcherRole = 'Reliever'
            #Pinch Hitter
            elif int(row[5]) == 11:                   
                team = homeTeam if int(row[3])==1 else awayTeam
                lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), 'PH', row[1], con)
            #Pinch Runner
            elif int(row[5]) == 12:
                batnum = int(row[4])
                team = homeTeam if int(row[3])==1 else awayTeam
                lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), 'PR', row[1], con)
                for guy in lineup.keys():
                    if lineup[guy].team == team and lineup[guy].player_bat_num == batnum and guy != row[1]:
                        replacee = lineup[guy]
                        if firstBase == replacee:
                            firstBase = lineup[row[1]]
                        elif secondBase == replacee:
                            secondBase = lineup[row[1]]
                        elif thirdBase == replacee:
                            thirdBase = lineup[row[1]]
                
                pass #find batter with same batnum
            #Defensive Sub
            else:
                team = homeTeam if int(row[3])==1 else awayTeam
                playerPos = GetPos(row[5])
                lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), playerPos, row[1], con)
                    
        #New game found, reset everything   
        elif rowType == 'id':
            pass
        #Insert Game, Lineup, Pitch Roster, and Play stuff into DB
            
        #Reset variables
    return plays
    


class PitchResult:
    gameKey = 0 #done
    hitterID = ''#done
    pitcherID = '' #done
    startSit = 0
    inning = '' #done
    hitterPANum = 0
    strikeCount = 0 #done
    ballCount = 0 #done
    pitchSeq = '' #done
    contactStrikes = 0 #done
    swingStrikes = 0 #done
    lookStrikes = 0 #done
    playType = '' #Event
    hit = False #Event
    resultOuts = 0 #Event
    endSit = 0 #Event
    ballLoc = ''
    ballType = ''
    runScored = False
    RBI = 0
    
    def __init__(self, gk, hk, pk, sk):
        self.gameKey = gk
        self.hitterID = hk
        self.pitcherID = pk
        self.startSituationKey = sk
        
    
        
    
        
    
