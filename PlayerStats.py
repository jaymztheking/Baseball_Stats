from RSParser import PlayerInfoParser as RSInfoParser
from BRParser import BRPlayerInfoParser as BRInfoParser
from datetime import datetime
import urllib2
import re


class Hitter:
    name = ''
    height = 0
    weight = 0
    birthDate = None
    mlbDebutDate = None
    batHand = 'R'
    rsuserid = ''
    bruserid = ''
    fields = {'name': 'NAME', 'height': 'HEIGHT_INCH', 'weight': 'WEIGHT_LBS',
              'birthDate': 'BIRTH_DATE', 'mlbDebutDate': 'MLB_DEBUT_DATE',
              'batHand': 'BAT_HAND', 'rsuserid': 'RS_USER_ID',
              'bruserid': 'BR_USER_ID'}

    def __init__(self, src, ID, name):
        if src == 'BR':
            self.bruserid = ID
        elif src == 'RS':
            self.rsuserid = ID
        self.name = name

    def InsertRSPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "HITTER_STATS" values(default, \'%s\', 0, 0, ' \
                    '\'1900-01-01\', \'1900-01-01\', \'%s\', \'%s\', \'\')' \
                    % (self.name.replace("\'", "`").replace('"', ''), self.batHand,
                       self.rsuserid)
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.GetInfofromRS(con)
            return True
        return False

    def InsertBRPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "HITTER_STATS" values(default, \'%s\', 0, 0, ' \
                    '\'1900-01-01\', \'1900-01-01\', \'%s\', \'\', \'%s\')' \
                    % (self.name.replace("\'", "`").replace('"', ''), self.batHand,
                       self.bruserid)
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.GetInfofromBR(con)
            return True
        return False

    def InsertPlayerRow(self, con):
        if self.rsuserid != '':
            self.InsertRSPlayerRow(con)
            return True
        elif self.bruserid != '':
            self.InsertBRPlayerRow(con)
            return True
        else:
            return False

    def CheckForRow(self, con):
        playerKey = self.GetHitterKey(con)
        if playerKey < 0:
            return False
        else:
            return True


    def GetHitterKey(self, con):
        cur = con.cursor()
        if self.rsuserid != '':
            sql = 'select "PLAYER_KEY" from "HITTER_STATS" ' \
                  'where "RS_USER_ID" = \'%s\'' % self.rsuserid
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 1:
                return int(results[0][0])
            else:
                return -1
        elif self.bruserid != '':
            sql = 'select "PLAYER_KEY" from "HITTER_STATS" ' \
                  'where "BR_USER_ID" = \'%s\'' % self.bruserid
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 1:
                return int(results[0][0])
            else:
                return -1
        else:
            return -1

    def GetInfofromRS(self, con):
        b = RSInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.rsuserid[0].upper(), self.rsuserid)
        html = urllib2.urlopen(url).read().encode('utf-8').replace('&#183;', '*')
        b.feed(html)
        cur = con.cursor()
        key = self.GetHitterKey(con)
        if key > 0:
            sql = 'UPDATE "HITTER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, ' \
                  '"BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "BAT_HAND"=\'%s\' ' \
                  'WHERE "PLAYER_KEY" = %s' % \
                  (b.height, b.weight, b.birthDate.strftime('%Y-%m-%d'),
                   b.debutDate.strftime('%Y-%m-%d'), b.batHand, key)
            cur.execute(sql)
            cur.execute('COMMIT;')
            return True
        else:
            return False

    def GetInfofromBR(self, con):
        b = BRInfoParser()
        if self.bruserid == '':
            return False
        url = 'http://baseball-reference.com/players/%s/%s.shtml' % (self.bruserid[0], self.bruserid)
        html = urllib2.urlopen(url).read()
        html = html.decode('utf-8')
        b.feed(html)
        cur = con.cursor()
        key = self.GetHitterKey(con)
        weight = float(re.search('([0-9]*) lb', b.weight).group(1)) if re.search('([0-9]*) lb', b.weight) is not None else 0
        hFeet = re.search('([0-9])\'', b.height).group(1) if re.search('([0-9])\'', b.height) is not None else 0
        hInch = re.search('([0-9]*)"', b.height).group(1) if re.search('([0-9])"', b.height) is not None else 0
        height = float(hFeet) *12 + float(hInch)
        bDay = datetime.strptime(b.birthDate, '%B %d,%Y')
        dDay = datetime.strptime(b.mlbDebutDate, '%B %d, %Y')
        if key > 0:
            sql = 'UPDATE "HITTER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, ' \
                  '"BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "BAT_HAND"=\'%s\' ' \
                  'WHERE "PLAYER_KEY" = %s' % \
                  (height, weight, bDay.strftime('%Y-%m-%d'),
                   dDay.strftime('%Y-%m-%d'), str(b.batHand.strip()[0]), key)
            cur.execute(sql)
            cur.execute('COMMIT;')
            return True
        else:
            return False


class Pitcher:
    name = ''
    height = 0
    weight = 0
    birthDate = None
    mlbDebutDate = None
    throwHand = 'R'
    armRelease = 'Overhand'
    rsuserid = ''
    bruserid = ''

    def __init__(self, src, ID, name):
        if src == 'BR':
            self.bruserid = ID
        elif src == 'RS':
            self.rsuserid = ID
        self.name = name

    def InsertRSPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "PITCHER_STATS" values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\',' \
                    ' \'%s\', \'%s\', \'%s\', \'\')' % (
            self.name.replace("\'", "`").replace('"', ''), self.throwHand, self.armRelease, self.rsuserid)
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.GetInfofromRS(con)
            return True
        return False

    def InsertBRPlayerRow(self, con):
        cur = con.cursor()
        insertSQL = 'insert into "PITCHER_STATS" values(default, \'%s\', 0, 0, \'1900-01-01\', \'1900-01-01\',' \
                    ' \'%s\', \'%s\', \'\', \'%s\')' % (
                        self.name.replace("\'", "`").replace('"', ''), self.throwHand, self.armRelease, self.bruserid)
        if not self.CheckForRow(con):
            cur.execute(insertSQL)
            cur.execute('COMMIT;')
            self.GetInfofromBR(con)
            return True
        return False

    def InsertPlayerRow(self, con):
        if self.rsuserid != '':
            self.InsertRSPlayerRow(con)
            return True
        elif self.bruserid != '':
            self.InsertBRPlayerRow(con)
            return True
        else:
            return False

    def CheckForRow(self, con):
        playerKey = self.GetPitcherKey(con)
        if playerKey > 0:
            return True
        else:
            return False

    def GetPitcherKey(self, con):
        cur = con.cursor()
        if self.rsuserid != '':
            sql = 'select "PLAYER_KEY" from "PITCHER_STATS" ' \
                  'where "RS_USER_ID" = \'%s\'' % self.rsuserid
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 1:
                return int(results[0][0])
            else:
                return -1
        elif self.bruserid != '':
            sql = 'select "PLAYER_KEY" from "PITCHER_STATS" ' \
                  'where "BR_USER_ID" = \'%s\'' % self.bruserid
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) == 1:
                return int(results[0][0])
            else:
                return -1
        else:
            return -1

    def GetInfofromRS(self, con):
        b = RSInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % (self.rsuserid[0].upper(), self.rsuserid)
        html = urllib2.urlopen(url).read().decode('utf-8')
        b.feed(html)
        cur = con.cursor()
        key = self.GetPitcherKey(con)
        sql = 'UPDATE "PITCHER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, "BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "THROW_HAND"=\'%s\' WHERE "PLAYER_KEY" = %s' % (
            b.height, b.weight, b.birthDate.strftime('%Y-%m-%d'), b.debutDate.strftime('%Y-%m-%d'), b.throwHand, key)
        cur.execute(sql)
        cur.execute('COMMIT;')

    def GetInfofromBR(self, con):
        b = BRInfoParser()
        if self.bruserid == '':
            return False
        url = 'http://baseball-reference.com/players/%s/%s.shtml' % (self.bruserid[0], self.bruserid)
        html = urllib2.urlopen(url).read().decode('utf-8').replace('&#183;', '*')
        b.feed(html)
        cur = con.cursor()
        key = self.GetPitcherKey(con)
        weight = float(re.search('([0-9]*) lb', b.weight).group(1)) if re.search('([0-9]*) lb',
                                                                                 b.weight) is not None else 0
        hFeet = re.search('([0-9])\'', b.height).group(1) if re.search('([0-9])\'', b.height) is not None else 0
        hInch = re.search('([0-9]*)"', b.height).group(1) if re.search('([0-9])"', b.height) is not None else 0
        height = float(hFeet) * 12 + float(hInch)
        bDay = datetime.strptime(b.birthDate, '%B %d,%Y')
        dDay = datetime.strptime(b.mlbDebutDate, '%B %d, %Y')
        if key > 0:
            sql = 'UPDATE "PITCHER_STATS" SET "HEIGHT_INCH" = %s, "WEIGHT_LBS" = %s, ' \
                  '"BIRTH_DATE"=\'%s\', "MLB_DEBUT_DATE"=\'%s\', "THROW_HAND"=\'%s\' ' \
                  'WHERE "PLAYER_KEY" = %s' % \
                  (height, weight, bDay.strftime('%Y-%m-%d'),
                   dDay.strftime('%Y-%m-%d'), str(b.throwHand.strip()[0]), key)
            cur.execute(sql)
            cur.execute('COMMIT;')
            return True
        else:
            return False
