from Retro import RSLog
import time

'''
start = time.time()
x = RSLog('.\\Play by Play Logs\\2017\\2017ANX.EVA')
x.ParseLog()
end = time.time()
print(end-start)
'''

from Baseball import Hitter
newguys = []
newguy = Hitter()
newguy.rs_user_id = 'gonzc001'
newguy.GetInfofromRS()
newguys.append(newguy)
newguy = Hitter()
newguy.rs_user_id = 'altuj001'
newguy.GetInfofromRS()
newguys.append(newguy)
Hitter().AddNewHitters(newguys)
print(Hitter().GetHitterRSLookup())






