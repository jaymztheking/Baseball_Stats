from Baseball import PosLookup, Game, HitBoxScore, PitchBoxScore, Play, Base
from GameSim import GameSim
import json, re
from datetime import date


class RSLog:
	def __init__(self, file):
		self.filename = file
		self.hitters = {}
		self.pitchers = {}
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
				self.pitroster[userid].values['game_key'] = self.lineup[userid].values['game_key']
				self.pitroster[userid].values['team_key'] = self.lineup[userid].values['team_key']
				if self.pitroster[userid].values['team_key'] == self.currentGame.values['home_team_key']:
					self.currentSim.activeHomePitcher = userid
				else:
					self.currentSim.activeAwayPitcher = userid
				self.pitroster[userid].values['player_key'] = self.lineup[userid].values['player_key']
				self.pitroster[userid].values['pitch_role'] = 'Starter'

	def ComputeEndGameStats(self):
		#Need Game Stuff and Box Scores
		pass

	def GetPlayType(self):
		playseq = self.currentPlay.values['play_seq']
		runseq = self.currentBase.values['run_seq']

		# Stolen Base
		if re.search('SB[23H]', playseq) != None:
			if 'SB2' in playseq:
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
			return 'Stolen Base'

		# Caught Stealing
		if re.search('CS[23H]', playseq) != None:
			if 'CS2' in playseq:
				self.currentBase.values['second_caught'] = True
				if 'E' not in playseq:
					runseq += ';1X2'
				elif '1-' not in runseq:
					runseq += ';1-2'
			if 'CS3' in playseq:
				self.currentBase.values['third_caught'] = True
				if 'E' not in playseq:
					runseq += ';2X3'
				elif '2-' not in runseq:
					runseq += ';2-3'
			if 'CSH' in playseq:
				self.currentBase.values['home_caught'] = True
				if 'E' not in playseq:
					runseq += ';3XH'
				elif '3-' not in runseq:
					runseq += ';3-H'
			return 'Caught Stealing'

		#Pick Off
		if re.search('PO[^C]', playseq) != None:
			if 'E' not in runseq:
				self.currentSim.outs += 1
				if 'PO1' in runseq:
					self.currentSim.first_base = ''
				if 'PO2' in runseq:
					self.currentSim.second_base = ''
				if 'PO3' in runseq:
					self.currentSim.third_base = ''
			return 'Pick Off'

		#Balk
		if re.search('BK', playseq) != None:
			return 'Balk'

		#Passed Ball
		if re.search('PB', playseq) != None:
			return 'Passed Ball'

		#Wild Pitch
		if re.search('WP', playseq) != None:
			return 'Wild Pitch'

		#Defensive Indifference
		if re.search('DI', playseq) != None:
			return 'Defensive Indifference'

		#Error on Foul
		if re.search('FLE', playseq) != None:
			return 'Error on Foul'

		#Misc
		if re.search('OA', playseq) != None:
			return 'Unknown Runner Activity'

		#Interference
		if re.search('C$', playseq) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			return 'Interference'

		#Walks
		if re.search('W(\+|$)', playseq) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			return 'Intentional Walk' if 'IW' in playseq else 'Walk'

		#HBP
		if re.search('W(\+|$)', playseq) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			return 'Hit By Pitch'

		#Sac Fly
		if 'SF' in playseq:
			return 'Sacrifice Fly'

		#Sac Hit
		if 'SH' in playseq:
			return 'Sacrifice Hit'

		#Strikeout
		if re.search('(^|[^B])K', playseq) != None:
			if 'B-' not in runseq:
				self.currentSim.outs += 1
			return 'Strikeout'

		#one Fielding Out
		if re.search('^[0-9]+$', playseq) != None:
			self.currentPlay.values['ball_loc'] = playseq[0]
			self.currentSim.outs += 1
			return 'Out'


	def LogEndProcess(self):
		for x in self.gamelineups.values():
			print(x)
		pass

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
		userid = row[1]+'|'+self.currentGame.values['game_id']
		self.lineup[userid] = HitBoxScore()
		if row[3] == 0:
			self.lineup[userid].values['team_key'] = self.currentGame.values['away_team_key']
		else:
			self.lineup[userid].values['team_key'] = self.currentGame.values['home_team_key']
		self.lineup[userid] = HitBoxScore()
		self.lineup[userid].values['batting_num'] = int(row[4])
		self.lineup[userid].values['position'] = PosLookup[int(row[5])]
		return True

	def ScrapePlayRow(self, row):
		self.currentSim.top_or_bot = int(row[2])
		self.currentSim.inning = int(row[1])
		self.currentSim.batter = row[3]
		if row[6] not in ('NP',):
			self.currentPlay = Play()
			self.currentBase = Base()
			self.currentBase.GetStartStateFromSim(self.currentSim)
			self.currentPlay.values['hitter_key'] = str(row[3])
			self.currentPlay.values['balls'] = int(row[4][0])
			self.currentPlay.values['strikes'] = int(row[4][1])
			self.currentPlay.values['pitch_seq'] = str(row[5])
			self.currentPlay.values['play_seq'] = str(row[6].split('.')[0])
			self.currentBase.values['run_seq']= str(row[6].split('.')[1]) if len(row[6].split('.')) == 2 else ''
			self.currentPlay.values['play_type'] = self.GetPlayType()
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
				self.play_seq += 1
				self.ScrapePlayRow(row)
			elif rowType == 'sub':
				if int(row[5]) == 1:
					pass  # Sub Pitcher
				elif int(row[5]) == 11:
					pass  # Sub Hitter
				elif int(row[5]) == 12:
					pass  # Sub Runner
				else:
					pass  # Sub Defender
			elif rowType == 'data':
				pass  # do something to add earned runs
			elif rowType == 'id':
				if self.currentGame is not None: #short circuit the first row
					self.ComputeEndGameStats()
					self.AddToGameDicts()
				if str(row[1]) == 'dunzo':
					#convert ids to keys
					self.LogEndProcess()
				else:
					self.ResetGame()
					self.currentGame.values['game_id'] = str(row[1]).strip('\n')
		return True