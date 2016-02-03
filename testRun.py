from datetime import date
import psycopg2
from GameStats import GetGames

date = date(2015,9,15)
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111")
games = GetGames(date, con)
con.close()
