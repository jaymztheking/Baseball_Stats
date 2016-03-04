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
    parms = 0
    b = LineupParser()
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    team = 'A'
    atm = GetTeam(gameKey, team, con)
    htm = GetTeam(gameKey, 'H', con)
    for i in range(2,len(b.pieces)):
        if b.pieces[i].isdigit():
            batnum = int(b.pieces[i])
            parms += 1
        elif b.pieces[i][:9] == '/players/':
            userid = b.pieces[i].split('/')[-1].replace('.shtml','')
            parms += 1
        elif b.pieces[i] in positions:
            pos = b.pieces[i]
            parms += 1
        else:
            name = b.pieces[i]
            parms += 1

        if parms == 4:
            if pos != '':
                if pos != 'P':
                    if team == 'H':
                        tm = htm
                    else:
                        tm = atm
                    lineupRows[name] = Lineup(gameKey, tm, name, batnum, pos, userid, con)
               
                
            pos = ''
            parms = 0
            if team == 'A':
                team = 'H'
            else:
                team = 'A'
            
    return lineupRows

def GetLineupData(lineups, url, con):
    b = BattingDataParser()
    gameKey = lineups.values()[0].game
    team = 'A'
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    lastBatNum = 1
    for i in range(1, len(b.allRows)):
        if len(b.allRows[i]) >1 and b.allRows[i][1] in lineups.keys():
            currentLineup = lineups[b.allRows[i][1]]
            lastBatNum = currentLineup.player_bat_num
        elif len(b.allRows[i]) >1 and b.allRows[i][1] == 'Batting':
            team = 'H'
            lastBatNum = 1
            continue
        elif len(b.allRows[i])>2 and b.allRows[i][2] != 'P' and b.allRows[i][1] != 'Team Totals' and int(b.allRows[i][3])>0:
            lineups[b.allRows[i][1]] = Lineup(gameKey, GetTeam(gameKey, team, con), b.allRows[i][1], lastBatNum, b.allRows[i][2], b.allRows[i][0] , con)
            currentLineup = lineups[b.allRows[i][1]]
        else: 
            continue
        
        currentLineup.AB = int(b.allRows[i][3])
        currentLineup.Hits = int(b.allRows[i][5])
        currentLineup.BB = int(b.allRows[i][7])
        currentLineup.Runs = int(b.allRows[i][4])
        currentLineup.RBI = int(b.allRows[i][6])
        
        text = b.allRows[i][-1].split(',')
        for t in text:
            if 'HBP' in t:
                if '*' in t:
                    currentLineup.HBP = int(t[:t.find('*')])
                else:
                    currentLineup.HBP = 1
            elif '2B' in t:
                if '*' in t:
                    currentLineup.Double = int(t[:t.find('*')])
                else:
                    currentLineup.Double = 1
            elif '3B' in t:
                if '*' in t:
                    currentLineup.Triple = int(t[:t.find('*')])
                else:
                    currentLineup.Triple = 1
            elif 'HR' in t:
                if '*' in t:
                    currentLineup.HR = int(t[:t.find('*')])
                else:
                    currentLineup.HR = 1
            elif 'SB' in t:
                if '*' in t:
                    currentLineup.SB = int(t[:t.find('*')])
                else:
                    currentLineup.SB = 1
            elif 'CS' in t:
                if '*' in t:
                    currentLineup.CS = int(t[:t.find('*')])
                else:
                    currentLineup.CS = 1
        currentLineup.Single = currentLineup.Hits - currentLineup.Double - currentLineup.Triple - currentLineup.HR
    
    return lineups       

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
    


            
        

    