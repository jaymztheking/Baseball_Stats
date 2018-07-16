from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd
import os
from sqlalchemy import UniqueConstraint
from Baseball import Hitter, Pitcher, PitchBoxScore, HitBoxScore, Play, Base, Game, engine, Team


def make_team_csv(year):
	teamlook = Team.get_team_key_to_br_team_lookup()
	pitchdict = {}
	teamstats= {
		'wins': 'win',
		'losses': 'loss',
		'cg': 'complete_game',
		'cgso': 'shut_out',
		'saves': 'save',
		'ip': 'ip',
		'hits': 'hits',
		'runs': 'runs',
		'earned_runs': 'earned_runs',
		'hr': 'hr',
		'bb': 'bb',
		'ibb': 'ibb',
		'so': 'k',
		'hbp': 'hbp',
		'balks': 'blk',
		'wp': 'wp',
		'bf': 'bf'
	}

	for file in enumerate(os.listdir(os.path.join('.', 'Play by Play Logs', str(year)))):
		print(file[1])
		if file[1][-3:-1] == 'EV':
			teamfile = RSLog(os.path.join('.', 'Play by Play Logs', str(year), file[1]))
			results = teamfile.scrape()
			for game in results['rosters'].keys():
				for pitcher in results['rosters'][game]:
					x = results['rosters'][game][pitcher]
					team = teamlook[x.team_key]
					if team not in pitchdict.keys():
						pitchdict[team] = {}
						for a in teamstats.keys():
							pitchdict[team][a] = 0
					for a in teamstats.keys():
						pitchdict[team][a] += int(getattr(x, teamstats[a]))

	csvdict = {'team': []}
	for x in pitchdict.keys():
		csvdict['team'].append(x)
		for y in pitchdict[x].keys():
			if y not in csvdict.keys():
				csvdict[y] = []
			csvdict[y].append(pitchdict[x][y])
	df = pd.DataFrame(data=csvdict)
	cols = []
	cols.append('team')
	for a in teamstats.keys():
		cols.append(a)
	df.to_csv('teampitch%s.csv' % year, columns=cols)

def make_player_csv(year):
	pitchlook = Pitcher.get_pitcher_name_lookup()
	pitchdict = {}
	pitchstats = {
		'wins': 'win',
		'losses': 'loss',
		'cg': 'complete_game',
		'cgso': 'shut_out',
		'saves': 'save',
		'ip': 'ip',
		'hits': 'hits',
		'runs': 'runs',
		'earned_runs': 'earned_runs',
		'hr': 'hr',
		'bb': 'bb',
		'ibb': 'ibb',
		'so': 'k',
		'hbp': 'hbp',
		'balks': 'blk',
		'wp': 'wp',
		'bf': 'bf'
	}

	for file in enumerate(os.listdir(os.path.join('.', 'Play by Play Logs', str(year)))):
		print(file[1])
		if file[1][-3:-1] == 'EV':
			teamfile = RSLog(os.path.join('.', 'Play by Play Logs', str(year), file[1]))
			results = teamfile.scrape()
			for game in results['rosters'].keys():
				for pitcher in results['rosters'][game]:
					x = results['rosters'][game][pitcher]
					pitcher_name = pitchlook[pitcher]
					if pitcher_name not in pitchdict.keys():
						pitchdict[pitcher_name] = {}
						for a in pitchstats.keys():
							pitchdict[pitcher_name][a] = 0
					for a in pitchstats.keys():
						pitchdict[pitcher_name][a] += int(getattr(x, pitchstats[a]))

	csvdict = {}
	csvdict['game'] = []
	for x in pitchdict.keys():
		csvdict['name'].append(x)
		for y in pitchdict[x].keys():
			if y not in csvdict.keys():
				csvdict[y] = []
			csvdict[y].append(pitchdict[x][y])
	df = pd.DataFrame(data=csvdict)
	cols = []
	cols.append('name')
	for a in pitchstats.keys():
		cols.append(a)
	df.to_csv('pitcherspitch%s.csv' % year, columns=cols)

def make_game_log_csv(year):
	gamedict = {}
	teamlookup = Team().get_team_key_to_br_team_lookup()
	pitchstats = {
		'ip'			: 	'ip',
		'hits'			:	'hits',
		'runs'			:	'runs',
		'earned_runs'	:	'earned_runs',
		'bb'			:	'bb',
		'so'			:	'k',
		'hr'			:	'hr',
		'hbp'			:	'hbp',
		'bf'			:	'bf',
		'pit'			:	'pitch_count',
		'str'			:	'strikes'
	}

	for file in enumerate(os.listdir(os.path.join('.', 'Play by Play Logs', str(year)))):
		print(file[1])
		if file[1][-3:-1] == 'EV':
			teamfile = RSLog(os.path.join('.', 'Play by Play Logs', str(year), file[1]))
			results = teamfile.scrape()
			for game in results['rosters'].keys():
				for pitcher in results['rosters'][game]:
					x = results['rosters'][game][pitcher]
					gameteam = game+teamlookup[x.team_key]
					if gameteam not in gamedict.keys():
						gamedict[gameteam] = {}
						for a in pitchstats.keys():
							gamedict[gameteam][a] = 0
					for a in pitchstats.keys():
						gamedict[gameteam][a] += int(getattr(x, pitchstats[a]))

	csvdict = {}
	csvdict['gamedate'] = []
	csvdict['team'] = []
	for x in gamedict.keys():
		csvdict['gamedate'].append(str(x[3:12]))
		csvdict['team'].append(str(x[12:15]))
		for y in gamedict[x].keys():
			if y not in csvdict.keys():
				csvdict[y] = []
			csvdict[y].append(gamedict[x][y])
	print(csvdict)
	df = pd.DataFrame(data=csvdict)
	cols = []
	cols.append('gamedate')
	cols.append('team')
	for a in pitchstats.keys():
		cols.append(a)
	df = df.sort_values(by=['team', 'gamedate'])
	df.to_csv('gamepitches%s.csv' % year, columns=cols)


def make_game_pitcher_log_csv(year, gameid):
	gamedict = {}
	teamlookup = Team().get_team_key_to_br_team_lookup()
	pitchstats = {
		'ip'			: 	'ip',
		'hits'			:	'hits',
		'runs'			:	'runs',
		'earned_runs'	: 'earned_runs',
		'bb'	 		:	'bb',
		'so'			:	'k',
		'hr'			:	'hr',
		'hbp'			:	'hbp',
		'bf'			:	'bf',
		'pit'			:	'pitch_count',
		'str'			:	'strikes'
	}

	for file in enumerate(os.listdir(os.path.join('.', 'Play by Play Logs', str(year)))):
		print(file[1])
		if file[1][-3:-1] == 'EV':
			teamfile = RSLog(os.path.join('.', 'Play by Play Logs', str(year), file[1]))
			if gameid[0:3] == file[1][4:7]:
				results = teamfile.scrape(gameid)
				for pitcher in results['rosters']:
					x = results['rosters'][pitcher]
					if pitcher not in gamedict.keys():
						gamedict[pitcher] = {}
						for a in pitchstats.keys():
							gamedict[pitcher][a] = 0.0
					for a in pitchstats.keys():
						gamedict[pitcher][a] += getattr(x, pitchstats[a])

	csvdict = {}
	csvdict['pitcher'] = []
	for x in gamedict.keys():
		csvdict['pitcher'].append(str(x))
		for y in gamedict[x].keys():
			if y not in csvdict.keys():
				csvdict[y] = []
			csvdict[y].append(gamedict[x][y])
	print(csvdict)
	df = pd.DataFrame(data=csvdict)
	cols = []
	cols.append('pitcher')
	for a in pitchstats.keys():
		cols.append(a)
	df.to_csv('gamepitcher%s.csv' % gameid, columns=cols)

make_game_pitcher_log_csv(2017, 'ARI201704020')