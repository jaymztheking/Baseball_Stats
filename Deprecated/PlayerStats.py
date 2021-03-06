from RSParser import PlayerInfoParser as RSInfoParser
from BRParser import BRPlayerInfoParser as BRInfoParser
from datetime import datetime
import urllib.request
import re


class Hitter:
	name = ''
	height = 0
	weight = 0
	birthDate = None
	mlbDebutDate = None
	batHand = 'R'
	rsuserid = ''
	bruserid = ''
	table = 'hitter'

	fields = {'key': 'player_key',
			  'name': 'name',
			  'height': 'height_inch',
			  'weight': 'weight_lbs',
			  'birthDate': 'birth_date',
			  'mlbDebutDate': 'mlb_debut_date',
			  'batHand': 'bat_hand',
			  'rsuserid': 'rs_user_id',
			  'bruserid': 'br_user_id'}


	def __init__(self, src, ID, name):
		if src == 'BR':
			self.bruserid = ID
		elif src == 'RS':
			self.rsuserid = ID
		self.name = name


	def InsertRSPlayerRow(self, con):
		cur = con.cursor()
		insertSQL = 'insert into %s values(default, \'%s\', 0, 0, ' \
					'\'1900-01-01\', \'1900-01-01\', \'%s\', \'%s\', \'\')' \
					% (self.table, self.name.replace("\'", "`").replace('"', ''), self.batHand,
					   self.rsuserid)
		if not self.CheckForRow(con):
			cur.execute(insertSQL)
			cur.execute('COMMIT;')
			self.GetInfofromRS(con)
			return True
		return False


	def InsertBRPlayerRow(self, con):
		cur = con.cursor()
		insertSQL = 'insert into %s values(default, \'%s\', 0, 0, ' \
					'\'1900-01-01\', \'1900-01-01\', \'%s\', \'\', \'%s\')' \
					% (self.table, self.name.replace("\'", "`").replace('"', ''), self.batHand,
					   self.bruserid)
		if not self.CheckForRow(con):
			cur.execute(insertSQL)
			cur.execute('COMMIT;')
			self.GetInfofromBR(con)
			return True
		return False


	def InsertPlayerRow(self, con):
		if self.rsuserid != '':
			self.InsertRSPlayerRow(con)
			return True
		elif self.bruserid != '':
			self.InsertBRPlayerRow(con)
			return True
		else:
			return False


	def CheckForRow(self, con):
		playerKey = self.GetHitterKey(con)
		if playerKey < 0:
			return False
		else:
			return True


	def GetHitterKey(self, con):
		cur = con.cursor()
		if self.rsuserid != '':
			sql = 'select %s from %s ' \
				  'where %s = \'%s\'' % (self.fields['key'], self.table, self.fields['rsuserid'], self.rsuserid)
			cur.execute(sql)
			results = cur.fetchall()
			if len(results) == 1:
				return int(results[0][0])
			else:
				return -1
		elif self.bruserid != '':
			sql = 'select %s from %s ' \
				  'where %s = \'%s\'' % (self.fields['key'], self.table, self.fields['bruserid'], self.bruserid)
			cur.execute(sql)
			results = cur.fetchall()
			if len(results) == 1:
				return int(results[0][0])
			else:
				return -1
		else:
			return -1


	def GetInfofromRS(self, con):
		b = RSInfoParser()
		url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.rsuserid[0].upper(), self.rsuserid)
		try:
			html = urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8').replace('&#183;', '*')
		except:
			print('Cannot connect to RetroSheet')
			return False
		b.feed(html)
		cur = con.cursor()
		key = self.GetHitterKey(con)
		if key > 0:
			sql = 'UPDATE %s SET %s = %s, %s = %s, ' \
				  '%s = \'%s\', %s =\'%s\', %s =\'%s\' ' \
				  'WHERE %s = %s' % \
				  (self.table, self.fields['height'], b.height, self.fields['weight'], b.weight, self.fields['birthDate'],
				   b.birthDate.strftime('%Y-%m-%d'), self.fields['mlbDebutDate'], b.debutDate.strftime('%Y-%m-%d'),
				   self.fields['batHand'], b.batHand, self.fields['key'], key)
			cur.execute(sql)
			cur.execute('COMMIT;')
			return True
		else:
			return False


	def GetInfofromBR(self, con):
		b = BRInfoParser()
		if self.bruserid == '':
			return False
		url = 'http://baseball-reference.com/players/%s/%s.shtml' % (self.bruserid[0], self.bruserid)
		html = urllib.request.urlopen(urllib.request.Request(url)).read()
		html = html.decode('utf-8')
		b.feed(html)
		cur = con.cursor()
		key = self.GetHitterKey(con)
		weight = float(re.search('([0-9]*) lb', b.weight).group(1)) if re.search('([0-9]*) lb', b.weight) is not None else 0
		hFeet = re.search('([0-9])\'', b.height).group(1) if re.search('([0-9])\'', b.height) is not None else 0
		hInch = re.search('([0-9]*)"', b.height).group(1) if re.search('([0-9])"', b.height) is not None else 0
		height = float(hFeet) * 12 + float(hInch)
		bDay = datetime.strptime(b.birthDate, '%B %d,%Y')
		dDay = datetime.strptime(b.mlbDebutDate, '%B %d, %Y')
		if key > 0:
			sql = 'UPDATE %s SET %s = %s, %s = %s, ' \
				  '%s = \'%s\', %s =\'%s\', %s =\'%s\' ' \
				  'WHERE %s = %s' % \
				  (self.table, self.fields['height'], b.height, self.fields['weight'], b.weight, self.fields['birthDate'],
				   b.birthDate.strftime('%Y-%m-%d'), self.fields['mlbDebutDate'], b.debutDate.strftime('%Y-%m-%d'),
				   self.fields['batHand'], b.batHand, self.fields['key'], key)
			cur.execute(sql)
			cur.execute('COMMIT;')
			return True
		else:
			return False


class Pitcher:
	name = ''
	height = 0
	weight = 0
	birthDate = None
	mlbDebutDate = None
	throwHand = 'R'
	armRelease = 'Overhand'
	rsuserid = ''
	bruserid = ''
	table = 'pitcher'

	fields = {'key': 'player_key',
			  'name': 'name',
			  'height': 'height_inch',
			  'weight': 'weight_lbs',
			  'birthDate': 'birth_date',
			  'mlbDebutDate': 'mlb_debut_date',
			  'throwHand': 'throw_hand',
			  'rsuserid': 'rs_user_id',
			  'bruserid': 'br_user_id'}

	def __init__(self, src, ID, name):
		if src == 'BR':
			self.bruserid = ID
		elif src == 'RS':
			self.rsuserid = ID
		self.name = name

	def InsertRSPlayerRow(self, con):
		cur = con.cursor()
		insertSQL = 'insert into %s values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\',' \
					' \'%s\', \'%s\', \'%s\')' % (self.table,
														self.name.replace("\'", "`").replace('"', ''), self.throwHand, self.rsuserid, self.bruserid)
		if not self.CheckForRow(con):
			cur.execute(insertSQL)
			cur.execute('COMMIT;')
			self.GetInfofromRS(con)
			return True
		return False

	def InsertBRPlayerRow(self, con):
		cur = con.cursor()
		insertSQL = 'insert into %s values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\',' \
					' \'%s\', \'%s\', \'\', \'%s\')' % (self.table,
														self.name.replace("\'", "`").replace('"', ''), self.throwHand,
														self.armRelease, self.bruserid)
		if not self.CheckForRow(con):
			cur.execute(insertSQL)
			cur.execute('COMMIT;')
			self.GetInfofromBR(con)
			return True
		return False

	def InsertPlayerRow(self, con):
		if self.rsuserid != '':
			self.InsertRSPlayerRow(con)
			return True
		elif self.bruserid != '':
			self.InsertBRPlayerRow(con)
			return True
		else:
			return False

	def CheckForRow(self, con):
		playerKey = self.GetPitcherKey(con)
		if playerKey > 0:
			return True
		else:
			return False

	def GetPitcherKey(self, con):
		cur = con.cursor()
		if self.rsuserid != '':
			sql = 'select %s from %s ' \
				  'where %s = \'%s\'' % (self.fields['key'], self.table, self.fields['rsuserid'], self.rsuserid)
			cur.execute(sql)
			results = cur.fetchall()
			if len(results) == 1:
				return int(results[0][0])
			else:
				return -1
		elif self.bruserid != '':
			sql = 'select %s from %s ' \
				  'where %s = \'%s\'' % (self.fields['key'], self.table, self.fields['bruserid'], self.bruserid)
			cur.execute(sql)
			results = cur.fetchall()
			if len(results) == 1:
				return int(results[0][0])
			else:
				return -1
		else:
			return -1

	def GetInfofromRS(self, con):
		b = RSInfoParser()
		url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.rsuserid[0].upper(), self.rsuserid)
		try:
			html = html = urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8')
		except:
			print('Cannot connect to RetroSheet')
			return False

		b.feed(html)
		cur = con.cursor()
		key = self.GetPitcherKey(con)
		sql = 'UPDATE %s SET %s = %s, %s = %s, %s = \'%s\', %s =\'%s\', %s =\'%s\' WHERE %s = %s' % \
			  (self.table,
			   self.fields[
				   'height'],
			   b.height,
			   self.fields[
				   'weight'],
			   b.weight,
			   self.fields[
				   'birthDate'],
			   b.birthDate.strftime(
				   '%Y-%m-%d'),
			   self.fields[
				   'mlbDebutDate'],
			   b.debutDate.strftime(
				   '%Y-%m-%d'),
			   self.fields[
				   'throwHand'],
			   b.throwHand,
			   self.fields['key'],
			   key)
		cur.execute(sql)
		cur.execute('COMMIT;')

	def GetInfofromBR(self, con):
		b = BRInfoParser()
		if self.bruserid == '':
			return False
		url = 'http://baseball-reference.com/players/%s/%s.shtml' % (self.bruserid[0], self.bruserid)
		html = html = urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8').replace('&#183;', '*')
		b.feed(html)
		cur = con.cursor()
		key = self.GetPitcherKey(con)
		weight = float(re.search('([0-9]*) lb', b.weight).group(1)) if re.search('([0-9]*) lb',
																				 b.weight) is not None else 0
		hFeet = re.search('([0-9])\'', b.height).group(1) if re.search('([0-9])\'', b.height) is not None else 0
		hInch = re.search('([0-9]*)"', b.height).group(1) if re.search('([0-9])"', b.height) is not None else 0
		height = float(hFeet) * 12 + float(hInch)
		bDay = datetime.strptime(b.birthDate, '%B %d,%Y')
		dDay = datetime.strptime(b.mlbDebutDate, '%B %d, %Y')
		if key > 0:
			sql = 'UPDATE %s SET %s = %s, %s = %s, %s = \'%s\', %s =\'%s\', WHERE %s = %s' % \
			  (self.table,
			   self.fields[
				   'height'],
			   height,
			   self.fields[
				   'weight'],
			   weight,
			   self.fields[
				   'birthDate'],
			   bDay,
			   self.fields[
				   'mlbDebutDate'],
			   dDay,
			   self.fields['key'],
			   key)
			cur.execute(sql)
			cur.execute('COMMIT;')
			return True
		else:
			return False
