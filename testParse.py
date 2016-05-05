
from BRParser import BRRSUserIdParser
import urllib2

b = BRRSUserIdParser()
url = "http://www.baseball-reference.com/players/a/arenano01.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
print(b.uid)
