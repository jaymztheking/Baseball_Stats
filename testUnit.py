import psycopg2
from RetroSheetProcess import ProcessRSLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

#filename = 'C:\\Users\\JMedaugh\\Desktop\\SAMPLE.EVA'
filename = 'C:\\Users\\James\\Desktop\\Baseball_Stats\\Play by Play Logs\\SAMPLE.EVA'
p, l, r, g = ProcessRSLog(filename, con)




