from bbUtils import GetHitterKey, GetTeam
from PlayerStats import Hitter

class Lineup:
    #Lineup    
    game = 0
    team = 0
    player = 0
    player_bat_num = 0
    player_pos = ''
    userID = ''
    
    #Batting Data
    PA = 0
    AB = 0 
    Hits = 0 
    BB = 0 
    HBP = 0 
    Runs = 0 
    RBI = 0 
    Single = 0 
    Double = 0 
    Triple = 0 
    HR = 0 
    SB = 0 
    CS = 0 
    
    def __init__(self, game, team, playerName, batnum, pos, ID, con):
        self.game = game
        self.team = team
        self.player_bat_num = batnum
        self.player_pos = pos
        self.userID = ID
        
        playerKey = GetHitterKey(ID, con)
        if playerKey == None:
            newPlayer = Hitter(ID, playerName)
            newPlayer.InsertPlayerRow(con)
            playerKey = GetHitterKey(ID, con)
            self.player = playerKey
        else:
            self.player = playerKey
    
    def InsertLineupRow(self, con):
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
    


            
        

    