from datetime import date
import psycopg2
import urllib2
from GameStats import Game
from LineupStats import GetLineups
from PitchingStats import GetPitchRoster
from BRParser import GamesParser

def InsertGames(date, con):
    url = "http://www.baseball-reference.com/games/standings.cgi?date="+date.strftime('%Y-%m-%d')
    b = GamesParser()
    b.games = []
    i = 0
    html = urllib2.urlopen(url).read().decode('utf-8')
    b.feed(html)
    for game in b.games:
        print(game[0], game[1])
        myGame = Game(game[0], game[1], date, con)
        myGame.GetBRLineScore(game[2])
        myGame.GetBRWeatherInfo(game[2])
        myGame.GetBRGameTime(game[2], con)
        if myGame.InsertStats(con):
            print('Row inserted in GAME table')
    
        lrRows = GetLineups(myGame.gameKey, game[2], con)
        for x in lrRows.values():
            x.InsertLineupRow(con)
        print('Inserted '+str(len(lrRows))+' rows into LINEUP table')
        pitch = GetPitchRoster(myGame.gameKey, game[2], con).values()
        for y in pitch:
            y.InsertRosterRow(con)
        print('Inserted '+str(len(pitch))+' rows into PITCH_ROSTER table')

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)


for y in range(4,10):
    for i in range(6,31):
        print('\n\n')
        mydate = date(2015,y,i)
        print(mydate.isoformat())
        InsertGames(mydate, con)
con.close()