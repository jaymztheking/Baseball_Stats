import psycopg2
import os
from PlayResultStats import ProcessPlayLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
year = 2015
#Real Deal

while year > 1992:
    print year
    for file in enumerate(os.listdir('.\\Play by Play Logs\\%s' % year)):
        print(file)   
        if '.EV' in file[1]:
            filename = '.\\Play by Play Logs\\%s\\' % year +file[1]
            a, b, c, d = ProcessPlayLog(filename, con)
    year -= 1


#Debug
'''
filename = '.\\Play by Play Logs\\SAMPLE.EVA'
a, b, c, d = ProcessPlayLog(filename, con)
'''

con.close()




