from datetime import date, time
import psycopg2
import databaseconfig as cfg

class Record:
    def __init__(self):
        self.inserted = False
        self.values = {}
        for field in self.fields.keys():
            self.values[field] = None
        self.values['game_key'] = -1  # dummy code

    @staticmethod
    def Connect():
        con = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (cfg.dbname, cfg.user, cfg.host, cfg.pw))
        return con

    def CreateInsertSQL(self, table):
        col = ''
        val = ''

        for x in self.fields.keys():
            if self.values[x] is not None:
                col += str(x) + ', '
                if self.fields[x][1] == 'not null' and self.values[x] is None:
                    print('Table referential integrity violated, fill in null values')
                    return None
                elif self.fields[x][2] == 'primary key':
                    val += 'default, '
                elif self.fields[x][0] in (str, date, time):
                    val += '\'' + str(self.values[x]) + '\', '
                else:
                    val += str(self.values[x]) + ', '

        return 'insert into ' + table + ' (' + col[:-2] + ') values (' + val[:-2] + ')'

    @staticmethod
    def ExecuteQuery(sql):
        con = Record.Connect()
        cur = con.cursor()
        cur.execute(sql)
        try:
            cur.execute('commit;')
        except:
            con.close()
            return False
        con.close()
        return True

    @staticmethod
    def ReturnSingleQuery(sql):
        con = Record.Connect()
        cur = con.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        con.close()
        if len(results) == 1:
            return results[0][0]
        else:
            return None


class Game(Record):
    def __init__(self):
        self.fields = {}
        self.fields['game_key'] = (int, 'not null', 'primary key')
        self.fields['game_id'] = (str, 'not null', '')
        self.fields['game_date'] = (date, 'not null', '')
        self.fields['game_time'] = (time, 'not null', '')
        self.fields['home_team_key'] = (int, 'not null', 'foreign key')
        self.fields['away_team_key'] = (int, 'not null', 'foreign key')
        self.fields['park_key'] = (int, 'not null', 'foreign key')
        self.fields['game_temp_f'] = (float, 'null', '')
        self.fields['wind_dir'] = (str, 'not null', '')
        self.fields['wind_speed_mph'] = (float, 'null', '')
        self.fields['field_condition'] = (str, 'null', '')
        self.fields['precipitation'] = (str, 'null', '')
        self.fields['sky_cond'] = (str, 'null', '')
        self.fields['total_innings'] = (int, 'null', '')
        self.fields['home_hits'] = (int, 'null', '')
        self.fields['away_hits'] = (int, 'null', '')
        self.fields['home_runs'] = (int, 'null', '')
        self.fields['away_runs'] = (int, 'null', ''),
        self.fields['home_team_win'] = (bool, 'null', '')
        self.fields['tie'] = (bool, 'null', '')
        self.fields['game_time_minutes'] = (int, 'null', '')
        self.fields['home_ump_id'] = (str, 'null', '')
        self.fields['attendance'] = (int, 'null', '')
        super(Game, self).__init__()

    def DBInsert(self):
        sql = super(Game, self).CreateInsertSQL('game')
        if super(Game, self).ExecuteQuery(sql) is not None:
            self.inserted = True
            self.values['game_key'] = super(Game, self).ReturnSingleQuery('select currval(\'game_game_key_seq\')')
            return True
        else:
            return False

    def GetGameKey(self):
        if self.inserted is True or self.values['game_key'] > 0:
            return self.values['game_key']
        elif self.values['game_id'] is not None:
            sql = 'select game_key from game where game_id = ' + self.values['game_id']
            return self.ReturnSingleQuery(sql)
        else:
            return None


class HitBoxScore(Record):
    def __init__(self):
        pass


class PitchBoxScore(Record):
    def __init__(self):
        pass


class Hitter(Record):
    def __init__(self):
        pass


class Pitcher(Record):
    def __init__(self):
        pass


class Play(Record):
    def __init__(self):
        pass


class Team(Record):
    def __init__(self):
        pass


class Park(Record):
    def __init__(self):
        pass
