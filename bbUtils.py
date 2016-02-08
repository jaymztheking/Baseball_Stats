def GetTeamKey(abb, con):
   cur = con.cursor()
   sql = 'select "TEAM_KEY" from "TEAM" where "TEAM_ABBREV" = \'%s\'' % abb
   cur.execute(sql)
   return cur.fetchall()[0][0]

def GetParkKey(hTeam, date, con):
    cur = con.cursor()
    sql = 'select "PARK_KEY" from "PARK" where "TEAM_KEY" = %s and "PARK_OPEN_DATE"<= \'%s\'' % (hTeam, date)
    cur.execute(sql)
    return cur.fetchall()[0][0]
    
def GetParkTZ(park, con):
    cur = con.cursor()
    sql = 'select "TIME_ZONE" from "PARK" where "PARK_KEY" = %s' % park
    cur.execute(sql)
    output = cur.fetchall()
    if len(output) == 1:
        return output[0][0]
    else:
        return ''
        
def GetGameKey(hteam, ateam, date, time, con):
    cur = con.cursor()        
    checkSQL = 'select "GAME_KEY" from "GAME" where "HOME_TEAM_KEY" = %s and "AWAY_TEAM_KEY" = %s and "GAME_DATE" = \'%s\' and "GAME_TIME" = \'%s\'' % \
    (hteam, ateam, date.strftime('%Y-%m-%d'), time)
    cur.execute(checkSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None
    
def GetHitterKey(name, con):
    cur = con.cursor()
    getSQL = 'select "PLAYER_KEY" from "HITTER_STATS" where "USER_ID" = \'%s\'' % name
    cur.execute(getSQL)
    results = cur.fetchall()
    if len(results) == 1:
        return results[0][0]
    else:
        return None
        
