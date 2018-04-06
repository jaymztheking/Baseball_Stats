import psycopg2
import os
import databaseconfig as cfg
from RetroSheetProcess import ProcessRSLog

con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
cur = con.cursor()
#cur.execute(open(".\\Baseball Database\\SQL Create Table Scripts\\restart.sql","r").read())
year = 2011
while year> 2010:
    for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
            print(file)   
            if '.EV' in file[1]:
                filename = '.\\Play by Play Logs\\'+str(year)+'\\'+file[1]
                ProcessRSLog(filename, con)
            print('Done')
    year -= 1
con.close()


