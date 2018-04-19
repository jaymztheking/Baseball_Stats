from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd


teamfile = RSLog('.\\Play by Play Logs\\2017\\2017ANA.EVA')
results = teamfile.scrape()

# Run Totals By Game
dic = {}
games = []
rbis = []
for game in results['games']:
	print(game)
	linerbis = 0
	for hitter in results['lineups'][game]:
		line = results['lineups'][game][hitter]
		if line.team_key == 13:
			linerbis += line.rbi
	rbis.append(linerbis)
	games.append(game)
dic= {'game': games, 'rbi': rbis}
df = pd.DataFrame(data=dic)
print(games)
df.to_csv('anarbi2017.csv')


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





