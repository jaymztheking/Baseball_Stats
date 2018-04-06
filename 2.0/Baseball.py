from datetime import date, time

class Record:
	def __init__(self):
		self.inserted = False
		self.values = {}
		for field in self.fields.keys():
			self.values[field] = None
		self.values['game_key'] = -1 #dummy code

	def CreateInsertSQL(self, table):
		col = ''
		val = ''

		for x in self.fields.keys():
			if self.values[x] is not None:
				col += str(x) + ', '
				if self.fields[x][1] == 'not null' and self.values[x] is None:
					print('Table referential integrity violated, fill in null values')
					return None
				elif self.fields[x][2] == 'primary key':
					val += 'default, '
				elif self.fields[x][0] in (str,date,time):
					val += '\'' + str(self.values[x]) + '\', '
				else:
					val += str(self.values[x])+', '

		return 'insert into '+table+' ('+col[:-2]+') values ('+val[:-2]+')'

	def ExecuteQuery(self, sql, con):
		cur = con.cursor()
		cur.execute(sql)
		try:
			cur.execute('commit;')
		except:
			return False
		return True

	def ReturnSingleQuery(self, sql, con):
		cur = con.cursor()
		cur.execute(sql)
		results = cur.fetchall()
		if len(results) == 1:
			return results[0][0]
		else:
			return None

class Game(Record):
	def __init__(self):
		self.fields = {}
		self.fields['game_key'] = (int,'not null','primary key')
		self.fields['game_id'] = (str,'not null','')
		self.fields['game_date'] = (date,'not null','')
		self.fields['game_time'] = (time,'not null','')
		self.fields['home_team_key'] = (int,'not null','foreign key')
		self.fields['away_team_key'] =  (int, 'not null', 'foreign key')
		self.fields['park_key'] = (int, 'not null', 'foreign key')
		self.fields['game_temp_f'] = (float,'null','')
		self.fields['wind_dir'] = (str,'not null','')
		self.fields['wind_speed_mph'] = (float,'null','')
		self.fields['weather_condition'] = (str,'null','')
		self.fields['total_innings'] = (int,'null','')
		self.fields['home_hits'] = (int,'null','')
		self.fields['away_hits'] = (int,'null','')
		self.fields['home_runs'] = (int,'null','')
		self.fields['away_runs'] = (int,'null',''),
		self.fields['home_team_win'] = (bool,'null','')
		self.fields['tie'] = (bool,'null','')
		self.fields['game_time_seconds'] = (int,'null','')
		self.fields['home_ump_id'] = (str,'null','')
		super(Game, self).__init__()

	def DBInsert(self, con):
		sql = super(Game, self).CreateInsertSQL('game')
		if super(Game, self).ExecuteQuery(sql, con) is not None:
			self.inserted = True
			self.values['game_key'] = super(Game, self).ReturnSingleQuery('select currval(\'game_game_key_seq\')', con)
			return True
		else:
			return False

	def GetGameKey(self):
		if self.inserted = True or self.values['game_key'] > 0:
			return self.values['game_key']
		elif self.values['game_id'] is not None:
			sql = 'select game_key from game where game_id = '+self.values['game_id']
		else:
			print('Not enough data to pull game key')
			return None

		return super(Game, self).ReturnSingleQuery(sql, con)


'''
class HitBoxScore(Record):
	def __init__(self):

class PitchBoxScore(Record):
	def __init__(self):

class Hitter(Record):
	def __init__(self):

class Pitcher(Record):
	def __init__(self):

class Play(Record):
	def __init__(self):

class Team(Record):
	def __init__(self):

class Park(Record):
	def __init__(self):
'''