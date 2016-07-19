import psycopg2
import os
from BRProcess import ProcessBRPage

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)

for file in enumerate(os.listdir('.\\Game HTML Saves\\')):
    filename = '.\\Game HTML Saves\\'+file[1]
    print(filename)
    ProcessBRPage(filename, con)





