from bbUtils import GetHitterKey, GetTeam, GetLineupPlayers
from PlayerStats import Hitter
import urllib2
from BRParser import LineupParser, BattingDataParser

def GetLineups(gameKey, url, con):
    positions = ['C','1B','2B','SS','3B','LF','CF','RF','DH','PH','P']          
    lineupRows = {}
    batnum = 0
    userid = ''
    pos = ''
    name = ''
    b = LineupParser()
    b.allRows = []
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    team = 'A'
    atm = GetTeam(gameKey, team, con)
    htm = GetTeam(gameKey, 'H', con)

    for row in b.allRows:
        if len(row)>1 and row[1].isdigit():
            userid = row[0]
            batnum = int(row[1])
            name = row[2]
            pos = row[3]
            if team == 'A':
                tm = atm
                team = 'H'
            else:
                tm = htm
                team = 'A'
            lineupRows[name] = Lineup(gameKey, tm, name, batnum, pos, userid, con)
    
    c = BattingDataParser()
    c.allRows = []
    team = 'A'
    html = urllib2.urlopen(url).read().decode('utf-8')
    c.feed(html)
    lastBatNum = 1
    for i in range(1, len(c.allRows)):
        if len(c.allRows[i]) >1 and c.allRows[i][1] in lineupRows.keys():
            lastBatNum = lineupRows[c.allRows[i][1]].player_bat_num
        elif len(c.allRows[i]) >1 and c.allRows[i][1] == 'Batting':
            team = 'H'
            lastBatNum = 1
            continue
        elif len(c.allRows[i])>3 and c.allRows[i][2] != 'P' and c.allRows[i][1] != 'Team Totals' and c.allRows[i][3].isnumeric() and int(c.allRows[i][3])>0:
            print(c.allRows[i][1])            
            lineupRows[c.allRows[i][1]] = Lineup(gameKey, GetTeam(gameKey, team, con), c.allRows[i][1], lastBatNum, 'PH', c.allRows[i][0] , con)
        else: 
            continue
        
        lineupRows[c.allRows[i][1]].AB = int(c.allRows[i][3]) if c.allRows[i][3].isnumeric() else 0
        lineupRows[c.allRows[i][1]].Hits = int(c.allRows[i][5]) if c.allRows[i][5].isnumeric() else 0
        lineupRows[c.allRows[i][1]].BB = int(c.allRows[i][7]) if c.allRows[i][7].isnumeric() else 0
        lineupRows[c.allRows[i][1]].Runs = int(c.allRows[i][4]) if c.allRows[i][4].isnumeric() else 0
        lineupRows[c.allRows[i][1]].RBI = int(c.allRows[i][6]) if c.allRows[i][6].isnumeric() else 0
        
        text = c.allRows[i][-1].split(',')
        for t in text:
            if 'HBP' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].HBP = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].HBP = 1
            elif '2B' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].Double = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].Double = 1
            elif '3B' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].Triple = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].Triple = 1
            elif 'HR' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].HR = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].HR = 1
            elif 'SB' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].SB = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].SB = 1
            elif 'CS' in t:
                if '*' in t:
                    lineupRows[c.allRows[i][1]].CS = int(t[:t.find('*')]) if t[:t.find('*')].isnumeric() else 0
                else:
                    lineupRows[c.allRows[i][1]].CS = 1
        lineupRows[c.allRows[i][1]].Single = lineupRows[c.allRows[i][1]].Hits - lineupRows[c.allRows[i][1]].Double - lineupRows[c.allRows[i][1]].Triple - lineupRows[c.allRows[i][1]].HR
        c.close()
    return lineupRows       

class Lineup:
    #Lineup    
    game = 0
    team = 0
    player = 0
    player_bat_num = 0
    player_pos = ''
    userID = ''
    
    #Batting Data
    AB = 0 #1
    Hits = 0 #3
    BB = 0 #5
    HBP = 0 #text
    Runs = 0 #2
    RBI = 0 #4
    Single = 0 #text
    Double = 0 #text
    Triple = 0 #text
    HR = 0 #text
    SB = 0 #text
    CS = 0 #text
    
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
        insertSQL = 'insert into "LINEUP" VALUES (%s, %s, %s, %s, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' % \
        (self.game, self.team, self.player, self.player_bat_num, self.player_pos, self.AB, self.Hits, self.BB, self.HBP, self.Runs, self.RBI, self.Single, self.Double, self.Triple, self.HR, self.SB, self.CS)
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
    


            
        

    