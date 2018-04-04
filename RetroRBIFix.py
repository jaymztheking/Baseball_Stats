import psycopg2
import os
import datetime
import databaseconfig as cfg
from bbUtils import GetGameKey, GetTeamfromAbb, GetHitterKey
from multiprocessing import Pool


def SetRBIRuns(game, hitter, playNum, runs, con):
    cur = con.cursor()
    sql = 'select rbis_in from play where game_key = %s and play_seq_no = %s'\
        % (game, playNum)
    cur.execute(sql)
    results = cur.fetchall()
    rbis = results[0][0]
    if rbis > 0:
        sql = 'update play set rbis_in =  greatest(runs_in - %d,0)' \
              'where game_key = %s and hitter_key = %s and play_seq_no = %s' \
              % (runs, game, hitter, playNum)
        cur.execute(sql)
        cur.execute('COMMIT;')


def FixRBI(filename, con):
    text = open(filename, 'a')
    text.write('\nid,dunzo')
    text.close()
    text = open(filename,'r')
    game = 0
    playInd = 1
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
            lineup[userID] = GetHitterKey('RS', userID, con)

        #Add Pinch Hitters to Lineup
        elif rowType == 'sub':
            userID = row[1]
            lineup[userID] = GetHitterKey('RS', userID, con)
            if int(row[5]) == 12:
                playInd += 1


        #Scan Plays for RBI Ineligibility
        elif rowType == 'play':
            noRBI = 0
            runstr = ''
            userID = row[3].strip()
            playStr = row[6] if row[6].find('.') == -1 else row[6][row[6].find('.')+1:]
            baseStr = playStr.strip().split(';')
            for runner in baseStr:
                if ('NR' in runner) or ('-H' in runner and '(E' in runner):
                    noRBI +=1
                    runstr += runner
                if ('XH' in runner) and ('E' in runner)and ('MREV' not in runner):
                    noRBI += 1
                    runstr += runner
            if noRBI > 0:
                inEligPlays.append((lineup[userID], playInd, noRBI, runstr))
            playInd += 1

        #Reached End of Game
        elif rowType == 'id':
            if date != datetime.date(1500, 1, 1):
                game = GetGameKey(hTeam, aTeam, date, time, con)
                for play in inEligPlays:
                    print(game, play)
                    SetRBIRuns(game, play[0], play[1], play[2], con)
                game = 0
                playInd = 1
                hTeam = 0
                aTeam = 0
                date = datetime.date(1500, 1, 1)
                time = ''
                lineup = {}
                inEligPlays = []

def unitFunc(file):
    print(file)
    con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
    if '.EV' in file:
        filename = '.\\Play by Play Logs\\' + str(2017) + '\\' + file
        FixRBI(filename, con)
        con.close()

if __name__ == '__main__':
    files = os.listdir('.\\Play by Play Logs\\'+str(2017))
    p = Pool()
    p.map(unitFunc, files)
    print('Done')