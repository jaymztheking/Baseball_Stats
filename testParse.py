from BRParser import LineupParser
import urllib2

b = LineupParser()
url = "http://www.baseball-reference.com/boxes/COL/COL201506030.shtml"
#need AL validation test for DH's too
html = urllib2.urlopen(url).read().decode('utf-8')
b.feed(html)
