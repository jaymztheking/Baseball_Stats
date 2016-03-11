from datetime import date
import psycopg2
from LineupStats import *
from PitchingStats import *
from GameStats import Game
from PitchingStats import GetPitchRoster

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
url = "http://www.baseball-reference.com/boxes/DET/DET201504060.shtml"
url1 = "http://www.baseball-reference.com/boxes/HOU/HOU201504060.shtml"


lineup1 = GetLineups(16, url, con)
lineup2 = GetLineups(17, url1, con)




