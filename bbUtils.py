def GetTeamKey(abb, con):
   cur = con.cursor()
   sql = 'select "TEAM_KEY" from "TEAM" where "TEAM_ABBREV" = \'%s\'' % abb
   cur.execute(sql)
   return cur.fetchall()[0][0]

def GetParkKey(hTeam, date, con):
    #eventually we'll want to account for date park was open
    cur = con.cursor()
    sql = 'select "PARK_KEY" from "PARK" where "TEAM_KEY" = %s' % hTeam
    cur.execute(sql)
    return cur.fetchall()[0][0]
