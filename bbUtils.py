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
