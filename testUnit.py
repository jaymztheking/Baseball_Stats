import psycopg2
from PlayResultStats import ProcessPlayLog

pw = 'h4xorz' #raw_input('Password? ')
con = psycopg2.connect("dbname=bbstats user=bbadmin host=192.168.1.111 password=%s" % pw)
filename = '.\\Play by Play Logs\\SAMPLE.EVA'
a, b, c, d = ProcessPlayLog(filename, con)
con.close()
'''
print ('Lines')
batnum = 1
team = 17
while batnum < 11:

    for x in c.keys():
        if c[x].player_bat_num == batnum and c[x].team == team and c[x].player_pos != 'PH':
                print(x,c[x].AB,c[x].Runs,c[x].Hits,c[x].RBI,c[x].BB,'x',c[x].PA)
        elif c[x].player_bat_num == batnum - 1 and c[x].team == team and c[x].player_pos == 'PH' :
                print(x,c[x].AB,c[x].Runs,c[x].Hits,c[x].RBI,c[x].BB,'x',c[x].PA)
    batnum += 1
team = 10
batnum = 1
print('More Lines')
while batnum < 10:

    for x in c.keys():
        if c[x].player_bat_num == batnum and c[x].team == team and c[x].player_pos != 'PH':
                print(x,c[x].AB,c[x].Runs,c[x].Hits,c[x].RBI,c[x].BB,'x',c[x].PA)
        elif c[x].player_bat_num == batnum - 1 and c[x].team == team and c[x].player_pos == 'PH' :
                print(x,c[x].AB,c[x].Runs,c[x].Hits,c[x].RBI,c[x].BB,'x',c[x].PA)
    batnum += 1
'''
print('\n\nPitchers')
for x in b.keys():
    print(x,b[x].team, '%.2f' % b[x].IP,b[x].Hits,b[x].Runs,b[x].earnedRuns,b[x].BB,b[x].K,'---',b[x].pitchCount,b[x].Strikes,b[x].GB,b[x].FB,b[x].LD)




