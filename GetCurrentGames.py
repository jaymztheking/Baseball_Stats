import urllib2
from BRParser import GamesParser

savePath = '.\\Game HTML Saves\\'

year = str(input('What year?'))
month = str(input('What month?'))
day = str(input('What day?'))
url = 'http://www.baseball-reference.com/games/standings.cgi?month=%s&day=%s&year=%s' % (month.zfill(2), day, year)


html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b= GamesParser()
b.feed(html)
for game in b.games:
    fileName = savePath + '%s_@_%s_%s' % (game[1], game[0],year+month.zfill(2)+day.zfill(2))+'.html'
    gameHTML = urllib2.urlopen(game[2]).read().decode('utf-8')
    newFile = open(fileName, 'w')
    newFile.write(gameHTML)
    newFile.close()