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
    currentGame = None
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
    wp = ''
    lp = ''
    sp = ''
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
            elif att == 'hometeam':
                homeTeamAbb = row[2].strip() 
                if homeTeam == None:
                    homeTeam = GetTeamfromAbb(homeTeamAbb, con)
            elif att == 'date':
                datePieces = row[2].split('/')
                gameDate = date(int(datePieces[0]),int(datePieces[1]),int(datePieces[2]))
            elif att == 'starttime':
                gameTime = row[2].strip()
            elif att == 'winddir':
                windDir = row[2].strip()
            elif att == 'windspeed':
                windSpeed = int(row[2])
            elif att == "temp":
                gameTemp = int(row[2])
            elif att == "fieldcond":
                weather.append(row[2].strip())
            elif att == "precip":
                weather.append(row[2].strip())
            elif att == "sky":
                weather.append(row[2].strip())
            elif att == "timeofgame":
                gameLength = int(row[2])
            elif att == "umphome":
                homeUmp = row[2].strip()
            elif att == "wp":
                wp = row[2].strip()
            elif att == "lp":
                lp = row[2].strip()
            elif att == "save":
                sp = row[2].strip()
                
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
            currentGame.homeTeamWin = False 
            currentGame.tie = False
            currentGame.homeUmp = homeUmp
            
        #Get Lineups and Pitchers
            userID = row[1]
            playerName = row[2]
            if int(row[3]) == 0:
                team = awayTeam
            else:
                team = homeTeam
            playerBatNum = row[4]
            playerPos = GetPos(row[5])
            if playerPos != 'P':
                lineup[userID] = Lineup(123, team, playerName, int(playerBatNum), playerPos, userID, con)
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
           
            
        #Clear Variables
            batEvent = ''
            runEvent = ''
            batRunner = False
            runsScored = 0
            play = ''
            ballType = ''
            ballLoc = ''
            contactStrikes = 0
            lookStrikes = 0
            swingStrikes = 0
            innPre = 'Top' if row[2]== '0' else 'Bot'
            prevInn = inning
            inning = innPre + ' '+str(row[1])
            #Inning Changed
            if inning != prevInn:
                startSit = 0
                outs = 0
                firstBase = None
                secondBase = None
                thirdBase = None
            else:
                startSit = endSit
            plays[playInd] = PitchResult(123, row[3], pitcher, startSit)
            plays[playInd].inning = inning
            plays[playInd].hitterPANum = lineup[row[3]].PA

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
            plays[playInd].pitchSeq = pitchSeq
          
        #Events
            batEvent = row[6].split('.')[0]
            if len(row[6].split('.')) == 2:
                runEvent = row[6].split('.')[1]
            batParts = batEvent.split('/')

            
            #Figure out runners first
            if runEvent != '':
                runners = runEvent.split(';')
                for run in runners:
                    if run[:3] == '1-2':
                        secondBase = firstBase
                        firstBase = None
                    elif run[:3] == '1-3':
                        thirdBase = firstBase
                        firstBase = None
                    elif run[:3] == '1-H':
                        plays[firstBase[0]+firstBase[1]].runScored = True
                        lineup[firstBase[0]].Runs += 1
                        pitchers[currentPitcher].Runs += 1
                        runsScored += 1
                        firstBase = None
                    elif run[:3] == '2-3':
                        thirdBase = secondBase
                        secondBase = None
                    elif run[:3] == '2-H':
                        plays[secondBase[0]+secondBase[1]].runScored = True
                        lineup[secondBase[0]].Runs += 1
                        pitchers[currentPitcher].Runs += 1
                        runsScored += 1
                        secondBase = None
                    elif run[:3] == '3-H':                        
                        plays[thirdBase[0]+thirdBase[1]].runScored = True
                        lineup[thirdBase[0]].Runs += 1
                        pitchers[currentPitcher].Runs += 1
                        runsScored += 1
                        thirdBase = None
                    elif run[:3] == 'B-1':
                        firstBase = [hitterID, str(lineup[hitterID].PA)]
                        batRunner = True
                    elif run[:3] == 'B-2':
                        secondBase = [hitterID, str(lineup[hitterID].PA)]
                        batRunner = True
                    elif run[:3] == 'B-3':
                        thirdBase = [hitterID, str(lineup[hitterID].PA)]
                        batRunner = True
                    elif run[:3] == 'B-H':
                        plays[hitterID+str(lineup[hitterID].PA)].runScored = True
                        lineup[hitterID].Runs += 1
                        pitchers[currentPitcher].Runs += 1
                        runsScored += 1
                        batRunner = True
                    elif run[:2] == '1X':
                        if 'E' not in run:
                            outs += 1                        
                            firstBase = None
                        elif run[:3] == '1X2':
                            secondBase = firstBase
                            firstBase = None
                        elif run[:3] == '1X3':
                            thirdBase = firstBase
                            firstBase = None
                        elif run[:3] == '1XH':
                            plays[firstBase[0]+firstBase[1]].runScored = True
                            lineup[firstBase[0]].Runs += 1
                            pitchers[currentPitcher].Runs += 1
                            runsScored += 1
                            firstBase = None
                    elif run[:2] == '2X':
                        if 'E' not in run:
                            outs += 1                        
                            secondBase = None
                        elif run[:3] == '2X3':
                            thirdBase = secondBase
                            secondBase = None
                        elif run[:3] == '2XH':
                            plays[secondBase[0]+secondBase[1]].runScored = True
                            lineup[secondBase[0]].Runs += 1
                            pitchers[currentPitcher].Runs += 1
                            runsScored += 1
                            secondBase = None
                    elif run[:2] == '3X':
                        if 'E' not in run:
                            outs += 1                        
                            thirdBase = None
                        elif run[:3] == '3XH':
                            plays[thirdBase[0]+thirdBase[1]].runScored = True
                            lineup[thirdBase[0]].Runs += 1
                            pitchers[currentPitcher].Runs += 1
                            runsScored += 1
                            thirdBase = None 
                    elif run[:2] == 'BX':
                        outs += 1
                if batParts[0] not in ('WP','PB','BK'):
                    if 'E' not in runEvent:
                        lineup[hitterID].RBI += runsScored
                        plays[playInd].RBI = runsScored
                                         
                        
            #Non-Plays (like before subs)
            if batParts[0].strip() == 'NP':
                lineup[hitterID].PA -=1
                play = 'No Play'
                
            #Flys/Unassisted Grounders
            if re.match('[0-9]$',batParts[0]) != None:
                lineup[hitterID].AB += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                plays[playInd].strikeCount = strikeCount
                plays[playInd].ballCount = ballCount
                outs += 1
                if 'SF' in batParts:
                    lineup[hitterID].AB -= 1
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
                        
            #Groundball outs for Batter
            if re.match('[0-9]{2,}$',batParts[0]) != None:
                lineup[hitterID].AB += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                plays[playInd].strikeCount = strikeCount
                plays[playInd].ballCount = ballCount
                outs += 1
                for mod in batParts:
                    if 'SH' in mod:
                        lineup[hitterID].AB -= 1
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
                        
            #Groudball outs for Runners
            if re.match('[0-9]\([1-3]\)',batParts[0]) != None or re.match('[0-9][0-9]\([1-3]\)',batParts[0]) != None:
                lineup[hitterID].AB += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                plays[playInd].strikeCount = strikeCount
                plays[playInd].ballCount = ballCount
                if '(1)' in batParts[0]:
                    outs += 1
                    firstBase = None
                elif '(2)' in batParts[0]:
                    outs += 1
                    secondBase = None
                elif '(3)' in batParts[0]:
                    outs += 1
                    thirdBase = None
                for mod in batParts:
                    if mod.strip() == 'GDP':
                        play = 'GDP'
                        ballLoc = batParts[0][0]
                        ballType = 'Ground Ball'
                        pitchers[currentPitcher].GB += 1
                        outs +=1
                        break
                    elif 'BG' in mod:
                        ballType = 'Bunt'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].GB += 1
                    elif 'G' in mod:
                        ballType = 'Ground Ball'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].GB += 1
                    elif 'L' in mod:
                        ballType = 'Line Drive'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].LD += 1
                    elif 'F' in mod:
                        ballType = 'Flyball'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].FB += 1
                    elif 'BP' in mod:
                        ballType = 'Bunt Pop'
                        ballLoc = batParts[0][0]
                        pitchers[currentPitcher].FB += 1
                    firstBase = [hitterID, str(lineup[hitterID].PA)]
                    play = 'FC'
            
            #Hits         
            if re.match('[SDT][0-9]',batParts[0]) != None:
                plays[playInd].hit = True
                lineup[hitterID].AB += 1
                lineup[hitterID].Hits += 1
                pitchers[currentPitcher].Hits += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                plays[playInd].strikeCount = strikeCount
                plays[playInd].ballCount = ballCount
                if batParts[0][0] == 'S':
                    play = 'Single'
                    lineup[hitterID].Single += 1
                    if batRunner == False:
                        firstBase = [hitterID, str(lineup[hitterID].PA)]
                elif batParts[0][0] == 'D':
                    play = 'Double'
                    lineup[hitterID].Double += 1
                    if batRunner == False:
                        secondBase = [hitterID, str(lineup[hitterID].PA)]
                elif batParts[0][0] == 'T':
                    play = 'Triple'
                    lineup[hitterID].Triple += 1
                    if batRunner == False:
                        thirdBase = [hitterID, str(lineup[hitterID].PA)]
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
                plays[playInd].Hit = True
                lineup[hitterID].AB += 1
                lineup[hitterID].Hits += 1
                lineup[hitterID].Runs += 1
                lineup[hitterID].RBI += 1
                runsScored += 1
                lineup[hitterID].HR += 1
                pitchers[currentPitcher].Hits += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                pitchers[currentPitcher].Runs += 1
                plays[playInd].strikeCount = strikeCount
                plays[playInd].ballCount = ballCount
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
            if re.match('^K', batParts[0]) != None:
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                lineup[hitterID].AB += 1
                outs += 1
                play = 'Strikeout'
                ballType = ''
                ballLoc = ''
                pitchers[currentPitcher].K += 1

            #Fielder's Choice
            if re.match('FC[0-9]$', batParts[0]) != None:
                lineup[hitterID].AB += 1
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount
                if batRunner == False:
                    firstBase = [hitterID,str(lineup[hitterID].PA)]
                play = 'FC'
                ballLoc = batParts[0][-1]
                
            #Triple Plays
            #Ground Rule Doubles
            #Hit By Pitch
            if batParts[0].strip() == 'HP':
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount+1
                lineup[hitterID].HBP += 1
                lineup[hitterID].AB -= 1
                pitchers[currentPitcher].HBP += 1
                play = 'Hit By Pitch'
                ballType = ''
                ballLoc = ''
                firstBase = [hitterID, str(lineup[hitterID].PA)]
                
            #Walk
            if batParts[0].strip() == 'W' or batParts[0].strip() == 'IW':
                plays[playInd].contactStrikes += contactStrikes
                plays[playInd].swingStrikes += swingStrikes
                plays[playInd].lookStrikes += lookStrikes
                pitchers[currentPitcher].ContactStrikes += contactStrikes
                pitchers[currentPitcher].SwingStrikes += swingStrikes
                pitchers[currentPitcher].LookStrikes += lookStrikes
                pitchers[currentPitcher].Strikes += lookStrikes + swingStrikes + contactStrikes
                pitchers[currentPitcher].Balls += ballCount
                pitchers[currentPitcher].pitchCount += contactStrikes + swingStrikes + lookStrikes + ballCount+1
                lineup[hitterID].BB += 1
                pitchers[currentPitcher].BB += 1
                play = 'Walk'
                ballType = ''
                ballLoc = ''
                firstBase = [hitterID, str(lineup[hitterID].PA)]
            #Stolen Base
            if re.match('SB[23H]',batParts[0]) != None:
                lineup[hitterID].PA -= 1
                if batParts[0].strip() == 'SB2':
                    lineup[firstBase[0]].SB += 1
                    secondBase = firstBase
                    firstBase = None
                elif batParts[0].strip() == 'SB3':
                    lineup[secondBase[0]].SB += 1
                    thirdBase = secondBase
                    secondBase = None
                elif batParts[0].strip() == 'SBH':
                    plays[thirdBase[0]+thirdBase[1]].runScored = True
                    lineup[thirdBase[0]].SB += 1
                    lineup[thirdBase[0]].Runs += 1
                    runsScored += 1
                    thirdBase = None
            #Caught Stealing
            if re.match('CS[23H]',batParts[0]) != None:
                if batParts[0][:2] == 'CS':
                    play = 'Caught Stealing'
                    lineup[hitterID].PA -= 1
                    ballType = ''
                    ballLoc = ''
                if 'CS2' in batParts[0]:
                    lineup[firstBase[0]].CS += 1
                    firstBase = None
                elif 'CS3' in batParts[0]:
                    lineup[secondBase[0]].CS += 1
                    secondBase = None
                elif 'CSH' in batParts[0]:
                    lineup[thirdBase[0]].CS += 1
                    thirdBase = None  
            #Balk
            #Throw Out
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
            plays[playInd].ballLoc = ballLoc
            plays[playInd].ballType = ballType
            plays[playInd].resultOuts = outs - (startSit/10)
            plays[playInd].endSit = endSit
            #Add play variables
            
        #Handle Pinch Hits, Pitcher Changes, and other subs
        elif rowType == 'sub':
            #Pitcher Change
            if int(row[5]) == 1:
                #Home Team
                if int(row[3]) == 1:
                    pitchers[homePitcher].IP += int(inning[-1])-1
                    for x in pitchers.keys():
                        if pitchers[x].team == pitchers[homePitcher].team and x != homePitcher:
                            pitchers[homePitcher].IP-=int(pitchers[x].IP)
                    pitchers[homePitcher].IP += int(outs)/3.0
                    homePitcher = row[1]
                    pitchers[homePitcher] = PitchRoster(123, homeTeam, row[2], row[1], con)
                    pitchers[homePitcher].pitcherRole = 'Reliever'
                #Away Team  
                else:
                    pitchers[awayPitcher].IP = int(inning[-1])-1
                    for x in pitchers.keys():
                        if pitchers[x].team == pitchers[awayPitcher].team and x != awayPitcher:
                            pitchers[awayPitcher].IP-=float(pitchers[x].IP)
                    pitchers[awayPitcher].IP += float(outs)/3.0
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
                        if firstBase != None and firstBase[0] == replacee:
                            firstBase = lineup[row[1]]
                        elif secondBase != None and secondBase[0] == replacee:
                            secondBase = lineup[row[1]]
                        elif thirdBase != None and thirdBase[0] == replacee:
                            thirdBase = lineup[row[1]]
                
                pass #find batter with same batnum
            #Defensive Sub
            else:
                team = homeTeam if int(row[3])==1 else awayTeam
                playerPos = GetPos(row[5])
                lineup[row[1]] = Lineup(123, team, row[2], int(row[4]), playerPos, row[1], con)
        elif rowType == 'data':
            if row[1] == 'er':
                pitchers[row[2]].earnedRuns += int(row[3])
        #New game found, reset everything   
        elif rowType == 'id':
            #Wrap up Game
            if gameDate != None:
                currentGame.totalInnings = int(inning.split(' ')[-1])
                pitchers[homePitcher].IP += currentGame.totalInnings
                pitchers[awayPitcher].IP += currentGame.totalInnings
                for x in pitchers.keys():
                    print(wp, lp, sp, x, x==lp, x==wp, x==sp)
                    if x == wp:
                        pitchers[x].Win = True
                    elif x == lp:
                        pitchers[x].Loss = True
                    elif x == sp:
                        pitchers[x].Save = True
                    elif pitchers[x].team == pitchers[homePitcher].team and x != homePitcher:
                        pitchers[homePitcher].IP-=float(pitchers[x].IP)
                    elif pitchers[x].team == pitchers[awayPitcher].team and x != awayPitcher:
                        pitchers[awayPitcher].IP-=float(pitchers[x].IP)
                if inning[:3] == 'Top':
                    pitchers[awayPitcher].IP -= 1
                for x in lineup.keys():
                    if lineup[x].team == homeTeam:
                        currentGame.homeHits += lineup[x].Hits
                        currentGame.homeRuns += lineup[x].Runs
                    else:
                        currentGame.awayHits += lineup[x].Hits
                        currentGame.awayRuns += lineup[x].Runs
                if currentGame.homeRuns > currentGame.awayRuns:
                    homeTeamWin = True
                elif currentGame.homeRuns == currentGame.awayRuns:
                    tie = True
                #currentGame.GetGamePark(gameDate, con)
                #currentGame.InsertStats(con)
                gameKey = currentGame.gameKey
                for x in pitchers.keys():
                    if pitchers[x] == 9.0:
                        pitchers[x].CG = True
                        if pitchers[x].Runs == 0:
                            pitchers[x].SO = True
                            if pitchers[x].Hits == 0:
                                pitchers[x].NH = True
                    pitchers[x].gameKey = gameKey
                    pitchers[x].InsertRosterRow(con)
                for x in lineup.keys():
                    lineup[x].game = gameKey
                    lineup[x].InsertLineupRow(con)
                for x in plays.keys():
                    plays[x].gameKey = gameKey
                    plays[x].InsertPlay(con)
            #Insert Game, Lineup, Pitch Roster, and Play stuff into DB
            
            #Reset variables
            rcurrentGame = currentGame
            rplays = plays
            rlineup = lineup
            rpitchers = pitchers
            lineup = {}
            pitchers = {}
            plays = {}
            currentGame = None
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
            wp = ''
            lp = ''
            sp = ''
            
    return rplays, rpitchers, rlineup, rcurrentGame
    


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
        
    def InsertPlay(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "LINEUP" VALUES (%s, %s, %s, %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' % \
        (self.game, self.team, self.player, self.player_bat_num, self.player_pos, self.AB, self.Hits, self.BB, self.HBP, self.Runs, self.RBI, self.Single, self.Double, self.Triple, self.HR, self.SB, self.CS, self.PA)
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            return True
        return False
    
    def CheckForRow(self, con):
        cur = con.cursor()
        checkSQL = 'select 1 from "LINEUP" where "GAME_KEY" = %s and "PLAYER_KEY" = %s' % (self.game, self.player)
        cur.execute(checkSQL)
        results = cur.fetchall()
        if len(results) == 0:
            return False
        else:
            return True
    
        
    
        
    
