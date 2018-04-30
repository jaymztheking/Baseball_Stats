from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd
import os
from Baseball import Team


teamfile = RSLog('.\\Play by Play Logs\\2017\\2017KCA.EVA')
results = teamfile.scrape()

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


################################################################################################
#                                  Gets Stats by Team                                          #
################################################################################################
year = 2017
teamlookup = Team().get_team_key_to_br_team_lookup()
mydict = {}
results = {}
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	if file[1][-3:-1] == 'EV':
		home = file[1][4:7]
		teamfile = RSLog('.\\Play by Play Logs\\'+str(year)+'\\%s' % file[1])
		results = teamfile.scrape()
		for l in results['lineups']:
			for m in results['lineups'][l]:
				x = results['lineups'][l][m]
				team = teamlookup[x.team_key]
				if team not in mydict.keys():
					mydict[team]= {}
					mydict[team]['pa'] = 0
					mydict[team]['ab'] = 0
					mydict[team]['run'] = 0
					mydict[team]['h'] = 0
					mydict[team]['x2b'] = 0
					mydict[team]['x3b'] = 0
					mydict[team]['hr'] = 0
					mydict[team]['rbi'] = 0
					mydict[team]['sb'] = 0
					mydict[team]['cs'] = 0
					mydict[team]['bb'] = 0
					mydict[team]['so'] = 0
					mydict[team]['gdp'] = 0
					mydict[team]['hbp'] = 0
					mydict[team]['sh'] = 0
					mydict[team]['sf'] = 0
					mydict[team]['ibb'] = 0
				mydict[team]['pa'] += x.plate_app
				mydict[team]['ab'] += x.at_bat
				mydict[team]['run'] += x.runs
				mydict[team]['h'] += x.hits
				mydict[team]['x2b'] += x.double
				mydict[team]['x3b'] += x.triple
				mydict[team]['hr'] += x.hr
				mydict[team]['rbi'] += x.rbi
				mydict[team]['sb'] += x.sb
				mydict[team]['cs'] += x.cs
				mydict[team]['bb'] += x.bb
				mydict[team]['so'] += x.so
				mydict[team]['gdp'] += x.gdp
				mydict[team]['hbp'] += x.hbp
				mydict[team]['sh'] += x.sh
				mydict[team]['sf'] += x.sf
				mydict[team]['ibb'] += x.ibb

teams = []
pas = []
abs = []
runs = []
hs = []
x2bs = []
x3bs = []
hrs = []
rbis = []
sbs = []
css = []
bbs = []
sos = []
gdps = []
hbps = []
shs = []
sfs = []
ibbs = []
for key in mydict.keys():
	teams.append(key)
	pas.append(mydict[key]['pa'])
	abs.append(mydict[key]['ab'])
	runs.append(mydict[key]['run'])
	hs.append(mydict[key]['h'])
	x2bs.append(mydict[key]['x2b'])
	x3bs.append(mydict[key]['x3b'])
	hrs.append(mydict[key]['hr'])
	rbis.append(mydict[key]['rbi'])
	sbs.append(mydict[key]['sb'])
	css.append(mydict[key]['cs'])
	bbs.append(mydict[key]['bb'])
	sos.append(mydict[key]['so'])
	gdps.append(mydict[key]['gdp'])
	hbps.append(mydict[key]['hbp'])
	shs.append(mydict[key]['sh'])
	sfs.append(mydict[key]['sf'])
	ibbs.append(mydict[key]['ibb'])
csvdict = {'team': teams, 'pa': pas, 'ab': abs, 'runs': runs, 'h': hs, '2b': x2bs, '3b': x3bs, 'hr': hrs, 'rbi': rbis,
		   'sb': sbs, 'cs': css, 'bb': bbs, 'so': sos, 'gdp': gdps, 'hbp': hbps, 'sh': shs, 'sf': sfs, 'ibb': ibbs}
df = pd.DataFrame(data=csvdict)
df = df.sort_values(by=['team'])
df.to_csv('2017byTeam.csv', columns=['team', 'pa', 'ab', 'runs', 'h', '2b', '3b', 'hr', 'rbi', 'sb', 'cs', 'bb', 'so',
									 'gdp', 'hbp', 'sh', 'sf', 'ibb'])

# ################################################################################################
# #                                  Gets Stats by Game                                          #
# ################################################################################################
#
# year = 2017
# teamlookup = Team().get_team_key_to_br_team_lookup()
# mydict = {}
# results = {}
# for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
# 	print(file[1])
# 	if file[1][-3:-1] == 'EV':
# 		home = file[1][4:7]
# 		teamfile = RSLog('.\\Play by Play Logs\\'+str(year)+'\\%s' % file[1])
# 		results = teamfile.scrape()
# 		for l in results['lineups']:
# 			for m in results['lineups'][l]:
# 				if results['lineups'][l][m].team_key == 7:
# 					x = results['lineups'][l][m]
# 					if l not in mydict.keys():
# 						mydict[l] = {}
# 						mydict[l]['date'] = str(results['games'][l].game_date)
# 						mydict[l]['run'] = 0
# 						mydict[l]['rbi'] = 0
# 						mydict[l]['sb'] = 0
# 						mydict[l]['cs'] = 0
# 					mydict[l]['run'] += x.runs
# 					mydict[l]['rbi'] += x.rbi
# 					mydict[l]['sb'] += x.sb
# 					mydict[l]['cs'] += x.cs
#
# dates = []
# runs = []
# rbis = []
# sbs = []
# css = []
# for key in mydict.keys():
# 	dates.append(mydict[key]['date'])
# 	runs.append(mydict[key]['run'])
# 	rbis.append(mydict[key]['rbi'])
# 	sbs.append(mydict[key]['sb'])
# 	css.append(mydict[key]['cs'])
# csvdict = {'date': dates, 'runs': runs, 'rbi': rbis, 'sb': sbs, 'cs': css}
# df = pd.DataFrame(data=csvdict)
# df = df.sort_values(by=['date'])
# df.to_csv('2017CINgames.csv', columns=['date','runs','rbi','sb','cs'])


