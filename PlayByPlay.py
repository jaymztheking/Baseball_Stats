class Play:
    pitchSeq = ''
    batEvent = ''
    runEvent = ''
    runsScored = 0
    runScored = False
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
    
    def AddPlay(self, userid, PA, pitchSeq, playStr):
        self.lineup[userid].PA += 1
        playInd = userid + str(self.lineup[userid].PA)
        
        