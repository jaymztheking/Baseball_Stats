from Retro import RSLog
import re

pa = 0
ab = 0
r = 0
h = 0
x2b = 0
x3b = 0
hr = 0
rbi = 0
sb = 0
cs = 0

teamfile = RSLog('.\\Play by Play Logs\\2017\\2017ANA.EVA')
results = teamfile.scrape()
for game in results['plays']:
	for play in results['plays'][game]:
		if results['bases'][game][play.play_seq_no-1].total_runs >= 1:


