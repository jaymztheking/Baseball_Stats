from Retro import RSLog


x = RSLog('.\\Play by Play Logs\\2017\\2017ANX.EVA')
x.ParseLog()
for i in x.gamebases.keys():
	for j in x.gamebases[i]:
		print(j.values['total_runs'])
