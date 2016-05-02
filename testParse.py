
from BRParser import PlayerInfoParser
import urllib2

b = PlayerInfoParser()
url = "http://www.baseball-reference.com/players/a/arenano01.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
print(vars(b))
print(b.throwHand)
