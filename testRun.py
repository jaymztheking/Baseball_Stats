from datetime import date
import psycopg2
from GameStats import InsertGames

pw = raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
for i in range(1,31):
    print('\n\n')
    mydate = date(2015,6,i)
    print(mydate.isoformat())
    InsertGames(mydate, con)
con.cursor().execute('COMMIT;')
con.close()
