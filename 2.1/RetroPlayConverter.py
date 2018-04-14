import re


def get_rs_play(playseq):
		playtyp = playseq.split('/')[0]
		playname = ''

		# Stolen Base
		if re.search('SB[23H]', playtyp) != None:
			playname = 'Stolen Base'

		# Caught Stealing
		if re.search('CS[23H]', playtyp) != None:
			playname = 'Caught Stealing'

		# Pick Off
		if re.search('PO[^C]', playtyp) != None:
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
			playname = 'Interference'

		# Walks
		if re.search('W(\+|$)', playtyp) != None:
			playname = 'Intentional Walk' if 'IW' in playseq else 'Walk'

		# HBP
		if re.search('HP', playtyp) != None:
			playname = 'Hit By Pitch'

		# Sac Fly
		if 'SF' in playseq:
			playname = 'Sacrifice Fly'

		# Sac Hit
		if 'SH' in playseq:
			playname = 'Sacrifice Hit'

		# Strikeout
		if re.search('(^|[^B])K', playtyp) != None:
			playname = 'Strikeout'

		# one Fielding Out
		if re.search('^[0-9]+$', playtyp) != None and 'Sacrifice' not in playname:
			playname = 'Out'

		# Force and Tag Outs/Double Play/Triple Play
		if re.search('^[0-9]{1,4}\([B123]\)', playtyp) != None and 'Sacrifice' not in playname:
			for a in playseq.split('/'):
				if 'DP' in a and 'NDP' not in a:
					playname = 'Double Play'
				if 'TP' in a:
					playname = 'Triple Play'
			if playname not in ('Triple Play', 'Double Play'):
				playname = 'Out'

		# Fielders Choice
		if re.search('FC[0-9]', playtyp) != None  and 'Sacrifice' not in playname:
			playname = 'Fielders Choice'

		# Reach On Error
		if re.search('(^|[^\(])E[0-9]', playtyp) != None and re.search('FLE', playtyp) == None \
				and 'Sacrifice' not in playname:
			playname = 'Reach On Error'

		# Single
		if re.search('^S[0-9]?', playtyp) != None and re.search('SB[23H]', playtyp) == None:
			playname = 'Single'

		# Double
		if re.search('^D[0-9]?', playtyp) != None and re.search('DI', playtyp) == None:
			playname = 'Double'

		# Ground Rule Double
		if re.search('DGR', playtyp) != None:
			playname = 'Ground Rule Double'

		# Triple
		if re.search('^T[0-9]?', playtyp) != None:
			playname = 'Triple'

		# Home Run
		if re.search('HR', playtyp) != None:
			playname = 'Home Run'

		return playname

def get_rs_run_seq(runseq, playseq):
	#Stolen Base
	playtyp = playseq.split('/')[0]
	if re.search('SB[23H]', playtyp) != None:
		if runseq == '':
			base = re.search('SB([23H])').group(1)
			if base == '2':
				runseq += ';1*2'
			elif base == '3':
				runseq += ';2*3'
			elif base == 'H':
				runseq += ';3*H'
		else:
			runseq = runseq.replace('-', '*')


	return runseq