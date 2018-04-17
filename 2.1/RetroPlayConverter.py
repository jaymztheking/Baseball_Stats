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
	if 'SH' in playseq and 'CSH' not in playseq:
		playname = 'Sacrifice Hit'

	# Strikeout
	if re.search('(^|[^B])K', playtyp) != None:
		playname = 'Strikeout'

	# Force and Tag Outs/Double Play/Triple Play
	if re.search('^([0-9]|\([B123]\))+/', playtyp) != None and 'Sacrifice' not in playname:
		for a in playseq.split('/'):
			if 'GDP' in a:
				playname = 'Ground Double Play'
			elif 'DP' in a and 'NDP' not in a:
				playname = 'Double Play'
			elif 'GTP' in a:
				playname = 'Ground Triple Play'
			elif 'TP' in a:
				playname = 'Triple Play'
		if playname not in ('Triple Play', 'Double Play', 'Ground Double Play'):
			playname = 'Out'

	# Fielders Choice
	if re.search('FC[0-9]', playtyp) != None  and 'Sacrifice' not in playname:
		playname = 'Fielders Choice'

	# Reach On Error
	if re.search('^[0-9]?E[0-9]', playtyp) != None and 'Sacrifice' not in playname:
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

	if '+' in playtyp:
		playname = get_rs_play(playtyp.split('+')[0]) + ' + ' + get_rs_play(playtyp.split('+')[1])

	return playname

def get_rs_run_seq(runseq, playseq, playname, sim):
	#Stolen Base
	playtyp = playseq.split('/')[0]
	if re.search('SB[23H]', playtyp) != None:
		if runseq == '':
			if 'SB2' in playtyp and re.search('1[-X]', runseq) == None:
				runseq += ';1*2'
			if 'SB3' in playtyp and re.search('2[-X]', runseq) == None:
				runseq += ';2*3'
			if 'SBH' in playtyp and re.search('3[-X]', runseq) == None:
				runseq += ';3*H'
		else:
			runseq = runseq.replace('-', '*')

	#Caught Stealing
	if re.search('CS[23H]', playtyp) != None:
		base = re.search('CS([23H])', playtyp).group(1)
		if re.search('E[0-9]', playtyp) != None and runseq == '':
			if base == '2' and re.search('1[-X]', runseq) == None:
				runseq += ';1-2'
			elif base == '3' and re.search('2[-X]', runseq) == None:
				runseq += ';2-3'
			elif base == 'H' and re.search('3[-X]', runseq) == None:
				runseq += ';3-H'
		else:
			if base == '2' and re.search('1[-X]', runseq) == None:
				runseq += ';1#2'
			elif base == '3' and re.search('2[-X]', runseq) == None:
				runseq += ';2#3'
			elif base == 'H' and re.search('3[-X]', runseq) == None:
				runseq += ';3#H'

	#Pickoff
	if re.search('PO[^C]', playtyp) != None:
		base = re.search('PO([23H])', playtyp).group(1)
		if re.search('E[0-9]', playtyp) != None and runseq == '':
			if base == '1' and re.search('1[-X]', runseq) == None:
				runseq += ';1-2'
			elif base == '2' and re.search('2[-X]', runseq) == None:
				runseq += ';2-3'
			elif base == '3' and re.search('3[-X]', runseq) == None:
				runseq += ';3-H'
		else:
			if base == '1' and re.search('1[-X]', runseq) == None:
				runseq += ';1X1'
			elif base == '2' and re.search('2[-X]', runseq) == None:
				runseq += ';2X2'
			elif base == '3' and re.search('3[-X]', runseq) == None:
				runseq += ';3X3'

	#Outs at plate (Strikeouts and Sacrifice
	if 'Sacrifice' in playname or playname == 'Strikeout':
		if 'B' not in runseq:
			runseq += ';BX1'

	#1 Base Advancement: Walk, Interference, HBP, FC, ROE, Single
	if playname in ('Walk', 'intentional Walk', 'Interference', 'Hit By Pitch', 'Fielders Choice', 'Reach On Error',
					  'Single'):
		if 'B' not in runseq:
			runseq += ';B-1'

	#Composite Plays (e.g. Strikeout + Caught Stealing)
	elif re.search('^I?[WK]\+', playtyp) != None:
		if 'Walk' in playname:
			if 'B' not in runseq:
				runseq += ';B-1'
		else:
			if 'B' not in runseq:
				runseq += ';BX1'

	#2 Base Advancement: Double and GRD
	elif playname in ('Double', 'Ground Rule Double'):
		if 'B' not in runseq:
			runseq += ';B-2'

	#3 Base Advancement: Triple
	elif playname == 'Triple':
		if 'B' not in runseq:
			runseq += ';B-3'

	elif playname == 'Home Run':
		if 'B' not in runseq:
			runseq += ';B-H'
		if sim.first_base != '':
			runseq += ';1-H'
		if sim.second_base != '':
			runseq += ';2-H'
		if sim.third_base != '':
			runseq += ';3-H'

	#Figure out Double Play and Fielding out mess
	elif re.search('^([0-9]|\([B123]\))+/', playtyp):
		outstr = re.findall('\([B123]\)', playtyp)
		outcount = 0
		for o in outstr:
			outcount += 1
			if o == '(1)':
				runseq += ';1X2'
			elif o == '(2)':
				runseq += ';2X3'
			elif o == '(3)':
				runseq += ';3XH'
			elif o == '(B)':
				runseq += ';BX1'
		if 'Double Play' in playname and outcount == 2 and 'B' not in runseq:
			runseq += ';B-1'
		elif 'Double Play' in playname and 'B' not in runseq:
			runseq += ';BX1'
		elif playname == 'Out' and outcount == 1 and 'B' not in runseq:
			runseq += ';B-1'
		elif 'B' not in runseq:
			runseq += ';BX1'

	return runseq

def get_rs_ball_type(playseq):
	ballloc = ''
	balltype = ''
	for x in playseq.split('/')[1:]:
		if re.search('^[0-9]{1,2}$', x) != None:
			ballloc = x
		if re.search('^B?[LFGP][0-9]', x) != None:
			ballloc = re.search('^B?[LFGP]([0-9])', x).group(1)
		if re.search('L', x) != None:
			balltype = 'Line Drive'
		if re.search('F', x) != None:
			balltype = 'Fly Ball'
		if re.search('G', x) != None:
			balltype = 'Ground Ball'
		if re.search('P', x) != None and re.search('DP', x) == None:
			balltype = 'Pop Up'
		if re.search('BP', x) != None:
			balltype = 'Bunt Pop'
		if re.search('BL', x) != None:
			balltype = 'Bunt Line Drive'
		if re.search('BG', x) != None:
			balltype = 'Bunt Ground Ball'
		if re.search('-', x) != None and balltype != '':
			balltype = 'Weak '+balltype
		if re.search('\+', x) != None and balltype != '':
			balltype = 'Strong '+balltype
	if re.search('^[SDTE]?([0-9])', playseq) != None and ballloc == '':
		ballloc = re.search('^[SDTE]?([0-9])', playseq).group(1)
	elif re.search('^FC([0-9])', playseq) != None and ballloc == '':
		ballloc = re.search('^FC([0-9])', playseq).group(1)

	return (ballloc, balltype)