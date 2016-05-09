import re
from bbUtils import GetHitterKey, GetPitcherKey

class Play:
    playNum = 0
    gameKey = 0
    hitterID = ''
    pitcherID = ''
    inning = ''
    pitchSeq = ''
    runScored = False
    runsScored = 0
    playType = ''
    ballType =''
    ballLoc = ''
    hit = False
    resultOuts = 0
    strikes = 0
    balls = 0
    contactX = 0
    lookX = 0
    swingX = 0
    startSit = 0
    endSit = 0

    def InsertPlay(self, src, con):
        hk = GetHitterKey(src, self.hitterID, con)
        pk = GetPitcherKey(src, self.pitcherID, con)
        cur = con.cursor()
        sql = 'INSERT INTO "PITCH_RESULT" VALUES(%s, %s, %s, %s, \'%s\', %s, %s, \'%s\', %s, %s, %s, \'%s\', \'%s\', %s, \'%s\', \'%s\', %s, \'%s\', %s, %s)' % \
        (self.gameKey, hk, pk, self.startSit, self.inning, self.strikes, self.balls, self.pitchSeq, self.contactX, self.swingX, self.lookX, self.playType, self.hit, self.resultOuts, self.ballLoc, self.ballType, self.endSit, self.runScored, self.runsScored, self.playNum)
        cur.execute(sql)
        cur.execute('COMMIT;')
    
    def CalcPitches(self):
        for pitch in self.pitchSeq:
            if pitch in ('F','X','L','O','R','T','Y'):
                self.contactX +=1
            elif pitch == 'C':
                self.lookX +=1
            elif pitch in ('S','M','Q'):
                self.swingX += 1
                           

class PlayByPlay:
    aTeam = 0
    hTeam = 0
    aAbb = ''
    hAbb = ''
    plays = {}
    lineup = {}
    pitchers = {}
    firstBase = None
    secondBase = None
    thirdBase = None
    outs = 0
    aPitcher = ''
    hPitcher = ''
    inning = ''
    
    def init(self):
        pass
        
    def ReturnSit(self):
        output = self.outs * 10
        if output >= 30:
            return 30
        else:
            if self.firstBase != None:
                output += 1
            if self.secondBase != None:
                output += 2
            if self.thirdBase != None:
                output += 4
            return output
        
    def GetRSBallType(self, batMods, playInd):
        for x in batMods:
            if re.search('^[0-9]{1,2}$', x) != None:
                self.plays[playInd].ballLoc = x
            if re.search('^B?[LFGP][0-9]', x) != None:
                self.plays[playInd].ballLoc = re.search('^B?[LFGP]([0-9])', x).group(1)
            if re.search('L', x) != None:
                self.plays[playInd].ballType = 'Line Drive'
            if re.search('F', x) != None:
                self.plays[playInd].ballType = 'Fly Ball'
            if re.search('G', x) != None:
                self.plays[playInd].ballType = 'Ground Ball'
            if re.search('P', x) != None and re.search('DP', x) == None:
                self.plays[playInd].ballType = 'Pop Up'
            if re.search('BP', x) != None:
                self.plays[playInd].ballType = 'Bunt Pop'
            if re.search('BL', x) != None:
                self.plays[playInd].ballType = 'Bunt Line Drive'
            if re.search('BG', x) != None:
                self.plays[playInd].ballType = 'Bunt Ground Ball'
        
    def CalcRSRunners(self, runEvent, playInd, rbiEligible):
        sorter = {'3':1,'2':2,'1':3,'B':4}
        hitterID = self.plays[playInd].hitterID
        pitcherID = self.plays[playInd].pitcherID
        if runEvent != '':
            runners = filter(None, runEvent.split(';'))
            runners = sorted(runners, key=lambda base: sorter[base[0]])
            if '2-1' in runners[0]:
                runners.insert(len(runners), runners.pop(0))
            for run in runners:
                if run[:3] == '1-2':
                    self.secondBase = self.firstBase
                    self.firstBase = None
                elif run[:3] == '1-3':
                    self.thirdBase = self.firstBase
                    self.firstBase = None
                elif run[:3] == '1-H':
                    ind = self.firstBase[0]
                    self.plays[ind].runScored = True
                    self.lineup[self.firstBase[1]].Runs += 1
                    self.pitchers[pitcherID].Runs += 1
                    if rbiEligible and ('NR' not in run and 'E' not in run):
                        self.lineup[hitterID].RBI += 1
                    self.plays[playInd].runsScored += 1
                    self.firstBase = None
                elif run[:3] == '2-3':
                    self.thirdBase = self.secondBase
                    self.secondBase = None
                elif run[:3] == '2-H':
                    ind = self.secondBase[0]
                    self.plays[ind].runScored = True
                    self.lineup[self.secondBase[1]].Runs += 1
                    self.pitchers[pitcherID].Runs += 1
                    if rbiEligible  and ('NR' not in run and 'E' not in run):
                        self.lineup[hitterID].RBI += 1
                    self.plays[playInd].runsScored += 1
                    self.secondBase = None
                elif run[:3] == '3-H':
                    ind = self.thirdBase[0]
                    self.lineup[self.thirdBase[1]].Runs += 1
                    self.plays[ind].runScored = True
                    self.pitchers[pitcherID].Runs += 1
                    if rbiEligible  and ('NR' not in run and 'E' not in run):
                        self.lineup[hitterID].RBI += 1
                    self.plays[playInd].runsScored += 1
                    self.thirdBase = None
                elif run[:3] == 'B-1':
                    self.firstBase = [playInd, self.plays[playInd].hitterID]
                elif run[:3] == 'B-2':
                    self.secondBase = [playInd, self.plays[playInd].hitterID]
                elif run[:3] == 'B-3':
                    self.thirdBase = [playInd, self.plays[playInd].hitterID]
                elif run[:3] == 'B-H':
                    self.plays[playInd].runScored = True
                    self.lineup[self.plays[playInd].hitterID].Runs += 1
                    self.pitchers[pitcherID].Runs += 1
                    if rbiEligible and ('NR' not in run and 'E' not in run):
                        self.lineup[hitterID].RBI += 1
                    self.plays[playInd].runsScored += 1
                elif run[:2] == '1X':
                    if 'E' not in run:
                        self.outs +=1
                        self.plays[playInd].resultOuts += 1
                        self.firstBase = None
                    else:
                        run = run[:3].replace('X','-')
                        self.CalcRSRunners(run, playInd, False)
                elif run[:2] == '2X':
                    if 'E' not in run:
                        self.outs +=1
                        self.plays[playInd].resultOuts += 1
                        self.secondBase = None
                    else:
                        run = run[:3].replace('X','-')
                        self.CalcRSRunners(run, playInd, False)
                elif run[:2] == '3X':
                    if 'E' not in run:
                        self.outs +=1
                        self.plays[playInd].resultOuts += 1
                        self.thirdBase = None
                    else:
                        run = run[:3].replace('X','-')
                        self.CalcRSRunners(run, playInd, False)
                elif run[:2] == 'BX':
                    if 'E' not in run:
                        self.outs +=1
                        self.plays[playInd].resultOuts += 1
                    else:
                        run = run[:3].replace('X','-')
                        self.CalcRSRunners(run, playInd, False)
                #Jean Segura Memorial Code Block - backward running
                elif run[:3] == '2-1':
                    self.firstBase = self.secondBase
                    self.secondBase = None
                
    def ProcessRSPlay(self, playStr, playInd):
        play = playStr.split('.')
        batEvent = play[0]
        runEvent = play[1] if len(play) == 2 else ''
        batParts = batEvent.split('/')

###############################################################################
#  No Plate Appearance, No At-Bat                                             #
###############################################################################        
        #Non-Plays
        if batParts[0].strip() == 'NP':
            self.plays[playInd].playType = 'No Play'
            rbiEligible = False
        
        #Stolen Base
        if re.search('SB[23H]', batParts[0]) != None:
            self.plays[playInd].playType = 'Stolen Base'
            rbiEligible = False
            if 'SB2' in batParts[0]:
                self.lineup[self.firstBase[1]].SB += 1
                if '1-' not in runEvent:
                    runEvent += ';1-2'
            if 'SB3' in batParts[0]:
                self.lineup[self.secondBase[1]].SB += 1
                if '2-' not in runEvent:
                    runEvent += ';2-3'
            if 'SBH' in batParts[0]:
                self.lineup[self.thirdBase[1]].SB += 1
                if '3-' not in runEvent:
                    runEvent += ';3-H'
                    
        #Caught Stealing
        if re.search('CS[23H]', batParts[0]) != None:
            self.plays[playInd].playType = 'Caught Stealing'
            rbiEligible = False
            if 'CS2' in batParts[0]:
                self.lineup[self.firstBase[1]].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';1X2'
                elif '1-' not in runEvent:
                    runEvent += ';1-2'
            if 'CS3' in batParts[0]:
                self.lineup[self.secondBase[1]].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';2X3'
                elif '2-' not in runEvent:
                    runEvent += ';2-3'
            if 'CSH' in batParts[0]:
                self.lineup[self.thirdBase[1]].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';3XH'
                elif '3-' not in runEvent:
                    runEvent += ';3-H'
         
         #Pick Off
        if re.search('PO[^C]', batParts[0]) != None:
            self.plays[playInd].playType = 'Pick Off'
            rbiEligible = False
            if 'E' not in batParts[0]:
                self.outs += 1
                self.plays[playInd].resultOuts = 1
                if 'PO1' in batParts[0]:
                    self.firstBase = None
                elif 'PO2' in batParts[0]:
                    self.secondBase = None
                elif 'PO3' in batParts[0]:
                    self.thirdBase = None
         
        #Balk
        if re.search('BK', batParts[0]) != None:
            self.plays[playInd].playType = 'Balk'
            rbiEligible = False
            
        #Passed Ball
        if re.search('PB', batParts[0]) != None:
            self.plays[playInd].playType = 'Passed Ball'
            rbiEligible = False
        
        #Wild Pitch
        if re.search('WP', batParts[0]) != None:
            self.plays[playInd].playType = 'Wild Pitch'
            rbiEligible = False
            
        #Defensive Indifference
        if re.search('DI', batParts[0]) != None:
            self.plays[playInd].playType = 'Defensive Indifference'
            rbiEligible = False
            
        #Error on Foul
        if re.search('FLE', batParts[0]) != None:
            self.plays[playInd].playType = 'Error on Foul'
            rbiEligible = False
            
        #Misc. Advance
        if re.search('OA', batParts[0]) != None:
            self.plays[playInd].playType = 'Unknown Runner Activity'
            rbiEligible = False

###############################################################################
#  Plate Appearance, No At-Bat                                                #
###############################################################################
            
        #Interference
        if re.search('C$', batParts[0]) != None:
            self.plays[playInd].playType = 'Interference'
            rbiEligible = True
            if 'B-' not in runEvent:
                runEvent += ';B-1'
                
        #Walk and Intentional Walks
        if re.search('W(\+|$)', batParts[0]) != None:
            self.plays[playInd].playType = 'Intentional Walk' if 'IW' in batParts[0] else 'Walk'
            rbiEligible = True
            if 'B-' not in runEvent:
                runEvent += ';B-1'
        
        #Hit By Pitch
        if re.search('HP', batParts[0]) != None:
            self.plays[playInd].playType = 'Hit By Pitch'
            rbiEligible = True
            if 'B-' not in runEvent:
                runEvent += ';B-1'
            
        #Sacrifice Fly
        if 'SF' in playStr:
            self.plays[playInd].playType = 'Sacrifice Fly'
            rbiEligible = True
            
        #Sacrific Hit
        if 'SH' in playStr:
            self.plays[playInd].playType = 'Sacrifice Hit'
            rbiEligible = True
            
###############################################################################
#  Plate Appearance, At-Bat                                                   #
###############################################################################        
          
        #Strike Out
        if re.search('(^|[^B])K', batParts[0]) != None:
            self.plays[playInd].playType = 'Strikeout'
            rbiEligible = False
            if 'B-' not in runEvent:
                self.plays[playInd].resultOuts = 1
                self.outs +=1
            
            
        #One Fielding Out
        if re.search('^[0-9]+$', batParts[0]) != None:
            if self.plays[playInd].playType[:9] != 'Sacrifice':            
                self.plays[playInd].playType = 'Out'
                rbiEligible = True
            self.plays[playInd].ballLoc = batParts[0][0]
            self.plays[playInd].resultOuts = 1
            self.outs += 1

        #Force and Tag Outs/Double Play/Triple Play
        if re.search('^[0-9]{1,4}\([B123]\)', batParts[0]) != None:
            outStr = re.findall('\([B123]\)', batParts[0])
            self.plays[playInd].ballLoc = batParts[0][0]
            for a in batParts:
                if 'DP' in a and 'NDP' not in a:
                    self.outs += len(outStr)
                    self.plays[playInd].resultOuts = len(outStr)
                    self.plays[playInd].playType = 'Double Play'
                    rbiEligible = False
                    if (runEvent.count('X') + len(outStr)) == 2 and '(B)' not in outStr:
                        runEvent += ';B-1'
                if 'TP' in a:
                    self.outs +=3
                    self.plays[playInd].resultOuts = 3
                    self.plays[playInd].playType = 'Triple Play'
                    rbiEligible = False
            if self.plays[playInd].playType not in('Triple Play', 'Double Play'):
                self.plays[playInd].playType = 'Out'
                rbiEligible = True
                self.outs += 1
                self.plays[playInd].resultOuts = 1
                if 'B' not in runEvent and '(B)' not in outStr:
                    runEvent += ';B-1'
            for o in outStr:
                if o == '(1)':
                    self.firstBase = None
                elif o == '(2)':
                    self.secondBase = None
                elif o == '(3)':
                    self.thirdBase = None
                    
        #Fielder's Choice
        if re.search('FC[0-9]', batParts[0]) != None:
            self.plays[playInd].playType = "Fielders Choice"
            rbiEligible = True
            self.plays[playInd].ballLoc = re.search('FC([0-9])', batParts[0]).group(1)
            if 'B' not in runEvent:
                runEvent += ';B-1'
            
        #Reach on Error
        if re.search('(^|[^\(])E[0-9]', batParts[0]) != None and re.search('FLE', batParts[0]) == None:
            if self.plays[playInd].playType[:9] != 'Sacrifice':            
                self.plays[playInd].playType = 'Reach On Error'
                if self.outs < 2:
                    rbiEligible = True
                else:
                    rbiEligible = False
            if 'B-' not in runEvent or 'BX' not in runEvent:
                runEvent += ';B-1'
            
        #Single
        if re.search('^S[0-9]?', batParts[0]) != None and re.search('SB[23H]', batParts[0]) == None:
            self.plays[playInd].hit = True
            self.plays[playInd].playType = 'Single'
            rbiEligible = True
            if re.search('^S[0-9]', batParts[0]) != None:
                self.plays[playInd].ballLoc = re.search('S([0-9])', batParts[0]).group(1)
            if 'B' not in runEvent:
                runEvent += ';B-1'
         
        #Double
        if re.search('^D[0-9]?', batParts[0]) != None and re.search('DI', batParts[0]) == None:
            self.plays[playInd].hit = True
            self.plays[playInd].playType = 'Double'
            rbiEligible = True
            if re.search('^D[0-9]', batParts[0]) != None:
                self.plays[playInd].ballLoc = re.search('D([0-9])', batParts[0]).group(1)
            if 'B' not in runEvent:
                runEvent += ';B-2'
         
        #Groud Rule Double
        if re.search('DGR', batParts[0]) != None:
            self.plays[playInd].hit = True
            self.plays[playInd].playType = 'Ground Rule Double'
            rbiEligible = True
            if 'B' not in runEvent:
                runEvent += ';B-2'
         
        #Triple
        if re.search('^T[0-9]?', batParts[0]) != None:
            self.plays[playInd].hit = True
            self.plays[playInd].playType = 'Triple'
            rbiEligible = True
            if re.search('^T[0-9]', batParts[0]) != None:
                self.plays[playInd].ballLoc = re.search('T([0-9])', batParts[0]).group(1)
            if 'B' not in runEvent:
                runEvent += ';B-3'
         
        #Home Run
        if re.search('HR', batParts[0]) != None:
            self.plays[playInd].hit = True
            self.plays[playInd].playType = 'Home Run'
            rbiEligible = True
            if 'B' not in runEvent:
                runEvent += ';B-H'
                
        self.GetRSBallType(batParts[1:], playInd)
        self.CalcRSRunners(runEvent.strip(), playInd, rbiEligible)

    def ProcessBRPlay(self, playStr, playInd):
        pass