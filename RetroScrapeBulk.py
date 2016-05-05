import psycopg2
import os
from RetroSheetProcess import ProcessRSLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
year = 2015
while year> 1992:
    for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
            print(file)   
            if '.EV' in file[1]:
                filename = '.\\Play by Play Logs\\'+str(year)+'\\'+file[1]
                ProcessRSLog(filename, con)
    year -= 1




