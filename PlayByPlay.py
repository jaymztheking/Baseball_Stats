import re

class Play:
    gameKey = 0
    hitterID = ''
    hitterPA = 0
    pitcherID = ''
    inning = ''
    pitchSeq = ''
    runScored = False
    RBIs = 0
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
    
    def init(self):
        pass
    
    def CalcPitches(self):
        for pitch in self.pitchSeq:
            if pitch in ('F','X','L','O','R','T','Y'):
                self.contactX +=1
            elif pitch == 'C':
                self.lookX +=1
            elif pitch in ('S','M','Q'):
                self.swingX += 1
                           

class PlayByPlay:
    sorter = {'3':1,'2':2,'1':3,'B':4}
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
    innning = ''
    
    def init(self):
        pass
        
    def ReturnSit(self):
        output = self.outs * 10
        if self.firstBase != None:
            output += 1
        if self.secondBase != None:
            output += 2
        if self.thirdBase != None:
            output += 4
        return output
      
    def ProcessRSPlay(self, playStr, playInd):
        hitterID = self.plays[playInd].hitterID
        pitcherID = self.plays[playInd].pitcherID
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
        
        #Stolen Base
        if re.search('SB[23H]', batParts[0]) != None:
            self.plays[playInd].playType = 'Stolen Base'
            if 'SB2' in batParts[0]:
                self.lineup[self.firstBase].SB += 1
                if '1-' not in runEvent:
                    runEvent += ';1-2'
            elif 'SB3' in batParts[0]:
                self.lineup[self.secondBase].SB += 1
                if '2-' not in runEvent:
                    runEvent += ';2-3'
            elif 'SBH' in batParts[0]:
                self.lineup[self.thirdBase].SB += 1
                if '3-' not in runEvent:
                    runEvent += ';3-H'
                    
        #Caught Stealing
        if re.search('CS[23H]', batParts[0]) != None:
            self.plays[playInd].playType = 'Caught Stealing'
            if 'CS2' in batParts[0]:
                self.lineup[self.firstBase].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';1X2'
                elif '1-' not in runEvent:
                    runEvent += ';1-2'
            if 'CS3' in batParts[0]:
                self.lineup[self.secondBase].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';2X3'
                elif '2-' not in runEvent:
                    runEvent += ';2-3'
            if 'CSH' in batParts[0]:
                self.lineup[self.thirdBase].CS += 1
                if 'E' not in batParts[0]:
                    runEvent += ';3XH'
                elif '3-' not in runEvent:
                    runEvent += ';3-H'
                    
        #Balk
        if re.search('BK', batParts[0]) != None:
            self.plays[playInd].playType = 'Balk'
            
        #Passed Ball
        if re.search('PB', batParts[0]) != None:
            self.plays[playInd].playType = 'Passed Ball'
        
        #Wild Pitch
        if re.search('WP', batParts[0]) != None:
            self.plays[playInd].playType = 'Wild Pitch'
            
        #Defensive Indifference
        if re.search('DI', batParts[0]) != None:
            self.plays[playInd].playType = 'Defensive Indifference'
            
        #Error on Foul
        if re.search('FLE', batParts[0]) != None:
            self.plays[playInd].playType = 'Error on Foul'

###############################################################################
#  Plate Appearance, No At-Bat                                                #
###############################################################################
            
        #Interference
        if re.search('C$', batParts[0]) != None:
            self.plays[playInd].playType = 'Interference'
            if 'B-' not in runEvent:
                runEvent += ';B-1'
                
        #Walk and Intentional Walks
        if re.search('W', batParts[0]) != None:
            self.plays[playInd].playType = 'Intentional Walk' if 'IW' in batParts[0] else 'Walk'
            self.lineup[hitterID].BB += 1
            self.pitchers[pitcherID].BB += 1
            if 'B-' not in runEvent:
                runEvent += ';B-1'
        
        #Hit By Pitch
        if re.search('HP', batParts[0]) != None:
            self.plays[playInd].playType = 'Hit By Pitch'
            self.lineup[hitterID].HBP += 1
            self.pitchers[pitcherID].HBP += 1
            if 'B-' not in runEvent:
                runEvent += ';B-1'
            
        #Sacrifice Fly
        if 'SF' in playStr:
            self.plays[playInd].playType = 'Sacrifice Fly'
            
        #Sacrific Hit
        if 'SH' in playStr:
            self.plays[playInd].playType = 'Sacrifice Hit'
            
###############################################################################
#  Plate Appearance, No At-Bat                                                #
###############################################################################        
          
        #Strike Out
        if re.search('(^|[^B])K', batParts[0]) != None:
            self.plays[playInd].playType = 'Strikeout'
            self.pitchers[pitcherID].K += 1
            self.plays[playInd].resultOuts = 1
            self.outs +=1
            
            
        #One Fielding Out
        if re.search('^[0-9]+$', batParts[0]) != None:
            if self.plays[playInd].playType[:9] != 'Sacrifice':            
                self.plays[playInd].playType = 'Out'
            self.plays[playInd].ballLoc = batParts[0][0]
            self.plays[playInd].resultOuts = 1
            self.outs += 1

        #Field Outs/Double Play/Triple Play
        if re.search('^[0-9]{1,2}\([B123]\)', batParts[0]) != None:
                        
            
        #Fielder's Choice
        
        #Single
         
        #Double and Groud Rule
         
        #Triple
         
        #Home Run
        