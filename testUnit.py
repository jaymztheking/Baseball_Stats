import psycopg2
import os
from RetroSheetProcess import ProcessRSLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

path = os.path.dirname(os.path.abspath(__file__))

#** BR Test File ** filename = path+'\\Test Files\\CHC_@_LAA_20160405.html'
filename = 'C:\Users\JMedaugh\Desktop\PBP\SAMPLE.EVA'

a = ProcessRSLog(filename, con)







