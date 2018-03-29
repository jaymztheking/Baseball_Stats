import psycopg2
import os
import datetime
import databaseconfig as cfg
from bbUtils import GetGameKey, GetTeamfromAbb, GetHitterKey


def SetRBIFalse(game, hitter, playNum, con):
    sql = 'update play set rbi_elig = False ' \
          'where game_key = %s and hitter_key = %s and play_seq_no = %s' \
          % (game, hitter, playNum)
    cur.execute(sql)
    cur.execute('COMMIT;')


def FixRBI(filename, con):
    text = open(filename, 'a')
    text.write('\nid,dunzo')
    text.close()
    text = open(filename,'r')
    game = 0
    playInd = 0
    hTeam = 0
    aTeam = 0
    date = datetime.date(1500,1,1)
    time = ''
    lineup = {}
    inEligPlays = []

    for line in text:
        line = line.replace('!', '')
        row = line.split(',')
        rowType = row[0]

        #Get Game Key
        if rowType == 'info':
            att = row[1]
            if att == 'visteam':
                aAbb = row[2].strip()
                if aTeam == 0:
                    aTeam = GetTeamfromAbb(aAbb, 'RS', con)
            elif att == 'hometeam':
                hAbb = row[2].strip()
                if hTeam == 0:
                    hTeam = GetTeamfromAbb(hAbb, 'RS', con)
            elif att == 'date':
                datePieces = row[2].split('/')
                date = datetime.date(int(datePieces[0]), int(datePieces[1]), int(datePieces[2]))
            elif att == 'starttime':
                time = row[2].strip()

        #Lineup Dictionary
        elif rowType == 'start':
            userID = row[1]
            lineup[userID] = GetHitterKey(userID, 'RS', con)

        #Add Pinch Hitters to Lineup
        elif rowType == 'sub':
            if int(row[5]) == 11:
                userID = row[1]
                lineup[userID] = GetHitterKey(userID, 'RS', con)

        #Scan Plays for RBI Ineligibility
        elif rowType == 'play':
            userID = row[3].strip()
            playInd += 1
            playStr = row[6]
            if ('NR' in playStr):
                inEligPlays.append((lineup[userID],playInd))

        #Reached End of Game
        elif rowType == 'id':
            if date != datetime.date(1500, 1, 1):
                game = GetGameKey(hTeam, aTeam, date, time, con)
                for play in inEligPlays:
                    print(play)
                    SetRBIFalse(game, play[0], play[1], con)
                game = 0
                playInd = 0
                lineup = {}
                inEligPlays.clear()
                date = datetime.date(1500, 1, 1)


con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
cur = con.cursor()
year = 2017
while year> 2016:
    for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
            print(file)
            if '.EV' in file[1]:
                filename = '.\\Play by Play Logs\\'+str(year)+'\\'+file[1]
                FixRBI(filename, con)
    year -= 1
con.close()