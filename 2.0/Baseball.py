from datetime import date, time
import psycopg2
import GameSim
import databaseconfig as cfg

PosLookup = ['X','P','C','1B','2B','3B','SS','LF','CF','RF','PH','PR']


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
        self.fields = {}
        self.fields['game_key'] = (int, 'not null', 'foreign key')
        self.fields['team_key'] = (int, 'not null', 'foreign key')
        self.fields['player_key'] = (int, 'not null', 'foreign key')
        self.fields['batting_num'] = (int, 'null', '')
        self.fields['position'] = (str, 'null', '')
        self.fields['plate_app'] = (int, 'null', '')
        self.fields['at_bat'] = (int, 'null', '')
        self.fields['hits'] = (int, 'null', '')
        self.fields['bb'] = (int, 'null', '')
        self.fields['ibb'] = (int, 'null', '')
        self.fields['hbp'] = (int, 'null', '')
        self.fields['runs'] = (int, 'null', '')
        self.fields['rbi'] = (int, 'null', '')
        self.fields['single'] = (int, 'null', '')
        self.fields['double'] = (int, 'null', '')
        self.fields['triple'] = (int, 'null', '')
        self.fields['hr'] = (int, 'null', '')
        self.fields['sb'] = (int, 'null', '')
        self.fields['cs'] = (int, 'null', '')
        super(HitBoxScore, self).__init__()

    def DBInsert(self):
        sql = super(HitBoxScore, self).CreateInsertSQL('hitboxscore')
        if super(HitBoxScore, self).ExecuteQuery(sql) is not None:
            self.inserted = True
            return True
        else:
            return False


class PitchBoxScore(Record):
    def __init__(self):
        self.fields = {}
        self.fields['game_key'] = (int, 'not null', 'foreign key')
        self.fields['team_key'] = (int, 'not null', 'foreign key')
        self.fields['player_key'] = (int, 'not null', 'foreign key')
        self.fields['pitch_role'] = (str, 'not null', '')
        self.fields['pitch_count'] = (int, 'null', '')
        self.fields['K'] = (int, 'null', '')
        self.fields['BB'] = (int, 'null', '')
        self.fields['IBB'] = (int, 'null', '')
        self.fields['HBP'] = (int, 'null', '')
        self.fields['hits'] = (int, 'null', '')
        self.fields['earned_runs'] = (int, 'null', '')
        self.fields['IP'] = (float, 'null', '')
        self.fields['strikes'] = (int, 'null', '')
        self.fields['balls'] = (int, 'null', '')
        self.fields['complete_game'] = (bool, 'null', '')
        self.fields['shut_out'] = (bool, 'null', '')
        self.fields['no_hitter'] = (bool, 'null', '')
        self.fields['win'] = (bool, 'null', '')
        self.fields['loss'] = (bool, 'null', '')
        self.fields['save'] = (bool, 'null', '')
        self.fields['swing_strikes'] = (int, 'null', '')
        self.fields['look_strikes'] = (int, 'null', '')
        self.fields['contact_strikes'] = (int, 'null', '')
        self.fields['flyballs'] = (int, 'null', '')
        self.fields['groundballs'] = (int, 'null', '')
        self.fields['line_drives'] = (int, 'null', '')
        super(PitchBoxScore, self).__init__()

class Hitter(Record):
    def __init__(self):
        pass


class Pitcher(Record):
    def __init__(self):
        pass


class Play(Record):
    def __init__(self):
        self.fields = {}
        self.fields['game_key'] = (int, 'not null', 'foreign key')
        self.fields['play_seq_no'] = (int, 'not null', '')
        self.fields['hitter_key'] = (int, 'not null', 'foreign key')
        self.fields['pitcher_key'] = (int, 'not null', 'foreign key')
        self.fields['top_bot_inn'] = (int, 'null', '')
        self.fields['inning_num'] = (int, 'null', '')
        self.fields['pitch_seq'] = (str, 'null', '')
        self.fields['play_seq'] = (str, 'null', '')
        self.fields['play_type'] = (str, 'null', '')
        self.fields['plate_app'] = (bool, 'null', '')
        self.fields['at_bat'] = (bool, 'null', '')
        self.fields['hit'] = (bool, 'null', '')
        self.fields['strikes'] = (int, 'null', '')
        self.fields['balls'] = (int, 'null', '')
        self.fields['contact_x'] = (int, 'null', '')
        self.fields['swing_x'] = (int, 'null', '')
        self.fields['look_x'] = (int, 'null', '')
        self.fields['ball_loc'] = (str, 'null', '')
        self.fields['ball_type'] = (str, 'null', '')
        super(Play, self).__init__()


class Base(Record):
    def __init__(self):
        self.fields = {}
        self.fields['game_key'] = (int, 'not null', 'foreign key')
        self.fields['play_seq_no'] = (int, 'not null', '')
        self.fields['run_seq'] = (str, 'null', '')
        self.fields['top_bot_inn'] = (int, 'null', '')
        self.fields['inning_num'] = (int, 'null', '')
        self.fields['start_outs'] = (int, 'null', '')
        self.fields['end_outs'] = (int, 'null', '')
        self.fields['start_first'] = (str, 'null', '')
        self.fields['start_second'] = (str, 'null', '')
        self.fields['start_third'] = (str, 'null', '')
        self.fields['end_first'] = (str, 'null', '')
        self.fields['end_second'] = (str, 'null', '')
        self.fields['end_third'] = (str, 'null', '')
        self.fields['second_stolen'] = (bool, 'null', '')
        self.fields['third_stolen'] = (bool, 'null', '')
        self.fields['home_stolen'] = (bool, 'null', '')
        self.fields['total_sb'] = (int, 'null', '')
        self.fields['second_caught'] = (bool, 'null', '')
        self.fields['third_caught'] = (bool, 'null', '')
        self.fields['home_caught'] = (bool, 'null', '')
        self.fields['total_cs'] = (int, 'null', '')
        self.fields['batter_scored'] = (bool, 'null', '')
        self.fields['first_scored'] = (bool, 'null', '')
        self.fields['second_scored'] = (bool, 'null', '')
        self.fields['third_scored'] = (bool, 'null', '')
        self.fields['total_runs'] = (int, 'null', '')
        self.fields['rbi'] = (int, 'null', '')
        super(Base, self).__init__()

        for x in self.values.keys():
            if self.fields[x][0] == bool:
                self.values[x] = False

    def GetStartStateFromSim(self, GameSim):
        self.values['start_outs'] = GameSim.outs
        self.values['start_first'] = GameSim.first_base
        self.values['start_second'] = GameSim.second_base
        self.values['start_third'] = GameSim.third_base

    def GetEndStateFromSim(self, GameSim):
        self.values['end_outs'] = GameSim.outs
        self.values['end_first'] = GameSim.first_base
        self.values['end_second'] = GameSim.second_base
        self.values['end_third'] = GameSim.third_base

class Team(Record):
    def __init__(self):
        pass


class Park(Record):
    def __init__(self):
        pass
