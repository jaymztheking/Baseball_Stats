from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd
import os
from sqlalchemy import UniqueConstraint
from Baseball import Hitter, Pitcher, PitchBoxScore, HitBoxScore, Play, Base, Game, engine, Team


year = 2017
teamlook = Team.get_team_key_to_br_team_lookup()
pitchdict = {}
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	if file[1][-3:-1] == 'EV':
		teamfile = RSLog('.\\Play by Play Logs\\'+str(year)+'\\%s' % file[1])
		results = teamfile.scrape()
		for game in results['rosters'].keys():
			for pitcher in results['rosters'][game]:
				x = results['rosters'][game][pitcher]
				team = teamlook[x.team_key]
				if team not in pitchdict.keys():
					pitchdict[team] = {}
					pitchdict[team]['wins'] = 0
					pitchdict[team]['losses'] = 0
					pitchdict[team]['cg'] = 0
					pitchdict[team]['cgso'] = 0
					pitchdict[team]['saves'] = 0
					pitchdict[team]['ip'] = 0
					pitchdict[team]['hits'] = 0
					pitchdict[team]['runs'] = 0
					pitchdict[team]['earned_runs'] = 0
					pitchdict[team]['hr'] = 0
					pitchdict[team]['bb'] = 0
					pitchdict[team]['ibb'] = 0
					pitchdict[team]['so'] = 0
					pitchdict[team]['hbp'] = 0
					pitchdict[team]['balks'] = 0
					pitchdict[team]['wp'] = 0
					pitchdict[team]['bf'] = 0
				pitchdict[team]['wins'] += int(x.win)
				pitchdict[team]['losses'] += int(x.loss)
				pitchdict[team]['cg'] += int(x.complete_game)
				pitchdict[team]['cgso'] += int(x.shut_out)
				pitchdict[team]['saves'] += int(x.save)
				pitchdict[team]['ip'] += x.ip
				pitchdict[team]['hits'] += x.hits
				pitchdict[team]['runs'] += x.runs
				pitchdict[team]['earned_runs'] += x.earned_runs
				pitchdict[team]['hr'] += x.hr
				pitchdict[team]['bb'] += x.bb
				pitchdict[team]['ibb'] += x.ibb
				pitchdict[team]['so'] += x.k
				pitchdict[team]['hbp'] += x.hbp
				pitchdict[team]['balks'] += x.blk
				pitchdict[team]['wp'] += x.wp
				pitchdict[team]['bf'] += x.bf

csvdict = {}
csvdict['team'] = []
for x in pitchdict.keys():
	csvdict['team'].append(x)
	for y in pitchdict[x].keys():
		if y not in csvdict.keys():
			csvdict[y] = []
		csvdict[y].append(pitchdict[x][y])
df = pd.DataFrame(data=csvdict)
df.to_csv('teampitch2017.csv', columns=['team','wins','losses','cg','cgso','saves','ip','hits','runs','earned_runs','hr','bb','ibb','so','hbp','balks','wp','bf'])
