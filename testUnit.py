from datetime import date
import psycopg2
from LineupStats import *
from GameStats import Game

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
url = "http://www.baseball-reference.com/boxes/DET/DET201504060.shtml"
away = 'MIN'
home = 'DET'
day = date(2015,4,6)
'''
myGame = Game(home, away, day, con)
myGame.GetBRLineScore(url)
myGame.GetBRWeatherInfo(url)
myGame.GetBRGameTime(url, con)
myGame.InsertStats(con)
'''
lineup = GetLineups(16, url, con)
GetLineupData(lineup, url, con)
for line in lineup.values():
    line.InsertLineupRow(con)

