from bbUtils import GetRSConversion, GetTeamfromAbb
from datetime import date
import psycopg2

def AddSchedule(filename, con):
    diffA = GetRSConversion()
    cur = con.cursor()
    gameDate = None
    gameNum = 1
    homeTeam = 0
    awayTeam = 0
    homeNum = 0
    awayNum = 0
    sched = open(filename)
    for line in sched:
        row = line.split(',')
        gameDate = date(int(row[0][1:5]),int(row[0][5:7]), int(row[0][7:9]))
        gameNum = int(row[1].strip('"'))
        if gameNum == 0:
            gameNum = 1
        abb = row[3].strip('"')
        if abb in diffA.keys():
            abb = diffA[abb]
        awayTeam = GetTeamfromAbb(abb, con)
        awayNum = int(row[5].strip('"'))
        abb = row[6].strip('"')
        if abb in diffA.keys():
            abb = diffA[abb]
        homeTeam = GetTeamfromAbb(abb, con)
        homeNum = int(row[8].strip('"'))
        sql = 'INSERT INTO "SCHEDULE" VALUES (\'%s\', %s, %s, %s, %s, %s, FALSE)' % (gameDate.strftime('%Y-%m-%d'), homeTeam, awayTeam, gameNum, homeNum, awayNum)
        cur.execute(sql)
    cur.execute('COMMIT')
pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
AddSchedule('.\\Schedules\\2015sked.csv', con)
con.close()
    