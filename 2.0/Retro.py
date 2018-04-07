from Baseball import Game, HitBoxScore, PitchBoxScore
from GameSim import GameSim
import json
from datetime import date


class RSLog:
	def __init__(self, file):
		self.filename = file
		with open('TeamLookup.json', 'r') as out:
			self.teams = json.load(out)

	def ResetGame(self):
		self.currentGame = Game()
		self.currentSim = GameSim()
		self.plays = {}
		self.lineup = {}
		self.pitroster = {}
		self.wp = ''
		self.lp = ''
		self.savep = ''

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
		pass

	def ScrapePlayRow(self, row):
		pass

	def ParseLog(self, storageMethod):
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
				if self.currentGame is not None:
					pass  # save all the stuff
				self.ResetGame()
				self.currentGame.values['game_id'] = str(row[1])
