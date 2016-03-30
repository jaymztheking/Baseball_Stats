import psycopg2
from PlayResultStats import ProcessPlayLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
filename = '.\\Play by Play Logs\\2015ANA.EVA'
a, b, c, d = ProcessPlayLog(filename, con)
con.close()




