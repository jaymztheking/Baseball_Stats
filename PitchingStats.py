from bbUtils import GetPitcherKey, GetCrossSiteUserID
from PlayerStats import Pitcher


class PitchRoster:
    gameKey = 0 
    team = 0 
    pitcherKey = 0 
    pitcherRole = '' 
    pitchCount = 0 
    K = 0 
    BB = 0 
    HBP = 0 
    Runs = 0 
    Hits = 0 
    earnedRuns = 0 
    IP = 0 
    CG = False
    SO = False
    NH = False
    Win = False
    Loss = False
    Save = False
    Strikes = 0 
    Balls = 0 
    ContactStrikes = 0 
    SwingStrikes = 0 
    LookStrikes = 0 
    LD = 0 
    GB = 0 
    FB = 0     
    
    def __init__(self, game, team, playerName, ID, src, con):
        self.gameKey = game
        self.team = team
        playerKey = GetPitcherKey(src, ID, con)
        if playerKey == None:
            newID = GetCrossSiteUserID(src, 'RS', ID, con)
            playerKey = GetPitcherKey('RS', newID, con)
            if playerKey == None:
                newPlayer = Pitcher(src, ID, playerName)
                newPlayer.InsertPlayerRow(con)
                playerKey = newPlayer.GetPitcherKey(con)
                self.pitcherKey = playerKey
            else:
                self.pitcherKey = playerKey
        else:
            self.pitcherKey = playerKey
    
    def InsertRosterRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "PITCH_ROSTER" VALUES (%s, %s, \'%s\', %s, %s, ' \
                    '%s, %s, %s, %s, %s, ' \
                    '%s, %s, %s, %s, %s, ' \
                    '%s, %s, %s, %s, %s, ' \
                    '%s, %s, %s, %s, %s)' % \
        (self.gameKey, self.pitcherKey, self.pitcherRole, self.pitchCount, self.K,
         self.BB, self.HBP, self.earnedRuns, self.IP, self.Strikes,
         self.Balls, self.ContactStrikes, self.CG, self.SO, self.team,
         self.NH, self.Win, self.Loss, self.Save, self.SwingStrikes,
         self.LookStrikes, self.FB, self.GB, self.LD, self.Hits)
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