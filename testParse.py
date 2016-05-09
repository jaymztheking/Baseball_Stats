
from BRParser import BRBatterParser
import urllib2

b = BRBatterParser()
url = "http://www.baseball-reference.com/boxes/COL/COL201604270.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)

for x in b.batID.keys():
    print 'Hey', x, b.batID[x]
