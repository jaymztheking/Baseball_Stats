from BRParser import PitchRosterParser

def GetPitchRoster(gameKey, url, con):
    b = PitchRosterParser()

class PitchRoster:
    gameKey = 0
    teamKey = 0
    pitcherKey = 0
    pitcherRole = ''
    pitchCount = 0
    K = 0
    BB = 0
    HBP = 0
    earnedRuns = 0
    IP = 0
    CG = False
    SO = False
    NH = False
    Win = False
    Loss = False
    Save = False
    Hold = False
    
    def __init__(self, game, team, player):
        self.gameKey = game
        self.teamKey = team
        self.pitcherKey = player