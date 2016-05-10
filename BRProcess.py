from datetime import date
from bbUtils import GetTeamfromAbb, ConvertTeamAbb
from BRParser import GameTeamsParser, GameTimeParser, GameWeatherParser, GameUmpParser, GameWinLossSaveParser, \
    BRLineupParser, BRPitcherParser,  BRPlayParser, BRBatterParser
from GameStats import Game
from LineupStats import Lineup
from PitchingStats import PitchRoster
from PlayByPlay import Play, PlayByPlay
import re


def abb(name):
    x = name.split(' ',1)
    x = x[0][0]+'. '+x[1]
    return x


def ProcessBRPage(filename, con):
    dateStr = filename.split('_')[-1]
    gameDate = date(int(dateStr[:4]),int(dateStr[4:6]),int(dateStr[6:8]))
    html = open(filename).read().decode('utf-8').replace('&#183;','*')
    pbp = PlayByPlay()
    pbp.inning = ''
    playNum = 1
    playInd = 0
    
    #Game Stuff
    b = GameTeamsParser()
    b.feed(html)
    pbp.hAbb = ConvertTeamAbb('BR',b.homeTeamAbb)
    pbp.aAbb = ConvertTeamAbb('BR',b.awayTeamAbb)
    pbp.hTeam = GetTeamfromAbb(pbp.hAbb, con)
    pbp.aTeam = GetTeamfromAbb(pbp.aAbb, con)
    currentGame = Game(pbp.hTeam, pbp.aTeam, gameDate, con)
    b = GameTimeParser()
    b.feed(html)
    currentGame.time = b.time
    lengthStr = b.gamelen.split(':')
    currentGame.gameLength += int(lengthStr[0]) * 60 + int(lengthStr[1])
    b = GameWeatherParser()
    b.feed(html)
    currentGame.temp = int(re.search(': -?([0-9]{2}) F', b.weather).group(1))
    currentGame.windSpeed = int(re.search('Wind ([0-9]{1,2})mph', b.weather, flags=re.IGNORECASE).group(1))
    windDir = re.search('mph ([^,]*),', b.weather, flags=re.IGNORECASE).group(1)
    if windDir == 'out to Centerfield':
        windDir = 'tocf'
    elif windDir == 'out to Rightfield':
        windDir = 'torf'
    elif windDir == 'out to Leftfield':
        windDir = 'tolf'
    elif windDir == 'from Left to Right':
        windDir = 'ltor'
    elif windDir == 'from Right to Left':
        windDir = 'rtol'
    elif windDir == 'in from Centerfield':
        windDir = 'fromcf'
    elif windDir == 'in from Rightfield':
        windDir = 'fromrf'
    elif windDir == 'in from Leftfield':
        windDir = 'fromlf'
    weatherStr = b.weather.split(',')
    if len(weatherStr) < 4:
        precip = 'unknown'
        sky = weatherStr[-1].replace('.','').lower()
    else:
        precip = weatherStr[-1].replace('.','').lower()
        sky = weatherStr[-2].lower()
    field = b.field.lower() if (b.field != '') else 'unknown'
    currentGame.weather = 'Field = '+field+', Prec = '+precip+', Sky = '+sky
    b = GameUmpParser()
    b.feed(html)
    currentGame.homeUmp = b.homeump
    
    #Lineups
    b = GameWinLossSaveParser()
    b.feed(html)
    winPitch = abb(b.winPitch)
    lossPitch = abb(b.lossPitch)
    savePitch = '' if len(b.savePitch) == 0 else abb(b.savePitch)
    b = BRLineupParser()
    b.feed(html)
    for line in b.lineup:
        if len(line) == 6 and line[0].isdigit():
            aBatNum = int(line[0])
            aUID = str(line[1])
            aName = str(line[2])
            aPos = str(line[3]).strip()
            hBatNum = int(line[4])
            hUID = str(line[5])
            hName = str(line[6])
            hPos = str(line[7]).strip()
            if aPos == 'P':
                pbp.aPitcher = abb(aName)
            if hPos == 'P':
                pbp.hPitcher = abb(hName)
            pbp.lineup[abb(aName)] = Lineup(123, pbp.aTeam, aName, aBatNum, aPos, aUID, 'BR', con)
            pbp.lineup[abb(hName)] = Lineup(123, pbp.hTeam, hName, hBatNum, hPos, hUID, 'BR', con)
        elif len(line) == 6:
            pbp.aPitcher = abb(str(line[1]))
            pbp.hPitcher = abb(str(line[4]))
            
    #Pitch Rosters
    bp = BRPitcherParser()
    bp.feed(html)
    pitchIDLookup = {}
    for pitcher in bp.roster:
        uid = str(pitcher[0])
        name = str(pitcher[1])
        pitchIDLookup[name] = uid
        er = int(pitcher[-2])
        team = pbp.aTeam if pitcher[-1] == 'A' else pbp.hTeam
        pbp.pitchers[abb(name)] = PitchRoster(123, team, name, uid, 'BR', con)
        pbp.pitchers[abb(name)].earnedRuns = er
        pbp.pitchers[abb(name)].IP = 0

    #Hitter ID Lookup
    bb = BRBatterParser()
    bb.feed(html)


    #Plays
    b = BRPlayParser()
    b.feed(html)
    for playNum in range(1, playNum+1):
        pbp.plays[playInd] = Play()
        pbp.plays[playInd].hitterID = b.plays[playNum][7]
        pbp.plays[playInd].pitcherID = b.plays[playNum][8]

        #Inning Stuff
        innPre = 'Top' if b.plays[playNum][0][0] == 't' else 'Bot'
        prevInn = pbp.inning
        pbp.inning = innPre + str(b.plays[playNum][0][1])
        if pbp.inning != prevInn:
            pbp.outs = 0
            pbp.firstBase = None
            pbp.secondBase = None
            pbp.thirdBase = None
        pbp.plays[playInd].startSit = pbp.ReturnSit()

        #Pitches
        pitchStr = b.plays[playNum][4]
        pbp.plays[playInd].pitchSeq = pitchStr.split(') ')[1]
        pbp.plays[playInd].strikes = int(pitchStr.split('-')[1][0])
        pbp.plays[playInd].balls = int(pitchStr.split('-')[0][-1])
        pbp.ProcessBRPlay(b.plays[playNum][11], playInd)
        pbp.plays[playInd].endSit = pbp.ReturnSit()
        pbp.plays[playInd].playNum = playInd + 1

        #Subs
        if playNum in b.subs.keys():
            #Pitching Change
            if re.search('(.*) replaces (.*) pitching', b.subs[playNum]) is not None:
                newP = re.search('(.*) replaces (.*) pitching', b.subs[playNum]).group(1)
                #Find Previous Pitcher and calculate innings pitched
                p = pbp.hPitcher if pbp.inning[0] == 'B' else pbp.aPitcher
                pbp.pitchers[p].IP += int(pbp.inning.split(' ')[-1])-1
                for x in pbp.pitchers.keys():
                    if pbp.pitchers[x].team == pbp.pitchers[p].team and x != p:
                        pbp.pitchers[p].IP -= float(pbp.pitchers[x].IP)
                pbp.pitchers[p].IP += int(pbp.outs) / 3.0
                if pbp.inning[0] == 'B':
                    pbp.hPitcher = abb(newP)
                    team = pbp.hTeam
                else:
                    pbp.aPitcher = abb(newP)
                    team = pbp.aTeam
                pbp.pitchers[abb(newP)] = PitchRoster(123, team, newP, pitchIDLookup[newP], 'BR', con)
                pbp.pitchers[abb(newP)].pitcherRole = 'Reliever'
                batnum = int(re.search('batting ([0-9])', b.subs[playNum]).group(1)) \
                    if re.search('batting ([0-9])', b.subs[playNum]) is not None else 0
                pbp.lineup[abb(newP)] = Lineup(123, team, newP, batnum, 'P', pitchIDLookup[newP], 'BR', con)

            #Pinch Hitter
            elif re.search('(.*) pinch hits for (.*)', b.subs[playNum]) is not None:
                newP = re.search('(.*) pinch hits for (.*)', b.subs[playNum]).group(1)
                team = pbp.hTeam if pbp.inning[0] == 'B' else pbp.aTeam
                batnum = int(re.search('batting ([0-9])', b.subs[playNum]).group(1)) \
                    if re.search('batting ([0-9])', b.subs[playNum]) is not None else 0
                pbp.lineup[abb(newP)] = Lineup(123, team, newP, batnum, 'PH', bb.batID[newP], 'BR', con)

            #Defensive Sub
            elif re.search('(.*) replaces (.*) playing (.*) batting', b.subs[playNum]) is not None:
                newP = re.search('(.*) replaces (.*) playing (.*) batting', b.subs[playNum]).group(1)
                team = pbp.hTeam if pbp.inning[0] == 'B' else pbp.aTeam
                batnum = int(re.search('batting ([0-9])', b.subs[playNum]).group(1)) \
                    if re.search('batting ([0-9])', b.subs[playNum]) is not None else 0
                pos = re.search('(.*) replaces (.*) playing (.*) batting', b.subs[playNum]).group(3)
                pbp.lineup[abb(newP)] = Lineup(123, team, newP, batnum, pos, bb.batID[newP], 'BR', con)

            #Pinch Runner
            elif re.search('(.*) pinch runs for', b.subs[playNum]) is not None:
                newP = re.search('(.*) pinch runs for', b.subs[playNum]).group(1)
                team = pbp.hTeam if pbp.inning[0] == 'B' else pbp.aTeam
                batnum = int(re.search('batting ([0-9])', b.subs[playNum]).group(1)) \
                    if re.search('batting ([0-9])', b.subs[playNum]) is not None else 0
                pbp.lineup[abb(newP)] = Lineup(123, team, newP, batnum, 'PR', bb.batID[newP], 'BR', con)
                playInd += 1
                pbp.plays[playInd] = Play()
                pbp.plays[playInd].hitterID = abb(re.search('(.*) pinch runs for (.*) \(', b.subs[playNum]).group(1))
                pbp.plays[playInd].pitcherID = abb(pbp.aPitcher) if pbp.inning[0] == 'B' else abb(pbp.hPitcher)
                pbp.plays[playInd].inning = pbp.inning
                pbp.plays[playInd].startSit = pbp.plays[playInd].endSit = pbp.ReturnSit()
                pbp.plays[playInd].playType = 'Pinch Runner'
                replacee = re.search('(.*) pinch runs for (.*) \(', b.subs[playNum]).group(2)
                if pbp.firstBase != None and pbp.firstBase[1] == abb(replacee):
                    pbp.firstBase = [playInd, abb(newP)]
                elif pbp.secondBase != None and pbp.secondBase[1] == abb(replacee):
                    pbp.secondBase = [playInd, abb(newP)]
                elif pbp.thirdBase != None and pbp.thirdBase[1] == abb(replacee):
                    pbp.thirdBase = [playInd, abb(newP)]

        #Calculate IP for Last Pitchers
        currentGame.InsertBlankGame(con)
        currentGame.totalInnings = int(pbp.inning.split(' ')[-1])
        pbp.pitchers[pbp.hPitcher].IP += currentGame.totalInnings
        pbp.pitchers[pbp.aPitcher].IP += currentGame.totalInnings
        if pbp.inning[:3] == 'Top':
            pbp.pitchers[pbp.aPitcher].IP -= 1
        elif pbp.inning[:3] == 'Bot':
            pbp.pitchers[pbp.aPitcher].IP -= float(3 - int(pbp.outs)) / 3.0


        #Insert Game, Plays, Pitchers, and Lineups into DB
        for x in pbp.plays.values():
            if x.playType not in (
            'No Play', 'Stolen Base', 'Caught Stealing', 'Pick Off', 'Balk', 'Passed Ball', 'Wild Pitch',
            'Defensive Indifference', 'Error on Foul', 'Unknown Runner Activity'):
                x.CalcPitches()
                pbp.lineup[x.hitterID].PA += 1
                pbp.pitchers[x.pitcherID].ContactStrikes += x.contactX
                pbp.pitchers[x.pitcherID].SwingStrikes += x.swingX
                pbp.pitchers[x.pitcherID].LookStrikes += x.lookX
                pbp.pitchers[x.pitcherID].Strikes += x.lookX + x.swingX + x.contactX
                pbp.pitchers[x.pitcherID].Balls += x.balls
                pbp.pitchers[x.pitcherID].pitchCount += x.lookX + x.swingX + x.contactX + x.balls
                if x.ballType in ('Ground Ball', 'Bunt Ground Ball'):
                    pbp.pitchers[x.pitcherID].GB += 1
                elif x.ballType in ('Line Drive', 'Bunt Line Drive'):
                    pbp.pitchers[x.pitcherID].LD += 1
                elif x.ballType in ('Fly Ball', 'Pop Up', 'Bunt Pop'):
                    pbp.pitchers[x.pitcherID].FB += 1
                if x.playType in (
                'Strikeout', 'Out', 'Double Play', 'Triple Play', "Fielders Choice", 'Reach On Error', 'Single',
                'Double', 'Ground Rule Double', 'Triple', 'Home Run'):
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
                    currentGame.awayHits += 1
                currentGame.awayRuns += x.runsScored
            else:
                if x.hit:
                    currentGame.homeHits += 1
                currentGame.homeRuns += x.runsScored
            x.gameKey = currentGame.gameKey
            x.InsertPlay('BR', con)
        if currentGame.homeRuns > currentGame.awayRuns:
            currentGame.homeTeamWin = True
        elif currentGame.homeRuns == currentGame.awayRuns:
            currentGame.tie = True
        currentGame.UpdateStats(con)

        # Go Through Pitchers
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

        # Go Through Hitters
        for x in pbp.lineup.keys():
            pbp.lineup[x].game = currentGame.gameKey
            pbp.lineup[x].InsertLineupRow(con)

        playInd += 1
    return currentGame, pbp