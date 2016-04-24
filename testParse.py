from BRPlayParser import BRPlayParser
from BRParser import GameUmpParser
import urllib2

b = GameUmpParser()
url = "http://www.baseball-reference.com/boxes/HOU/HOU201604170.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html.replace('&nbsp;',' '))
print b.homeump