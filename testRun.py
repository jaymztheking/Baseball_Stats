import date
import psycopg2

date = date(2015,09,15)
con = psycopg2.connect("dbname=bbstats user=bbadmin")
games = GetGames(date, con)

