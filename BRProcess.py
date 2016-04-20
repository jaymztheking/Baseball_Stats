from datetime import date
from bbUtils import GetTeamfromAbb
from BRParser import GameTeamsParser

def ProcessBRPage(filename, con):
    currentGame = None
    dateStr = filename.split('_')[-1]
    gameDate = date(int(dateStr[:4]),int(dateStr[4:6]),int(dateStr[6:8]))
    html = open(filename).read().decode('utf-8').replace('&#183;','*')
    b = GameTeamsParser()
    b.feed(html)
    return b
    