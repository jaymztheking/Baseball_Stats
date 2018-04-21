from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd
import os
from Baseball import Team

#
# teamfile = RSLog('.\\Play by Play Logs\\2017\\2017CHN.EVN')
# results = teamfile.scrape()

# # Run Totals By Game
# dic = {}
# games = []
# sbs= []
# for game in results['games']:
# 	print(game)
# 	linesb = 0
# 	for hitter in results['lineups'][game]:
# 		line = results['lineups'][game][hitter]
# 		if line.team_key == 13:
# 			linesb += line.sb
# 	sbs.append(linesb)
# 	games.append(game)
# dic= {'game': games, 'sb': sbs}
# df = pd.DataFrame(data=dic)
# print(games)
# df.to_csv('anasb2017.csv')


#Lines for Game
# for hitter in results['lineups']['CHN201708010']:
# 	line = results['lineups']['CHN201708010'][hitter]
# 	print(hitter, line.plate_app, line.at_bat)
#
# #Inning Plays
# for play in results['plays']['ANA201705070']:
# 	base = results['bases']['ANA201705070'][play.play_seq_no-1]
# 	if int(play.inning_num) == 2 and int(play.top_bot_inn) == 1:
# 		print(vars(play))
# 		print(vars(base))
# 		print('')

year = 2017
teamlookup = Team().get_team_key_to_br_team_lookup()
mydict = {}
results = {}
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	if file[1][-3:-1] == 'EV':
		run = 0
		rbi = 0
		sb = 0
		cs = 0
		home = file[1][4:7]
		teamfile = RSLog('.\\Play by Play Logs\\'+str(year)+'\\%s' % file[1])
		results = teamfile.scrape()
		for l in results['lineups']:
			for m in results['lineups'][l]:
				x = results['lineups'][l][m]
				team = teamlookup[x.team_key]
				if team not in mydict.keys():
					mydict[team]= {}
					mydict[team]['run'] = 0
					mydict[team]['rbi'] = 0
					mydict[team]['sb'] = 0
					mydict[team]['cs'] = 0
				mydict[team]['run'] += x.runs
				mydict[team]['rbi'] += x.rbi
				mydict[team]['sb'] += x.sb
				mydict[team]['cs'] += x.cs

team = []
run = []
rbi = []
sb = []
cs = []
for key in mydict.keys():
	team.append(key)
	run.append(mydict[key]['run'])
	rbi.append(mydict[key]['rbi'])
	sb.append(mydict[key]['sb'])
	cs.append(mydict[key]['cs'])
otherdict = {'team': team, 'runs': run, 'rbi': rbi, 'sb': sb, 'cs': cs}
df = pd.DataFrame(data=otherdict, columns=['team','runs','rbi','sb','cs'])
df.to_csv('result.csv')
