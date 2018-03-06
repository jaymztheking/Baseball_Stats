import psycopg2
import os
import databaseconfig as cfg
from RetroSheetProcess import ProcessRSLog

con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
cur = con.cursor()
cur.execute("Select * from team where team_key = 9")
tst = cur.fetchall()
print(tst)
year = 2017
while year> 2016:
    for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
            print(file)   
            if '.EV' in file[1]:
                filename = '.\\Play by Play Logs\\'+str(year)+'\\'+file[1]
                ProcessRSLog(filename, con)
    year -= 1
con.close()


