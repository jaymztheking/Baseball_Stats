from BRParser import BattingDataParser
import urllib2

b = BattingDataParser()
url = "http://www.baseball-reference.com/boxes/COL/COL201506030.shtml"
#need AL validation test for DH's too
url1 = "http://www.baseball-reference.com/boxes/DET/DET201504060.shtml"
url2 = "http://www.baseball-reference.com/boxes/MIN/MIN201507250.shtml"
html = urllib2.urlopen(url2).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
