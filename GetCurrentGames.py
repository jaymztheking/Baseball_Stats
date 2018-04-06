import urllib.request, datetime, os
from BRParser import GamesParser

savePath = os.path.dirname(os.path.abspath(__file__))

'''
year = str(input('What year?'))
month = str(input('What month?'))
day = str(input('What day?'))
url = 'http://www.baseball-reference.com/games/standings.cgi?month=%s&day=%s&year=%s' % (month.zfill(2), day, year)
'''

startDate = datetime.date(2018,3,30)
endDate = datetime.date(2018,4,3)
oneDay = datetime.timedelta(1)

while startDate < endDate:
	year = str(startDate.year)
	month = str(startDate.month)
	day = str(startDate.day)

	url = 'http://www.baseball-reference.com/games/standings.cgi?month=%s&day=%s&year=%s' % (month.zfill(2), day, year)
	request = urllib.request.Request(url)
	html = urllib.request.urlopen(request).read().decode('utf-8').replace('&#183;','*')
	listOfGames = []
	b= GamesParser()
	b.feed(html)
	for game in b.games:
		fileName = os.path.join(savePath,'Game HTML Saves', game[game.rfind('/')+1:])
		url = 'http://www.baseball-reference.com'+game
		request = urllib.request.Request(url)
		gameHTML = str(urllib.request.urlopen(request).read())
		newFile = open(fileName, 'w')
		newFile.write(gameHTML)
		newFile.close()

	startDate = startDate + oneDay