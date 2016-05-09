from datetime import date
from bbUtils import GetTeamfromAbb, ConvertTeamAbb
from BRParser import GameTeamsParser, GameTimeParser, GameWeatherParser, GameUmpParser, GameWinLossSaveParser, \
    BRLineupParser, BRPitcherParser,  BRPlayParser
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
    
    #Plays
    b = BRPlayParser()
    b.feed(html)
    for playNum in range(1, playNum+1):
        pbp.plays[playNum] = Play()
        pbp.plays[playNum].hitterID = b.plays[playNum][7]
        pbp.plays[playNum].pitcherID = b.plays[playNum][8]

        #Inning Stuff
        innPre = 'Top' if b.plays[playNum][0][0] == 't' else 'Bot'
        prevInn = pbp.inning
        pbp.inning = innPre + str(b.plays[playNum][0][1])
        if pbp.inning != prevInn:
            pbp.outs = 0
            pbp.firstBase = None
            pbp.secondBase = None
            pbp.thirdBase = None
        pbp.plays[playNum].startSit = pbp.ReturnSit()

        #Pitches
        pitchStr = b.plays[playNum][4]
        pbp.plays[playNum].pitchSeq = pitchStr.split(') ')[1]
        pbp.plays[playNum].strikes = int(pitchStr.split('-')[1][0])
        pbp.plays[playNum].balls = int(pitchStr.split('-')[0][-1])
        pbp.ProcessBRPlay(b.plays[playNum][11])
        pbp.plays[playNum].endSit = pbp.ReturnSit()
        pbp.plays[playNum].playNum = playNum

        #Subs
        if playNum in b.subs.keys():
            #Pitching Change
            if re.search('(.*) replaces (.*) pitching', b.subs[playNum]) is not None:
                newP = re.search('(.*) replaces (.*) pitching', b.subs[playNum]).group(1)
                #Find Previous Pitcher and calculate innings pitched
                p = pbp.hPitcher if pbp.innning[0] == 'B' else pbp.aPitcher
                pbp.pitchers[p].IP += int(pbp.inning.split(' ')[-1])-1
                for x in pbp.pitchers.keys():
                    if pbp.pitchers[x].team == pbp.pitchers[p].team and x != p:
                        pbp.pitchers[p].IP -= float(pbp.pitchers[x].IP)
                pbp.pitchers[p].IP += int(pbp.outs) / 3.0
                if pbp.innning[0] == 'B':
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
                team = pbp.hTeam if pbp.innning[0] == 'B' else pbp.aTeam
                #pbp.lineup[abb(newP)] = Lineup(123, team, newP, 0, 'PH', abb(newP), 'BR', con)


            #Defensive Sub

            #Pinch Runner

            #other

    return currentGame, pbp