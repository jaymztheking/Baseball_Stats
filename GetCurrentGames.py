import urllib2, datetime
from BRParser import GamesParser

savePath = '.\\Game HTML Saves\\'

'''
year = str(input('What year?'))
month = str(input('What month?'))
day = str(input('What day?'))
url = 'http://www.baseball-reference.com/games/standings.cgi?month=%s&day=%s&year=%s' % (month.zfill(2), day, year)
'''

startDate = datetime.date(2016,5,6)
endDate = datetime.date(2016,5,7) #datetime.date.today()
oneDay = datetime.timedelta(1)

while startDate < endDate:

    year = str(startDate.year)
    month = str(startDate.month)
    day = str(startDate.day)

    url = 'http://www.baseball-reference.com/games/standings.cgi?month=%s&day=%s&year=%s' % (month.zfill(2), day, year)

    html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
    listOfGames = []
    b= GamesParser()
    b.feed(html)
    for game in b.games:
        gameNum = 1
        if game[1]+game[0] in listOfGames:
            gameNum += 1
        fileName = savePath + '%s_@_%s_%s_%s' % (game[1], game[0], gameNum, year+month.zfill(2)+day.zfill(2))+'.html'
        listOfGames.append(game[1]+game[0])
        gameHTML = urllib2.urlopen(game[2]).read()
        newFile = open(fileName, 'w')
        newFile.write(gameHTML)
        newFile.close()

    startDate = startDate + oneDay