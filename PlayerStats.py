from bbUtils import GetHitterKey, GetPitcherKey
from RSParser import PlayerInfoParser
import urllib2


class Hitter:
    name = ''
    height = 0
    weight = 0
    birthDate = None
    mlbDebutDate = None
    batHand = 'R'
    userid = ''
    
    def __init__(self, ID, name):
        self.userid = ID
        self.name = name
    
    def InsertPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "HITTER_STATS" values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\', \'%s\', \'%s\')' % (self.name.replace("\'","`").replace('"',''), self.batHand, self.userid)    
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.UpdatePlayerInfo(con)
            return True
        return False
        
    def CheckForRow(self, con):
        playerKey = GetHitterKey(self.userid, con)
        if playerKey == None:
            return False
        else:
            return True
    
    def UpdatePlayerInfo(self, con):
        b = PlayerInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.userid[0].upper(), self.userid)
        html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
        b.feed(html)
        cur = con.cursor()
        key = GetHitterKey(self.userid, con)
        sql = 'UPDATE "HITTER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, "BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "BAT_HAND"=\'%s\' WHERE "PLAYER_KEY" = %s' % (b.height, b.weight, b.birthDate.strftime('%Y-%m-%d'), b.debutDate.strftime('%Y-%m-%d'), b.batHand, key)
        cur.execute(sql)        
        cur.execute('COMMIT;')
        
class Pitcher:
    name = ''
    height = 0
    weight = 0
    birthDate = None
    mlbDebutDate = None
    throwHand = 'R'
    armRelease = 'Overhand'
    userid = ''
    
    def __init__(self, ID, name):
        self.userid = ID
        self.name = name
        
    def InsertPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "PITCHER_STATS" values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\', \'%s\', \'%s\', \'%s\')' % (self.name.replace("\'","`").replace('"',''), self.throwHand, self.armRelease, self.userid)    
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.UpdatePlayerInfo(con)
            return True
        return False
        
    def CheckForRow(self, con):
        playerKey = GetPitcherKey(self.userid, con)
        if playerKey == None:
            return False
        else:
            return True
            
    def UpdatePlayerInfo(self, con):
        b = PlayerInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.userid[0].upper(), self.userid)
        html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;','*')
        b.feed(html)
        cur = con.cursor()
        key = GetPitcherKey(self.userid, con)
        sql = 'UPDATE "PITCHER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, "BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "THROW_HAND"=\'%s\' WHERE "PLAYER_KEY" = %s' % (b.height, b.weight, b.birthDate.strftime('%Y-%m-%d'), b.debutDate.strftime('%Y-%m-%d'), b.throwHand, key)
        cur.execute(sql)        
        cur.execute('COMMIT;')
        