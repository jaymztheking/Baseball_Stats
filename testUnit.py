from datetime import date
import psycopg2
import urllib2
from LineupStats import *

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
url = "http://www.baseball-reference.com/boxes/BAL/BAL201504100.shtml"#"http://www.baseball-reference.com/boxes/DET/DET201504060.shtml"
lineup = GetLineups(9, url, con)
a = GetLineupData(lineup, url, con)
