import psycopg2
import os
from BRProcess import ProcessBRPage

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

path = os.path.dirname(os.path.abspath(__file__))

filename = path+'\\Test Files\\CHC_@_LAA_20160405.html'

x, y = ProcessBRPage(filename, con)
for a in y.pitchers.keys():
    print(a)







