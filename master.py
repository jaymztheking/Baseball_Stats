from Retro import RSLog
import os
import time

start = time.time()
print(time.strftime('%I:%M:%S %p', time.localtime(start)))
year = 2017
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	teamfile = RSLog('.\\Play by Play Logs\\'+str(year)+'\\%s' % file[1])
	results = teamfile.scrape()
	teamfile.add_to_db(results['games'], results['lineups'], results['rosters'], results['plays'], results['bases'])
	print('Done!')
	print(time.strftime('%I:%M:%S %p', time.localtime(time.time())))