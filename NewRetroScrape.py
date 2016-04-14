import psycopg2
import os
from RetroSheetProcess import ProcessRSLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

for file in enumerate(os.listdir('.\\Play by Play Logs\\2015')):
        print(file)   
        if '.EV' in file[1]:
            filename = '.\\Play by Play Logs\\2015\\'+file[1]
            ProcessRSLog(filename, con)




