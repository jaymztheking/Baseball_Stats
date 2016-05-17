import psycopg2
from BRProcess import ProcessBRPage

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbtest user=bbadmin host=192.168.1.111 password=%s" % pw)
filename = 'C:\Users\JMedaugh\Desktop\SDP_@_COL_20160410.html'

a, b = ProcessBRPage(filename, con)






