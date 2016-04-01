import psycopg2
from PlayerStats import Hitter

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)



sql = 'select "USER_ID" from "HITTER_STATS" where "HEIGHT_INCH" = 0'
cur = con.cursor()
cur.execute(sql)
for x in cur:
    print(x[0])
    player = Hitter(x[0], con)
    player.UpdatePlayerInfo(con)

'''
player = Pitcher('jackj001', con)
player.UpdatePlayerInfo(con)
'''




