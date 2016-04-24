from datetime import date
from bbUtils import GetTeamfromAbb, ConvertTeamAbb
from BRParser import GameTeamsParser, GameTimeParser, GameWeatherParser, GameUmpParser
from GameStats import Game
import re

def ProcessBRPage(filename, con):
    dateStr = filename.split('_')[-1]
    gameDate = date(int(dateStr[:4]),int(dateStr[4:6]),int(dateStr[6:8]))
    html = open(filename).read().decode('utf-8').replace('&#183;','*')
    
    #Game Stuff
    b = GameTeamsParser()
    b.feed(html)
    homeTeamAbb = ConvertTeamAbb('BR',b.homeTeamAbb)
    awayTeamAbb = ConvertTeamAbb('BR',b.awayTeamAbb)
    hTeam = GetTeamfromAbb(homeTeamAbb, con)
    aTeam = GetTeamfromAbb(awayTeamAbb, con)
    currentGame = Game(hTeam, aTeam, gameDate, con)
    b = GameTimeParser()
    b.feed(html)
    currentGame.time = b.time
    lengthStr = b.gamelen.split(':')
    currentGame.gameLength += int(lengthStr[0]) * 60 + int(lengthStr[1])
    b = GameWeatherParser()
    b.feed(html)
    print b.weather
    currentGame.temp = int(re.search(': -?([0-9]{2}) F', b.weather).group(1))
    currentGame.windSpeed = int(re.search('Wind ([0-9]{1,2})mph', b.weather, flags=re.IGNORECASE).group(1))
    windDir = re.search('mph ([^,]*),', b.weather, flags=re.IGNORECASE).group(1)
    if windDir == 'out to Centerfield':
        windDir = 'tocf'
    elif windDir == 'out to Rightfield':
        windDir = 'torf'
    elif windDir == 'out to Leftfield':
        windDir = 'tolf'
    elif windDir == 'from Left to Right':
        windDir = 'ltor'
    elif windDir == 'from Right to Left':
        windDir = 'rtol'
    elif windDir == 'in from Centerfield':
        windDir = 'fromcf'
    elif windDir == 'in from Rightfield':
        windDir = 'fromrf'
    elif windDir == 'in from Leftfield':
        windDir = 'fromlf'
    weatherStr = b.weather.split(',')
    if len(weatherStr) < 4:
        precip = 'unknown'
        sky = weatherStr[-1].replace('.','').lower()
    else:
        precip = weatherStr[-1].replace('.','').lower()
        sky = weatherStr[-2].lower()
    field = b.field.lower() if (b.field != '') else 'unknown'
    currentGame.weather = 'Field = '+field+', Prec = '+precip+', Sky = '+sky
    b = GameUmpParser()
    b.feed(html)
    currentGame.homeUmp = str(b.homeump)
    
    
    return currentGame
    
    
    