from GameSim import GameSim
from Retro import InfoRow, SubRow, PlayRow
from datetime import date

rowcount = 0
file = '.\\Play by Play Logs\\2017AAA.EVN'
text = open(file, 'r')
for line in text:
	row = line.strip('\n').split(',')
	rowtype = row[0]
	rowcount += 1
	if rowtype == 'id':
		currentgame = row[1]
		x = GameSim(currentgame)
	elif rowtype == 'info':
		x.read_info_row_data(InfoRow(currentgame, row, rowcount))
	elif rowtype == 'start':
		x.add_lineup(SubRow(currentgame, row, rowcount))
	elif rowtype == 'play':
		x.read_play_row_data(PlayRow(currentgame, row, rowcount))
print(x.activehomepitcher, x.activeawaypitcher)