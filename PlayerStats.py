from datetime import date
from bbUtils import GetHitterKey

class Hitter:
    name = ''
    height = 0
    weight = 0
    birthdate = None
    mlbdebutdate = None
    bathand = 'R'
    userid = ''
    
    def __init__(self, ID, name):
        self.userid = ID
        self.name = name
    
    def InsertPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "HITTER_STATS" values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\', \'%s\', \'%s\')' % (self.name, self.bathand, self.userid)    
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            return True
        return False
        
    def CheckForRow(self, con):
        playerKey = GetHitterKey(self.userid, con)
        if playerKey == None:
            return False
        else:
            return True