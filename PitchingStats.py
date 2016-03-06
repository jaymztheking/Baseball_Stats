from BRParser import PitchRosterParser
from bbUtils import GetPitcherKey, GetTeam
from PlayerStats import Pitcher
import urllib2

def GetPitchRoster(gameKey, url, con):
    b = PitchRosterParser()
    b.allRows = []
    pitchers = {}
    userid = ''
    name = ''
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    team = 'A'
    tm = GetTeam(gameKey, team, con)
    for p in b.allRows:
        if len(p)>5 and p[1] != 'Team Totals' and p[2].isnumeric():
            userid = p[0]
            name = p[1].split(',')[0]
            pitchers[userid] = PitchRoster(gameKey, tm, name, userid, con)
            pitchers[userid].IP = float(p[2]) 
            pitchers[userid].Hits = int(p[3]) if p[3].isnumeric() else 0
            pitchers[userid].Runs = int(p[4]) if p[4].isnumeric() else 0
            pitchers[userid].earnedRuns = int(p[5]) if p[5].isnumeric() else 0
            pitchers[userid].BB = int(p[6]) if p[6].isnumeric() else 0
            pitchers[userid].K = int(p[7]) if p[7].isnumeric() else 0
            pitchers[userid].pitchCount = int(p[11]) if p[11].isnumeric() else 0
            pitchers[userid].Strikes = int(p[12]) if p[12].isnumeric() else 0
            pitchers[userid].Balls = pitchers[userid].pitchCount - pitchers[userid].Strikes
            pitchers[userid].ContactStrikes = int(p[13]) if p[13].isnumeric() else 0
            pitchers[userid].SwingStrikes = int(p[14]) if p[14].isnumeric() else 0
            pitchers[userid].LookStrikes = int(p[15]) if p[15].isnumeric() else 0
            pitchers[userid].LD = int(p[18]) if p[18].isnumeric() else 0
            pitchers[userid].FB = int(p[17]) if p[17].isnumeric() else 0
            pitchers[userid].GB = int(p[16]) if p[16].isnumeric() else 0
            
            if pitchers[userid].IP == 9.0:
                pitchers[userid].CG = True
                if pitchers[userid].Runs == 0:
                    pitchers[userid].SO = True
                    if pitchers[userid].Hits == 0:
                        pitchers[userid].NH = True
                        
            if len(p[1].split(',')) > 1:
                x = p[1].split(',')[1]
                if ' L ' in x:
                    pitchers[userid].Loss = True
                elif ' W ' in x:
                    pitchers[userid].Win = True
                elif ' S ' in x:
                    pitchers[userid].Save = True
            pitchers[userid].InsertRosterRow(con)
        elif team == 'A' and len(p)>1 and p[1] == 'Team Totals':
            team = 'H'
            tm = GetTeam(gameKey, team, con)
    
    return pitchers

class PitchRoster:
    gameKey = 0 #init
    teamKey = 0 #init
    pitcherKey = 0 #init
    pitcherRole = '' #dunno yet
    pitchCount = 0 #p11
    K = 0 #p7
    BB = 0 #p6
    HBP = 0 #dunno yet
    Runs = 0 #p4
    Hits = 0 #p3
    earnedRuns = 0 #p5
    IP = 0 #p2
    CG = False
    SO = False
    NH = False
    Win = False
    Loss = False
    Save = False
    Strikes = 0 #p12
    Balls = 0 #calc
    ContactStrikes = 0 #p13
    SwingStrikes = 0 #p14
    LookStrikes = 0 #p15
    LD = 0 #p18
    GB = 0 #p17
    FB = 0 #p16    
    
    def __init__(self, game, team, playerName, ID, con):
        self.gameKey = game
        self.teamKey = team
        
        playerKey = GetPitcherKey(ID, con)
        if playerKey == None:
            newPlayer = Pitcher(ID, playerName)
            newPlayer.InsertPlayerRow(con)
            playerKey = GetPitcherKey(ID, con)
            self.pitcherKey = playerKey
        else:
            self.pitcherKey = playerKey
    
    def InsertRosterRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "PITCH_ROSTER" VALUES (%s, %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % \
        (self.gameKey, self.pitcherKey, self.pitcherRole, self.pitchCount, self.K, self.BB, self.HBP, self.earnedRuns, self.IP, self.Strikes, self.Balls, self.ContactStrikes, self.CG, self.SO, self.teamKey, self.NH, self.Win, self.Loss, self.Save, self.SwingStrikes, self.LookStrikes, self.FB, self.GB, self.LD)        
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            return True
        return False
    
    def CheckForRow(self, con):
        cur = con.cursor()
        checkSQL = 'select 1 from "PITCH_ROSTER" where "GAME_KEY" = %s and "PITCHER_KEY" = %s' % (self.gameKey, self.pitcherKey)
        cur.execute(checkSQL)
        results = cur.fetchall()
        if len(results) == 0:
            return False
        else:
            return True