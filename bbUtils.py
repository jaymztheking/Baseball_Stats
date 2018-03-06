from BRParser import BRRSUserIdParser
import urllib.request

def GetTeamfromAbb(abb, src, con):
   cur = con.cursor()
   if src == 'RS':
       srcabb = 'team_abbrev_rs'
   else:
       srcabb = 'team_abbrev_bs'
   sql = 'select team_key from team where %s = \'%s\'' % (srcabb, abb)
   cur.execute(sql)
   results = cur.fetchall()
   if len(results) == 1:
       return results [0][0]
   else:
       return None
       
def GetTeam(gameKey, teamInd, con):
    cur = con.cursor()
    if teamInd == 'A':
        team = 'away_team_key'
    else:
        team = 'home_team_key'
    sql = 'select %s from game where game_key = %s' % (team, gameKey)
    cur.execute(sql)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None

def GetParkKey(hTeam, date, con):
    cur = con.cursor()
    sql = 'select park_key from park where team_key = %s and park_open_date <= \'%s\' and (park_close_date is null or park_close_date >= \'%s\')' % (hTeam, date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'))
    cur.execute(sql)
    return cur.fetchall()[0][0]
        
def GetGameKey(hteam, ateam, date, time, con):
    cur = con.cursor()        
    checkSQL = 'select game_key from game where home_team_key = %s and away_team_key = %s and game_date = \'%s\' and game_time = \'%s\'' % \
    (hteam, ateam, date.strftime('%Y-%m-%d'), time)
    cur.execute(checkSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None
        
def GetGameKeys(hteam, ateam, date, con):
    cur = con.cursor()        
    output = []
    checkSQL = 'select game_key from game where home_team_key = %s and away_team_key = %s and game_date = \'%s\' order by game_time' % \
    (hteam, ateam, date.strftime('%Y-%m-%d'))
    cur.execute(checkSQL)
    results = cur.fetchall()
    for row in results:
        output.append(row[0])
    return output
    
def GetHitterKey(src, uid, con):
    cur = con.cursor()
    if src == 'BR':
        getSQL = 'select player_key from hitter where br_user_id = \'%s\'' % uid
    elif src == 'RS':
        getSQL = 'select player_key from hitter where rs_user_id = \'%s\'' % uid
    else:
        getSQL = 'select player_key from hitter where 1 <> 1'
    cur.execute(getSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None

def GetPitcherKey(src, uid, con):
    cur = con.cursor()
    if src == 'BR':
        getSQL = 'select player_key from pitcher where br_user_id = \'%s\'' % uid
    elif src == 'RS':
        getSQL = 'select player_key from pitcher where rs_user_id = \'%s\'' % uid
    else:
        getSQL = 'select player_key from pitcher where 1 <> 1'
    cur.execute(getSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None
        
def GetLineupPlayers(gamekey, con): #debug with gamekey 2
    cur = con.cursor()
    playerList = {}
    getSQL = 'select h."NAME", l."PLAYER_BAT_NUM" from "HITTER_STATS" h INNER JOIN "LINEUP" l on h."PLAYER_KEY" = l."PLAYER_KEY" where l."GAME_KEY" = %s' % gamekey   
    cur.execute(getSQL)    
    results = cur.fetchall()
    for row in results:
        playerList[row[0]] = row[1]
    return playerList

def GetHitterKeyfromLU(gameKey, team, batNum, con):
    cur = con.cursor()
    getSQL = 'select "PLAYER_KEY" from "LINEUP" where "GAME_KEY" = %s and "TEAM_KEY" = %s and "PLAYER_BAT_NUM" = %s and "PLAYER_POS" <> \'PH\'' % \
    (gameKey, team, batNum)
    cur.execute(getSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None
    
def ConvertTeamAbb(src, teamAbb):
    if src == 'RS':
        diffAbb = {}
        diffAbb['CHN'] = 'CHC'    
        diffAbb['CHA'] = 'CHW'
        diffAbb['ANA'] = 'LAA'
        diffAbb['KCA'] = 'KCR'
        diffAbb['TBA'] = 'TBR'
        diffAbb['NYA'] = 'NYY'
        diffAbb['SDN'] = 'SDP'
        diffAbb['NYN'] = 'NYM'
        diffAbb['WAS'] = 'WSN'
        diffAbb['SFN'] = 'SFG'
        diffAbb['LAN'] = 'LAD'
        diffAbb['SLN'] = 'STL'
        return diffAbb.get(teamAbb, teamAbb)
    elif src == 'BR':
        diffAbb = {}
        diffAbb['CHC'] = 'CHN'    
        diffAbb['CHW'] = 'CHA'
        diffAbb['LAA'] = 'ANA'
        diffAbb['KCR'] = 'KCA'
        diffAbb['TBR'] = 'TBA'
        diffAbb['NYY'] = 'NYA'
        diffAbb['SDP'] = 'SDN'
        diffAbb['NYM'] = 'NYN'
        diffAbb['WSN'] = 'WAS'
        diffAbb['SFG'] = 'SFN'
        diffAbb['LAD'] = 'LAN'
        diffAbb['STL'] = 'SLN'
        return diffAbb.get(teamAbb, teamAbb)
    else:
        return teamAbb

def GetPos(num):
    pos = ['P','C','1B','2B','3B','SS','LF','CF','RF','DH']
    return pos[int(num)-1]


def GetCrossSiteUserID(src, tgt, id, con):
    if src == 'BR' and tgt == 'RS':
        url = 'http://www.baseball-reference.com/players/%s/%s.shtml' % (id[0], id)
        print(url)
        b = BRRSUserIdParser()
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request).read()
        html = html.decode('utf-8')
        b.feed(html)
        return b.uid
    else:
        return 'xxx'

