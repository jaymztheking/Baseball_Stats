from Baseball import Game
from datetime import date, time
import databaseconfig as cfg
import psycopg2

con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
a = Game()
a.values['game_date'] = date(1234,1,1)
a.values['game_time'] = time(1,1,1)
a.values['park_key'] = 1
a.values['home_team_key'] = 1
a.values['away_team_key'] = 2
print(a.DBInsert(con))
print(a.inserted)
