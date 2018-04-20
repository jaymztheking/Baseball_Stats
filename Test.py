from Retro import RSLog
from GameSim import GameSim
import re
import pandas as pd


teamfile = RSLog('.\\Play by Play Logs\\2017\\2017CHN.EVN')
results = teamfile.scrape()

# # Run Totals By Game
# dic = {}
# games = []
# sbs= []
# for game in results['games']:
# 	print(game)
# 	linesb = 0
# 	for hitter in results['lineups'][game]:
# 		line = results['lineups'][game][hitter]
# 		if line.team_key == 13:
# 			linesb += line.sb
# 	sbs.append(linesb)
# 	games.append(game)
# dic= {'game': games, 'sb': sbs}
# df = pd.DataFrame(data=dic)
# print(games)
# df.to_csv('anasb2017.csv')


#Lines for Game
for hitter in results['lineups']['CHN201708010']:
	line = results['lineups']['CHN201708010'][hitter]
	print(hitter, line.plate_app, line.at_bat)
#
# #Inning Plays
# for play in results['plays']['ANA201705070']:
# 	base = results['bases']['ANA201705070'][play.play_seq_no-1]
# 	if int(play.inning_num) == 2 and int(play.top_bot_inn) == 1:
# 		print(vars(play))
# 		print(vars(base))
# 		print('')