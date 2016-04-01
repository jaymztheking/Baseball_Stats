from RSParser import PlayerInfoParser
import urllib2

b = PlayerInfoParser()
url = "http://www.retrosheet.org/boxesetc/G/Pgomec002.htm"
html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
b.feed(html)
