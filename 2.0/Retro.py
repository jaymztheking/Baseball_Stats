from Baseball import Game, HitBoxScore, PitchBoxScore, Play, Base, JSONEncoder, Hitter, Pitcher
from GameSim import GameSim
import json, re, csv
from datetime import date


PosLookup = ['X', 'P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'X', 'PH', 'PR']


class RSLog:
	def __init__(self, file):
		self.filename = file
		self.games = {}
		self.gamebases = {}
		self.gameplays = {}
		self.gamelineups = {}
		self.gamepitroster = {}
		with open('TeamLookup.json', 'r') as out:
			self.teams = json.load(out)

	def ResetGame(self):
		self.currentGame = Game()
		self.currentSim = GameSim()
		self.play_seq = 0
		self.lineup = {}
		self.pitroster = {}
		self.plays = []
		self.bases = []

		self.wp = ''
		self.lp = ''
		self.savep = ''

	def AddToGameDicts(self):
		gameid = self.currentGame.values['game_id']
		self.games[gameid] = self.currentGame
		self.gamebases[gameid] = self.bases
		self.gameplays[gameid] = self.plays
		self.gamelineups[gameid] = self.lineup
		self.gamepitroster[gameid] = self.pitroster

	def AddStarters(self):
		for userid in self.lineup.keys():
			if self.lineup[userid].values["position"] == 'P':
				self.pitroster[userid] = PitchBoxScore()
				self.pitroster[userid].values['team_key'] = self.lineup[userid].values['team_key']
				self.pitroster[userid].values['pitch_role'] = 'Starter'
				if self.pitroster[userid].values['team_key'] == self.currentGame.values['home_team_key']:
					self.currentSim.activeHomePitcher = userid
				else:
					self.currentSim.activeAwayPitcher = userid

	def ComputeEndGameStats(self):
		#Game End Stuff
		if self.currentGame.values['home_runs'] > self.currentGame.values['away_runs']:
			self.currentGame.values['home_team_win'] = True
		elif self.currentGame.values['home_runs'] == self.currentGame.values['away_runs']:
			self.currentGame.values['tie'] = True
		#Pitcher Game End Stuff
		self.pitroster[self.wp].values['win'] = True
		self.pitroster[self.lp].values['loss'] = True
		if self.savep != '':
			self.pitroster[self.savep].values['save'] = True
		self.currentGame.values['total_innings'] = self.currentSim.inning
		if self.pitroster[self.wp].values['IP'] == self.currentGame.values['total_innings']:
			self.pitroster[self.wp].values['complete_game'] = True
			if self.currentGame.values['home_runs'] == 0 and \
			self.pitroster[self.wp].values['team_key'] == self.currentGame.values['away_team_key']:
				self.pitroster[self.wp].values['shut_out'] = True
				if self.currentGame.values['home_hits'] == 0:
					self.pitroster[self.wp].values['no_hitter'] = True
			elif self.currentGame.values['away_runs'] == 0 and \
			self.pitroster[self.wp].values['team_key'] == self.currentGame.values['home_team_key']:
				self.pitroster[self.wp].values['shut_out'] = True
				if self.currentGame.values['away_hits'] == 0:
					self.pitroster[self.wp].values['no_hitter'] = True


	def GetBallType(self):
		for x in self.currentPlay.values['play_seq'].split('/')[1:]:
			if re.search('^[0-9]{1,2}$', x) != None:
				self.currentPlay.values['ball_loc'] = x
			if re.search('^B?[LFGP][0-9]', x) != None:
				self.currentPlay.values['ball_loc'] = re.search('^B?[LFGP]([0-9])', x).group(1)
			if re.search('L', x) != None:
				return 'Line Drive'
			if re.search('F', x) != None:
				return 'Fly Ball'
			if re.search('G', x) != None:
				return 'Ground Ball'
			if re.search('P', x) != None and re.search('DP', x) == None:
				return 'Pop Up'
			if re.search('BP', x) != None:
				return 'Bunt Pop'
			if re.search('BL', x) != None:
				return 'Bunt Line Drive'
			if re.search('BG', x) != None:
				return 'Bunt Ground Ball'
		return ''

	def GetPlayType(self):
		playseq = self.currentPlay.values['play_seq']
		playtyp = playseq.split('/')[0]
		playname = ''
		runseq = self.currentBase.values['run_seq']

		# Stolen Base
		if re.search('SB[23H]', playtyp) != None:
			if 'SB2' in playtyp:
				self.currentBase.values['second_stolen'] = True
				if '1-' not in runseq:
					self.currentBase.values['run_seq'] += ';1-2'
			if 'SB3' in playseq:
				self.currentBase.values['third_stolen'] = True
				if '2-' not in runseq:
					self.currentBase.values['run_seq'] += ';2-3'
			if 'SBH' in playseq:
				self.currentBase.values['home_stolen'] = True
				if '3-' not in runseq:
					self.currentBase.values['run_seq'] += ';3-H'
			self.currentBase.values['total_sb'] = self.currentBase.values['second_stolen'] + \
			self.currentBase.values['third_stolen'] + self.currentBase.values['home_stolen']
			playname = 'Stolen Base'

		# Caught Stealing
		if re.search('CS[23H]', playtyp) != None:
			if 'CS2' in playseq:
				self.currentBase.values['second_caught'] = True
				if 'E' not in playseq:
					self.currentBase.values['run_seq'] += ';1X2'
				elif '1-' not in runseq:
					self.currentBase.values['run_seq'] += ';1-2'
			if 'CS3' in playseq:
				self.currentBase.values['third_caught'] = True
				if 'E' not in playseq:
					self.currentBase.values['run_seq'] += ';2X3'
				elif '2-' not in runseq:
					self.currentBase.values['run_seq'] += ';2-3'
			if 'CSH' in playseq:
				self.currentBase.values['home_caught'] = True
				if 'E' not in playseq:
					self.currentBase.values['run_seq'] += ';3XH'
				elif '3-' not in runseq:
					self.currentBase.values['run_seq'] += ';3-H'
			self.currentBase.values['total_cs'] = self.currentBase.values['second_caught'] + \
				self.currentBase.values['third_caught'] + self.currentBase.values['home_caught']
			playname = 'Caught Stealing'

		# Pick Off
		if re.search('PO[^C]', playtyp) != None:
			if 'E' not in runseq:
				self.currentSim.outs += 1
				if 'PO1' in runseq:
					self.currentSim.first_base = ''
				if 'PO2' in runseq:
					self.currentSim.second_base = ''
				if 'PO3' in runseq:
					self.currentSim.third_base = ''
			playname = 'Pick Off'

		# Balk
		if re.search('BK', playtyp) != None:
			playname = 'Balk'

		# Passed Ball
		if re.search('PB', playtyp) != None:
			playname = 'Passed Ball'

		# Wild Pitch
		if re.search('WP', playtyp) != None:
			playname = 'Wild Pitch'

		# Defensive Indifference
		if re.search('DI', playtyp) != None:
			playname = 'Defensive Indifference'

		# Error on Foul
		if re.search('FLE', playtyp) != None:
			playname = 'Error on Foul'

		# Misc
		if re.search('OA', playtyp) != None:
			playname = 'Unknown Runner Activity'

		# Interference
		if re.search('C$', playtyp) != None:
			if 'B-' not in runseq:
				self.currentBase.values['run_seq'] += ';B-1'
			playname = 'Interference'

		# Walks
		if re.search('W(\+|$)', playtyp) != None:
			if 'B-' not in runseq:
				self.currentBase.values['run_seq'] += ';B-1'
			playname = 'Intentional Walk' if 'IW' in playseq else 'Walk'

		# HBP
		if re.search('HP', playtyp) != None:
			if 'B-' not in runseq:
				self.currentBase.values['run_seq'] += ';B-1'
			playname = 'Hit By Pitch'

		# Sac Fly
		if 'SF' in playseq:
			playname = 'Sacrifice Fly'

		# Sac Hit
		if 'SH' in playseq:
			playname = 'Sacrifice Hit'

		# Strikeout
		if re.search('(^|[^B])K', playtyp) != None:
			if 'B-' not in runseq:
				self.currentSim.outs += 1
			playname = 'Strikeout'

		# one Fielding Out
		if re.search('^[0-9]+$', playtyp) != None:
			self.currentPlay.values['ball_loc'] = playseq[0]
			self.currentSim.outs += 1
			playname = 'Out'

		# Force and Tag Outs/Double Play/Triple Play
		if re.search('^[0-9]{1,4}\([B123]\)', playtyp) != None:
			outstr = re.findall('\([B123]\)', playseq)
			self.currentPlay.values['ball_loc'] = playseq[0]
			for a in playseq.split('/'):
				if 'DP' in a and 'NDP' not in a:
					self.currentSim.outs += len(outstr)
					playname = 'Double Play'
					if (self.currentBase.values['run_seq'].count('X') + len(outstr)) == 2 and '(B)' not in outstr:
						self.currentBase.values['run_seq'] += ';B-1'
				if 'TP' in a:
					self.currentSim.outs += 3
					playname = 'Triple Play'
			if playname not in ('Triple Play', 'Double Play'):
				self.currentSim.outs += 1
				playname = 'Out'
				if 'B' not in self.currentBase.values['run_seq'] and '(B)' not in outstr:
					self.currentBase.values['run_seq'] += ';B-1'
			for o in outstr:
				if o == '(1)':
					self.currentSim.first_base = ''
				elif o == '(2)':
					self.currentSim.second_base = ''
				elif o == '(3)':
					self.currentSim.third_base = ''

		# Fielders Choice
		if re.search('FC[0-9]', playtyp) != None:
			playname = 'Fielders Choice'
			self.currentPlay.values['ball_loc'] = re.search('FC([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		# Reach On Error
		if re.search('(^|[^\(])E[0-9]', playtyp) != None and re.search('FLE', playtyp) == None:
			if playname[:9] != 'Sacrifice':
				playname = 'Reach On Error'
			if 'B-' not in self.currentBase.values['run_seq'] or 'BX' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		# Single
		if re.search('^S[0-9]?', playtyp) != None and re.search('SB[23H]', playtyp) == None:
			playname = 'Single'
			if re.search('^S([0-9])', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('S([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		# Double
		if re.search('^D[0-9]?', playtyp) != None and re.search('DI', playtyp) == None:
			playname = 'Double'
			if re.search('^D[0-9]', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('D([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-2'

		# Ground Rule Double
		if re.search('DGR', playtyp) != None:
			playname = 'Ground Rule Double'
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-2'

		# Triple
		if re.search('^T[0-9]?', playtyp) != None:
			playname = 'Triple'
			if re.search('^T[0-9]', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('T([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-3'

		# Home Run
		if re.search('HR', playtyp) != None:
			playname = 'Home Run'
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-H'



		return playname

	def CalcHitBox(self):
		batter = self.currentPlay.values['hitter_key']
		first = self.currentBase.values['start_first']
		second = self.currentBase.values['start_second']
		third = self.currentBase.values['start_third']
		self.lineup[batter].values['plate_app'] += self.currentPlay.values['plate_app']
		self.lineup[batter].values['at_bat'] += self.currentPlay.values['at_bat']
		self.lineup[batter].values['hits'] += self.currentPlay.values['hit']
		self.lineup[batter].values['rbi'] += self.currentBase.values['rbi']
		if self.lineup[batter].values['team_key'] == self.currentGame.values['home_team_key']:
			self.currentGame.values['home_hits'] += self.currentPlay.values['hit']
		else:
			self.currentGame.values['away_hits'] += self.currentPlay.values['hit']
		play = self.currentPlay.values['play_type']
		if play == 'Single':
			self.lineup[batter].values['single'] += 1
		elif play in ('Double', 'Ground Rule Double'):
			self.lineup[batter].values['double'] += 1
		elif play == 'Triple':
			self.lineup[batter].values['triple'] += 1
		elif play == 'Home Run':
			self.lineup[batter].values['hr'] += 1
		elif play in ('Walk', 'Intentional Walk'):
			self.lineup[batter].values['bb'] += 1
			if play == 'Intentional Walk':
				self.lineup[batter].values['ibb'] += 1
		elif play == 'Hit By Pitch':
			self.lineup[batter].values['hbp'] += 1
		elif play == 'Strikeout':
			self.lineup[batter].values['so'] += 1
		if self.currentBase.values['second_stolen'] is True:
			self.lineup[first].values['sb'] += 1
		if self.currentBase.values['third_stolen'] is True:
			self.lineup[second].values['sb'] += 1
		if self.currentBase.values['home_stolen'] is True:
			self.lineup[third].values['sb'] += 1
		if self.currentBase.values['second_caught'] is True:
			self.lineup[first].values['cs'] += 1
		if self.currentBase.values['third_caught'] is True:
			self.lineup[second].values['cs'] += 1
		if self.currentBase.values['home_caught'] is True:
			self.lineup[third].values['cs'] += 1
		return True

	def CalcPitchBox(self):
		if self.currentSim.top_or_bot == 0:
			userid = self.currentSim.activeHomePitcher
		else:
			userid = self.currentSim.activeAwayPitcher
		for pitch in self.currentPlay.values['pitch_seq']:
			if pitch in ('F', 'X', 'L', 'O', 'R', 'T'):
				self.pitroster[userid].values['contact_strikes'] += 1
			elif pitch == 'C':
				self.pitroster[userid].values['look_strikes'] += 1
			elif pitch in ('S', 'M', 'Q', 'K'):
				self.pitroster[userid].values['swing_strikes'] += 1
			elif pitch in ('B', 'H', 'I', 'P', 'U', 'Y'):
				self.pitroster[userid].values['balls'] += 1
		self.pitroster[userid].values['strikes'] = self.pitroster[userid].values['contact_strikes'] + \
			self.pitroster[userid].values['look_strikes'] + self.pitroster[userid].values['swing_strikes']
		self.pitroster[userid].values['pitch_count'] = self.pitroster[userid].values['strikes'] + \
			self.pitroster[userid].values['balls']
		if self.currentPlay.values['ball_type'] in ('Ground Ball', 'Bunt Ground Ball'):
			self.pitroster[userid].values['groundballs'] += 1
		elif self.currentPlay.values['ball_type'] in ('Line Drive', 'Bunt Line Drive'):
			self.pitroster[userid].values['line_drives'] += 1
		elif self.currentPlay.values['ball_type'] in ('Fly Ball', 'Pop Up', 'Bunt Pop'):
			self.pitroster[userid].values['flyballs'] += 1
		if self.currentPlay.values['play_type'] == 'Strikeout':
			self.pitroster[userid].values['K'] += 1
		elif self.currentPlay.values['play_type'] == 'Walk':
			self.pitroster[userid].values['BB'] += 1
		elif self.currentPlay.values['play_type'] == 'Intentional Walk':
			self.pitroster[userid].values['IBB'] += 1
			self.pitroster[userid].values['BB'] += 1
		elif self.currentPlay.values['play_type'] == 'Hit By Pitch':
			self.pitroster[userid].values['HBP'] += 1
		elif self.currentPlay.values['hit'] is True:
			self.pitroster[userid].values['hits'] += 1

	def CalcIP(self, replacee, home_ind):
		#Figure out Innings Pitcher for Mound Exiter
		IP = float(self.currentSim.inning) - 1 + float(self.currentSim.outs / 3.0)
		for pit in self.pitroster.keys():
			if home_ind == 0 and self.pitroster[pit].values['team_key'] == self.currentGame.values['away_team_key']:
				IP -= self.pitroster[pit].values['IP']
			elif self.pitroster[pit].values['team_key'] == self.currentGame.values['home_team_key']:
				IP -= self.pitroster[pit].values['IP']
		self.pitroster[replacee].values['IP'] = IP

	def PitchSub(self, userid, replacee, home_ind, batnum):
		self.CalcIP(replacee, home_ind)
		#Put in the new pitcher
		if home_ind == 1:
			self.currentSim.activeHomePitcher = userid
			team = self.currentGame.values['home_team_key']
		else:
			self.currentSim.activeAwayPitcher = userid
			team = self.currentGame.values['away_team_key']
		if batnum > 0:
			row = 'sub,'+userid+',"",'+str(home_ind)+','+str(batnum)+',1'
			self.ScrapeLineupRow(row.split(','))
		self.pitroster[userid] = PitchBoxScore()
		self.pitroster[userid].values['team_key'] = team
		self.pitroster[userid].values['pitch_role'] = 'Reliever'


	def LogEndProcess(self):
		filePrefix = self.filename[-11:-4]
		NewHitters = {}
		NewPitchers = {}
		HitterLookup = Hitter().GetHitterRSLookup()
		PitcherLookup = Pitcher().GetPitcherRSLookup()
		print('Finding New Hitters')
		#Get New Hitters not yet in DB
		hcount = 0
		for l in self.gamelineups.keys():
			for h in self.gamelineups[l].keys():
				if h not in HitterLookup:
					hcount += 1
					NewHitters[h] = Hitter()
					NewHitters[h].values['rs_user_id'] = h
					NewHitters[h].GetInfofromRS()
					HitterLookup[h] = -1
		if hcount > 0:
			with open(filePrefix+'newhitters.csv', 'w', newline='', skipinitialspace=True) as out:
				writer = csv.DictWriter(out, fieldnames=NewHitters[h].fields.keys())
				writer.writeheader()
				for h in NewHitters.values():
					row = {}
					for field in h.fields.keys():
						if field == 'player_key':
							pass
						else:
							row[field] = h.values[field]
					writer.writerow(row)
			#Insert csv into DB
			HitterLookup = Hitter().GetHitterRSLookup()
		print('Finding New Pitchers')
		#Same but for Pitchers
		pcount = 0
		for r in self.gamepitroster.keys():
			for p in self.gamepitroster[r].keys():
				if p not in PitcherLookup:
					pcount += 1
					NewPitchers[p] = Pitcher()
					NewPitchers[p].values['rs_user_id'] = p
					NewPitchers[p].GetInfofromRS()
					PitcherLookup[p] = -1
		if pcount > 0:
			with open(filePrefix + 'newpitchers.csv', 'w', newline='', skipinitialspace=True) as out:
				writer = csv.DictWriter(out, fieldnames=NewPitchers[p].fields.keys())
				writer.writeheader()
				for p in NewPitchers.values():
					row = {}
					for field in p.fields.keys():
						if field == 'player_key':
							pass
						else:
							row[field] = p.values[field]
					writer.writerow(row)
			# Insert csv into DB
			PitcherLookup = Pitcher().GetPitcherRSLookup()
		print('Getting Game Keys')
		# Get Game Key
		for r in self.gamepitroster.keys():
			for p in self.gamepitroster[r].keys():
				if p not in PitcherLookup:
					NewPitchers[p] = Pitcher()
					NewPitchers[p].values['rs_user_id'] = p
					NewPitchers[p].GetInfofromRS()
		with open(self.filename[-11:-4]+'games.csv', 'w', newline='', skipinitialspace=True) as out:
			writer = csv.DictWriter(out, fieldnames=self.currentGame.fields.keys())
			writer.writeheader()
			for g in self.games.values():
				row = {}
				for field in g.fields.keys():
					if field == 'game_key':
						pass
					else:
						row[field.strip('\n')] = g.values[field]
				writer.writerow(row)
			#Get Game Lookup
			GameLookup = Game().GetGameLookup()
		print('Filling in Keys')
		#Fill in missing keys
		#Game
		for gameid in self.games.keys():
			thisGame = GameLookup[gameid]
			self.games[gameid].values['game_key'] = thisGame
			self.gameplays[gameid].values['game_key'] = thisGame
			self.gameplays[gameid].values['hitter_key'] = HitterLookup[self.gameplays[gameid].values['hitter_key']]
			self.gameplays[gameid].values['pitcher_key'] = PitcherLookup[self.gameplays[gameid].values['pitcher_key']]
			self.gamebases[gameid].values['game_key'] = thisGame
			self.gamelineups[gameid].values['game_key'] = thisGame
			self.gamelineups[gameid].values['player_key'] = HitterLookup[self.gamelineups[gameid].values['player_key']]
			self.pitroster[gameid].values['game_key'] = thisGame
		#Play
		#Base
		#Lineup
		#PitchRoster


	def ScrapeInfoRow(self, row):
		x = row[1]
		if x == 'visteam':
			self.currentGame.values['away_team_key'] = int(self.teams[str(row[2].strip())])
			return True
		elif x == 'hometeam':
			self.currentGame.values['home_team_key'] = int(self.teams[str(row[2].strip())])
			return True
		elif x == 'date':
			datePieces = row[2].split('/')
			self.currentGame.values['game_date'] = date(int(datePieces[0]), int(datePieces[1]), int(datePieces[2]))
			return True
		elif x == 'starttime':
			self.currentGame.values['game_time'] = row[2].strip()
			return True
		elif x == 'winddir':
			self.currentGame.values['wind_dir'] = row[2].strip()
			return True
		elif x == 'windspeed':
			self.currentGame.values['wind_speed_mph'] = float(row[2].strip())
			return True
		elif x == 'temp':
			self.currentGame.values['game_temp_f'] = float(row[2].strip())
			return True
		elif x == 'fieldcond':
			self.currentGame.values['field_condition'] = row[2].strip()
			return True
		elif x == 'precip':
			self.currentGame.values['precipitation'] = row[2].strip()
			return True
		elif x == 'sky':
			self.currentGame.values['sky_cond'] = row[2].strip()
			return True
		elif x == 'timeofgame':
			self.currentGame.values['game_time_minutes'] = int(row[2].strip())
			return True
		elif x == 'umphome':
			self.currentGame.values['home_ump_id'] = row[2].strip()
			return True
		elif x == 'attendance':
			self.currentGame.values['attendance'] = int(row[2].strip())
			return True
		elif x == 'wp':
			self.wp = row[2].strip()
			return True
		elif x == 'lp':
			self.lp = row[2].strip()
			return True
		elif x == 'save':
			self.savep = row[2].strip()
			return True
		else:
			return False


	def ScrapeLineupRow(self, row):
		userid = row[1]
		self.lineup[userid] = HitBoxScore()
		self.lineup[userid].values['player_key'] = userid
		if int(row[3]) == 0:
			self.lineup[userid].values['team_key'] = self.currentGame.values['away_team_key']
		else:
			self.lineup[userid].values['team_key'] = self.currentGame.values['home_team_key']
		self.lineup[userid].values['batting_num'] = int(row[4])
		self.lineup[userid].values['position'] = PosLookup[int(row[5])]
		return True


	def ScrapePlayRow(self, row):
		if self.currentSim.top_or_bot != int(row[2]):
			self.currentSim.top_or_bot = int(row[2])
			self.currentSim.outs = 0
		self.currentSim.inning = int(row[1])
		self.currentSim.batter = row[3]
		if row[6].strip('\n') != 'NP':
			self.play_seq += 1
			self.currentPlay = Play()
			self.currentBase = Base()
			self.currentBase.GetStartStateFromSim(self.currentSim)
			self.currentPlay.values['play_seq_no'] = self.play_seq
			self.currentBase.values['play_seq_no'] = self.play_seq
			self.currentPlay.values['hitter_key'] = str(row[3])
			self.currentPlay.values['top_bot_inn'] = int(row[2])
			if int(row[2]) == 0:
				self.currentPlay.values['pitcher_key'] = self.currentSim.activeHomePitcher
			else:
				self.currentPlay.values['pitcher_key'] = self.currentSim.activeAwayPitcher
			self.currentPlay.values['inning_num'] = int(row[1])
			self.currentPlay.values['balls'] = int(row[4][0])
			self.currentPlay.values['strikes'] = int(row[4][1])
			self.currentPlay.values['pitch_seq'] = str(row[5])
			self.currentPlay.values['play_seq'] = str(row[6].split('.')[0]).strip('\n')
			self.currentBase.values['run_seq'] = str(row[6].split('.')[1]) if len(row[6].split('.')) == 2 else ''
			self.currentPlay.values['play_type'] = self.GetPlayType()
			self.currentPlay.values['ball_type'] = self.GetBallType()

			#Use GameSim logic for other fields
			self.currentPlay.values['plate_app'], self.currentPlay.values['at_bat'], \
				self.currentPlay.values['hit'] = self.currentSim.ProcessRSPlayType(self.currentPlay.values['play_type'])
			self.currentBase.values['batter_scored'], self.currentBase.values['first_scored'], \
				self.currentBase.values['second_scored'], self.currentBase.values['third_scored'] = \
					self.currentSim.ProcessRSBase(self.currentBase.values['run_seq'], self.currentBase)
			self.currentBase.values['total_runs'], self.currentBase.values['rbi'] = \
				self.currentSim.GetRunsRBI(self.currentPlay.values['play_type'], self.currentBase)
			if self.currentBase.values['batter_scored']:
				self.lineup[self.currentSim.batter].values['runs'] += 1
			elif self.currentBase.values['first_scored']:
				self.lineup[self.currentBase.values['start_first']].values['runs'] += 1
			elif self.currentBase.values['second_scored']:
				self.lineup[self.currentBase.values['start_second']].values['runs'] += 1
			elif self.currentBase.values['third_scored']:
				self.lineup[self.currentBase.values['start_third']].values['runs'] += 1
			self.currentBase.GetEndStateFromSim(self.currentSim)
			if self.currentSim.top_or_bot == 0:
				self.currentGame.values['away_runs'] += int(self.currentBase.values['total_runs'])
			else:
				self.currentGame.values['home_runs'] += int(self.currentBase.values['total_runs'])
			self.CalcHitBox()
			self.CalcPitchBox()
			self.plays.append(self.currentPlay)
			self.bases.append(self.currentBase)
		return True


	def ParseLog(self):
		text = open(self.filename, 'a')
		text.write('\nid,dunzo')  # dummy row to find end of file
		text.close()
		text = open(self.filename, 'r')
		self.currentGame = None

		for line in text:
			line = line.replace('!', '')
			row = line.split(',')
			rowType = row[0]
			if rowType == 'info':
				self.ScrapeInfoRow(row)
			elif rowType == 'start':
				self.ScrapeLineupRow(row)
			elif rowType == 'play':
				if self.play_seq == 0:
					self.AddStarters()
				self.ScrapePlayRow(row)
			elif rowType == 'sub':
				if int(row[5]) == 1:
					if int(row[3]) == 0:
						self.PitchSub(row[1], self.currentSim.activeAwayPitcher, int(row[3]), int(row[4]))
					else:
						self.PitchSub(row[1], self.currentSim.activeHomePitcher, int(row[3]), int(row[4]))
				elif int(row[5]) == 12:
					self.ScrapeLineupRow(row)
					if self.currentSim.first_base != '' and  \
									self.lineup[self.currentSim.first_base].values['batting_num'] == int(row[4]):
						self.currentSim.first_base = row[1]
					elif self.currentSim.second_base != '' and \
									self.lineup[self.currentSim.second_base].values['batting_num'] == int(row[4]):
						self.currentSim.second_base = row[1]
					elif self.currentSim.third_base != '' and \
									self.lineup[self.currentSim.third_base].values['batting_num'] == int(row[4]):
						self.currentSim.third_base = row[1]
				else:
					self.ScrapeLineupRow(row)
			elif rowType == 'data':
				if row[1] == 'er':
					self.pitroster[row[2]].values['earned_runs'] += int(row[3])
			elif rowType == 'id':
				if self.currentGame is not None:  # short circuit the first row
					self.CalcIP(self.currentSim.activeAwayPitcher, 0)
					self.CalcIP(self.currentSim.activeHomePitcher, 1)
					self.ComputeEndGameStats()
					self.AddToGameDicts()
				if str(row[1]) != 'dunzo\n':
					self.ResetGame()
					self.currentGame.values['game_id'] = str(row[1]).strip('\n')
				else:
					# convert ids to keys
					print('Done Scraping')
					return self.LogEndProcess()