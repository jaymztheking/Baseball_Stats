from bbUtils import GetGameKeys, GetHitterKeyfromLU, GetTeamfromAbb
import psycopg2
from datetime import date

def processPlayLog(filename, con):
    diffAbb = {}
    diffAbb['CHN'] = 'CHC'    
    diffAbb['CHA'] = 'CHW'
    diffAbb['ANA'] = 'LAA'
    diffAbb['KCA'] = 'KCR'
    diffAbb['TBA'] = 'TBR'
    diffAbb['NYA'] = 'NYY'
    diffAbb['SDN'] = 'SDP'
    diffAbb['NYN'] = 'NYM'
    diffAbb['WAS'] = 'WSN'
    diffAbb['SFN'] = 'SFG'
    diffAbb['LAN'] = 'LAD'
    diffAbb['SLN'] = 'STL'
    text = open(filename)
    startSit = 1
    awayTeam = None
    homeTeam = None
    homeTeamAbb = ''
    awayTeamAbb = ''
    gameDate = None
    gameKey = None
    awayPitcherKey = None
    homePitcherKey = None
    for line in text:
        row = line.split(',')
        rowType = row[0]
        gameIndex = 0
        #Grab game info to pull up game key
        if rowType == 'info':
            att = row[1]
            if att == 'visteam':
                awayTeamAbb = row[2].strip()
                if awayTeam == None:
                    if awayTeamAbb in diffAbb.keys():
                        awayTeamAbb = diffAbb[awayTeamAbb]
                    awayTeam = GetTeamfromAbb(awayTeamAbb, con)
                    if awayTeam == None:
                        print(awayTeamAbb)
            elif att == 'hometeam':
                homeTeamAbb = row[2].strip() 
                if homeTeam == None:
                    if homeTeamAbb in diffAbb.keys():
                        homeTeamAbb = diffAbb[homeTeamAbb]
                    homeTeam = GetTeamfromAbb(homeTeamAbb, con)
            elif att == 'date':
                datePieces = row[2].split('/')
                gameDate = date(int(datePieces[0]),int(datePieces[1]),int(datePieces[2]))
            elif att == 'number' and row[2]>0:
                gameIndex = int(row[2])-1
        elif gameKey == None and gameDate != None and homeTeam != None and awayTeam != None:
            try:
                gameKey = GetGameKeys(homeTeam, awayTeam, gameDate, con)[gameIndex]
            except IndexError:
                gameKey = None
                continue
            
        #Grab hitter keys from lineup
        elif rowType == 'start':
            if gameKey != None:
                if int(row[3]) == 0 and int(row[4]) > 0:
                    hitterKey = GetHitterKeyfromLU(gameKey, awayTeam, int(row[4]), con)
                elif int(row[3]) == 1 and int(row[4]) > 0:
                    hitterKey = GetHitterKeyfromLU(gameKey, homeTeam, int(row[4]), con)
            if hitterKey == None:
                print(row[2])
            
        #Change pitcher keys somehow
            
        #Grab play-by-play stuff
        elif rowType == 'aplay':
           pitchSeq = row[5]
           innPre = 'Top' if row[2]== '0' else 'Bot'
           inning = innPre + ' '+str(row[1])
           print(inning)
           
        #New game found, reset everything   
        elif rowType == 'id':
            awayTeam = None
            awayTeamAbb = ''
            gameDate = None
            gameKey = None
            startSit = 1
            


class PitchResult:
    gameKey = 0 #done
    hitterKey = 0
    pitcherKey = 0
    startSituationKey = 0
    inning = '' #done
    strikeCount = 0
    ballCount = 0
    pitchSeq = '' #done
    contactStrikes = 0
    swingStrikes = 0
    lookStrikes = 0
    playType = ''
    hit = False
    resultOuts = 0
    endSituationKey = 0
    ballLoc = ''
    ballType = ''
    runScored = False
    RBI = 0
    
    def __init__(self, gk, hk, pk, sk):
        self.gameKey = gk
        self.hitterKey = hk
        self.pitcherKey = pk
        self.startSituationKey = sk
        
    def ProcessPitchSeq(self):
        if self.pitchSeq != '':
            pass
    
pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
processPlayLog('.\\Play by Play Logs\\2015DET.EVA', con)