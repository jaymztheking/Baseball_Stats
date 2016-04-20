import psycopg2
from BRProcess import ProcessBRPage

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

filename = 'C:\\Users\\JMedaugh\\Desktop\\Baseball_Stats\\Game HTML Saves\\ATL_@_WSN_20160411.html'
x = ProcessBRPage(filename, con)
print x.homeTeamAbb, x.awayTeamAbb





