from datetime import datetime, date
import csv

offKey = ['R','AB','H','2B','3B','HR','RBI','HBP','BB','SB','CS']
offNum = [21, 22, 23, 24, 25, 26, 29, 30, 33, 34]



def GetGameLogStats(filename):
    games = []
    log = open(filename)
    logReader = csv.reader(log, delimiter=',',quotechar='"' )
    for row in logReader:
        gamedate = datetime.strptime(row[0].replace('"',''), '%Y%m%d').date()
        gameIndex = row[1].replace('"','')
        homeTeamAbb = row[6].replace('"','')
        awayTeamAbb = row[3].replace('"','')
        awayRuns = int(row[9])
        homeRuns = int(row[10])
        awayOff = []
        homeOff = []
        for x in offNum: 
            awayOff.append(int(row[x]))
            homeOff.append(int(row[x+28]))
        games.append([gamedate, gameIndex, awayTeamAbb, homeTeamAbb,[awayRuns]+awayOff,[homeRuns]+homeOff])
    return games

def GetGamesfromDB(gdate, aTeam, hTeam, con):
    games = []   
    cur = con.cursor()
    sql = '''
    SELECT 
	"GAME"."GAME_DATE",
	"GAME"."GAME_TIME",
	"AWAY_TEAM"."TEAM_ABBREV",
	"HOME_TEAM"."TEAM_ABBREV",
	"GAME"."AWAY_RUNS" as "AWAY_RUNS",
	sum("LINEUP"."AT_BATS") as "AWAY_AB",
	sum("LINEUP"."HITS") as "AWAY_HITS",
	sum("LINEUP"."2B") as "AWAY_2B",
	sum("LINEUP"."3B") as "AWAY_3B",
	sum("LINEUP"."HR") as "AWAY_HR",
	sum("LINEUP"."RBI") as "AWAY_RBI",
	sum("LINEUP"."HBP") as "AWAY_HBP",
	sum("LINEUP"."BB") as "AWAY_BB",
	sum("LINEUP"."SB") as "AWAY_SB",
	sum("LINEUP"."CS") as "AWAY_CS"
FROM "GAME"
INNER JOIN "TEAM" "HOME_TEAM" on "GAME"."HOME_TEAM_KEY" = "HOME_TEAM"."TEAM_KEY"
INNER JOIN "TEAM" "AWAY_TEAM" on "GAME"."AWAY_TEAM_KEY" = "AWAY_TEAM"."TEAM_KEY"
INNER JOIN "LINEUP" on "GAME"."GAME_KEY" = "LINEUP"."GAME_KEY" and "GAME"."AWAY_TEAM_KEY" = "LINEUP"."TEAM_KEY"
WHERE "GAME_DATE" = \'%s\' and "HOME_TEAM"."TEAM_ABBREV" = \'%s\' and "AWAY_TEAM"."TEAM_ABBREV" = \'%s\'
GROUP BY
	"GAME"."GAME_DATE",
	"GAME"."GAME_TIME",
	"AWAY_TEAM"."TEAM_ABBREV",
	"HOME_TEAM"."TEAM_ABBREV",
	"GAME"."AWAY_RUNS"
ORDER BY
	"GAME"."GAME_TIME" ''' % (gdate.strftime('%Y-%m-%d'), hTeam, aTeam)
    cur.execute(sql)
    games = cur.fetchall()
    return games
    
filename = '.\\GL2015.TXT'
pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
validGames = GetGameLogStats(filename)
for game in validGames:
    myGame = GetGamesfromDB(game[0],game[2],game[3], con)
    if len(myGame) == 1:
        myStats = myGame[0][4:]
        theirStats = game[4]
        for i in range(len(offNum)):
            #print(int(myStats[i]), int(theirStats[i]), offKey[i])
            if int(myStats[i]) != int(theirStats[i]):
                print('MISMATCH!', game[0], game[2],game[3], offKey[i], int(myStats[i]), int(theirStats[i]))
#myGames = GetGamesfromDB(date(2015,7,21),'MIN','ANA', con)
con.close()