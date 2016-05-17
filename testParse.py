
from BRParser import  BRPlayerInfoParser
import urllib2

b =  BRPlayerInfoParser()
url = "http://www.baseball-reference.com/players/p/puigya01.shtml"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
print b.birthDate
