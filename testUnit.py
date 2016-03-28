import psycopg2
from PlayResultStats import ProcessPlayLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
filename = '.\\Play by Play Logs\\SAMPLE.EVA'
a = ProcessPlayLog(filename, con)







