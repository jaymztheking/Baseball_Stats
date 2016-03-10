from datetime import date
import psycopg2
import urllib2
from GameStats import Game
from LineupStats import GetLineups, GetLineupData
from BRParser import GamesParser

def InsertGames(date, con):
    url = "http://www.baseball-reference.com/games/standings.cgi?date="+date.strftime('%Y-%m-%d')
    b = GamesParser()
    b.games = []
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    lineupRows = []
    for game in b.games:
        myGame = Game(game[0], game[1], date, con)
        myGame.GetBRLineScore(game[2])
        myGame.GetBRWeatherInfo(game[2])
        myGame.GetBRGameTime(game[2], con)
        if myGame.InsertStats(con):
            print('Row inserted in GAME table')
        lineupRows = GetLineups(myGame.gameKey)
        lineupRows = GetLineupData(lineupRows, game[2], con)
        for x in lineupRows:
            x.InsertLineupRow(con)

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)


print('\n\n')
mydate = date(2015,5,31)
print(mydate.isoformat())
InsertGames(mydate, con)
con.close()
