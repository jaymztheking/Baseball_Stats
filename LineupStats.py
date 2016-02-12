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
    minBat = 1
    for i in range(2,len(b.pieces)):
        if b.pieces[i].isdigit():
            batnum = b.pieces[i]
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
                if team == 'A' and pos != 'P':
                    lineupRows[name] = Lineup(gameKey, GetTeam(gameKey, 'A', con), name, batnum, pos, userid, con)
                    minBat = batnum
                elif pos != 'P':
                    lineupRows[name] = Lineup(gameKey, GetTeam(gameKey, 'H', con), name, batnum, pos, userid, con)
            pos = ''
            parms = 0
            
    return lineupRows

def GetLineupData(lineups, url, con):
    b = BattingDataParser()
    gameKey = lineups.values()[0].game
    players = GetLineupPlayers(gameKey, con)
    valid = False
    team = 'A'
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    columns = 0
    for i in range(21, len(b.pieces)):
        if b.pieces[i] in lineups.keys():
            valid = True
            currentLineup = lineups[b.pieces[i]]
            lastBatNum = currentLineup.player_bat_num
            columns = 0
        #Need to expand for long term subs (e.g. new RF comes into game for multiple innings)
        elif i < len(b.pieces)-1 and b.pieces[i+1] == 'PH' :
            #insert PH line in lineup  
            lineups[b.pieces[i]] = Lineup(gameKey, GetTeam(gameKey, team, con), b.pieces[i], lastBatNum, 'PH', b.lastAtag , con)
            valid = True
            currentLineup = lineups[b.pieces[i]]
            columns = 0
        elif i < len(b.pieces)-1 and b.pieces[i+1] == 'P':
            columns = 6
            valid = False
            continue
        elif b.pieces[i].isdigit() and columns < 5 and valid:
            if columns == 0:
                if int(b.pieces[i]) == 0:
                    valid = False
                    continue
                currentLineup.AB = int(b.pieces[i])
                columns += 1
            elif columns == 1:
                currentLineup.Runs = int(b.pieces[i])
                columns += 1
            elif columns == 2:
                currentLineup.Hits = int(b.pieces[i])
                columns += 1
            elif columns == 3:
                currentLineup.RBI = int(b.pieces[i])
                columns += 1
            elif columns == 4:
                currentLineup.BB = int(b.pieces[i])
                columns += 1
        elif columns == 5:
            valid = False
            if str(b.pieces[i]).translate(None, ',*').isalpha():
                print(b.pieces[i])       
    return lineups       

class Lineup:
    game = 0
    team = 0
    player = 0
    player_bat_num = 0
    player_pos = ''
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
        insertSQL = 'insert into "LINEUP" VALUES (%s, %s, %s, %s, \'%s\', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);' % \
        (self.game, self.team, self.player, self.player_bat_num, self.player_pos)
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
    


            
        

    