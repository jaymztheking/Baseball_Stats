
from BRParser import  BRPitcherParser
import urllib2

b =  BRPitcherParser()
url = "http://www.baseball-reference.com/boxes/DET/DET201504060.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
for x in b.roster:
    print x