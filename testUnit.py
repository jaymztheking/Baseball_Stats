import psycopg2
import os
from PlayResultStats import ProcessPlayLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

#Real Deal
'''
for file in enumerate(os.listdir('.\\Play by Play Logs\\')):
    if '.EV' in file[1]:
        filename = '.\\Play by Play Logs\\'+file[1]
        a, b, c, d = ProcessPlayLog(filename, con)
'''

#Debug

filename = '.\\Play by Play Logs\\SAMPLE.EVN'
a, b, c, d = ProcessPlayLog(filename, con)


con.close()




