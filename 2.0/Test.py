import json

with open('TeamLookup.json', 'r') as out:
	team = json.load(out)

print(type(team))