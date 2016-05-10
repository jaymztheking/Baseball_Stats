
from BRParser import BRPlayParser
import urllib2

b = BRPlayParser()
url = "http://www.baseball-reference.com/boxes/COL/COL201604270.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)

for x in b.plays.values():
    print x[-1]
