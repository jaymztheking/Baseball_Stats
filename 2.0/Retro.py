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
				+ self.currentBase.values['third_stolen'] + self.currentBase.values['home_stolen']
			playname =  'Stolen Base'

		# Caught Stealing
		if re.search('CS[23H]', playtyp) != None:
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
			self.currentBase.values['total_cs'] = self.currentBase.values['second_caught'] + \
				self.currentBase.values['third_caught'] + self.currentBase.values['home_caught']
			playname = 'Caught Stealing'

		#Pick Off
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

		#Balk
		if re.search('BK', playtyp) != None:
			playname = 'Balk'

		#Passed Ball
		if re.search('PB', playtyp) != None:
			playname = 'Passed Ball'

		#Wild Pitch
		if re.search('WP', playtyp) != None:
			playname = 'Wild Pitch'

		#Defensive Indifference
		if re.search('DI', playtyp) != None:
			playname = 'Defensive Indifference'

		#Error on Foul
		if re.search('FLE', playtyp) != None:
			playname = 'Error on Foul'

		#Misc
		if re.search('OA', playtyp) != None:
			playname = 'Unknown Runner Activity'

		#Interference
		if re.search('C$', playtyp) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			playname = 'Interference'

		#Walks
		if re.search('W(\+|$)', playtyp) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			playname = 'Intentional Walk' if 'IW' in playseq else 'Walk'

		#HBP
		if re.search('W(\+|$)', playtyp) != None:
			if 'B-' not in runseq:
				runseq += ';B-1'
			playname = 'Hit By Pitch'

		#Sac Fly
		if 'SF' in playseq:
			playname = 'Sacrifice Fly'

		#Sac Hit
		if 'SH' in playseq:
			playname = 'Sacrifice Hit'

		#Strikeout
		if re.search('(^|[^B])K', playtyp) != None:
			if 'B-' not in runseq:
				self.currentSim.outs += 1
			playname = 'Strikeout'

		#one Fielding Out
		if re.search('^[0-9]+$', playtyp) != None:
			self.currentPlay.values['ball_loc'] = playseq[0]
			self.currentSim.outs += 1
			playname = 'Out'

		#Force and Tag Outs/Double Play/Triple Play
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

		#Fielders Choice
		if re.search('FC[0-9]', playtyp) != None:
			playname = 'Fielders Choice'
			self.currentPlay.values['ball_loc'] = re.search('FC([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		#Reach On Error
		if re.search('(^|[^\(])E[0-9]', playtyp) != None and re.search('FLE', playtyp) == None:
			if playname[:9] != 'Sacrifice':
				playname = 'Reach On Error'
			if 'B-' not in self.currentBase.values['run_seq'] or 'BX' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		#Single
		if re.search('^S[0-9]?', playtyp) != None and re.search('SB[23H]', playtyp) == None:
			playname = 'Single'
			if re.search('^S([0-9])', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('S([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-1'

		#Double
		if re.search('^D[0-9]?', playtyp) != None and re.search('DI', playtyp) == None:
			playname = 'Double'
			if re.search('^D[0-9]', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('D([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-2'

		#Ground Rule Double
		if re.search('DGR', playtyp) != None:
			playname = 'Ground Rule Double'
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-2'

		#Triple
		if re.search('^T[0-9]?', playtyp) != None:
			playname = 'Triple'
			if re.search('^T[0-9]', playtyp) != None:
				self.currentPlay.values['ball_loc'] = re.search('T([0-9])', playtyp).group(1)
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-3'

		#Home Run
		if re.search('HR', playtyp) != None:
			playname = 'Home Run'
			if 'B' not in self.currentBase.values['run_seq']:
				self.currentBase.values['run_seq'] += ';B-H'

		return playname

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
			self.currentPlay.values['ball_type'] = self.GetBallType()
			self.currentBase = self.currentSim.ProcessRSBase(self.currentBase.values['run_seq'], self.currentBase)
			self.currentBase = self.currentSim.GetRunsRBI(self.currentPlay.values['play_type'], self.currentBase)
			self.currentBase.GetEndStateFromSim(self.currentSim)
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