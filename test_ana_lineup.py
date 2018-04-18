from Retro import RSLog

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
for game in results['lineups'].keys():
	for player in results['lineups'][game]:
		x = results['lineups'][game][player]
		if int(x.team_key) == 13:
			pa += x.plate_app
			ab += x.at_bat
			r += x.runs
			h += x.hits
			x2b += x.double
			x3b += x.triple
			hr += x.hr
			rbi += x.rbi
			sb += x.sb
			cs += x.cs
print(pa, ab, r, h, x2b, x3b, hr, rbi, sb, cs)

