from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd


teamfile = RSLog('.\\Play by Play Logs\\2017\\2017ANA.EVA')
results = teamfile.scrape()

# Run Totals By Game
playruntotal = 0
lineruntotal = 0
for game in results['games']:
	playruns = 0
	lineruns = 0
	for play in results['plays'][game]:
		base = results['bases'][game][play.play_seq_no-1]
		if int(base.top_bot_inn) == 1:
			playruns += base.total_runs
	for hitter in results['lineups'][game]:
		line = results['lineups'][game][hitter]
		if line.team_key == 13:
			lineruns += line.runs
	print(game, playruns, lineruns)
	playruntotal += playruns
	lineruntotal += lineruns
print(playruntotal, lineruntotal)

# #Lines for Game
# for hitter in results['lineups']['ANA201705160']:
# 	line = results['lineups']['ANA201705160'][hitter]
# 	if int(line.team_key) == 13:
# 		print(hitter, line.at_bat, line.runs)

#Inning Plays
# for play in results['plays']['ANA201705160']:
# 	base = results['bases']['ANA201705160'][play.play_seq_no-1]
# 	if int(play.inning_num) == 7 and int(play.top_bot_inn) == 1:
# 		print(play.play_seq_no, play.hitter_key, play.play_type)
# 		print(base.run_seq, 's1', base.start_first, 's2', base.start_second, 's3', base.start_third, 'e1', base.end_first, 'e2', base.end_second, 'e3', base.end_third)





