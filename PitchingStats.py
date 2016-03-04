from BRParser import PitchRosterParser
import urllib2

def GetPitchRoster(gameKey, url, con):
    b = PitchRosterParser()
    pitchers = {}
    userid = ''
    name = ''
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    team = 'A'
    
    
    return pitchers

class PitchRoster:
    gameKey = 0
    teamKey = 0
    pitcherKey = 0
    pitcherRole = ''
    pitchCount = 0
    K = 0
    BB = 0
    HBP = 0
    Runs = 0
    earnedRuns = 0
    IP = 0
    CG = False
    SO = False
    NH = False
    Win = False
    Loss = False
    Save = False
    Hold = False
    Strikes = 0
    Balls = 0
    ContactStrikes = 0
    SwingStrikes = 0
    LookStrikes = 0
    LD = 0
    GB = 0
    FB = 0    
    
    def __init__(self, game, team, player):
        self.gameKey = game
        self.teamKey = team
        self.pitcherKey = player