from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, Float, Boolean, SmallInteger
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import sessionmaker
from RSParser import PlayerInfoParser
import databaseconfig as cfg
import urllib.request, re

class MyBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    '''
    @declared_attr
    def SetDefaults(cls):
        for x in cls.__table__.columns:
            print(x)
    '''

engine = create_engine("postgresql://%s:%s@%s/%s" % (cfg.user, cfg.pw, cfg.host, cfg.dbname))
DecBase = declarative_base(cls=MyBase)
Session = sessionmaker(bind=engine, expire_on_commit=False)

class Game(DecBase):
    game_key = Column(Integer, primary_key=True)
    game_id = Column(String(20), nullable=False)
    game_date = Column(Date, nullable=False)
    game_time = Column(Time, nullable=False)
    home_team_key = Column(SmallInteger, ForeignKey("team.team_key"), nullable=False)
    away_team_key = Column(SmallInteger, ForeignKey("team.team_key"), nullable=False)
    park_key = Column(SmallInteger, ForeignKey("park.park_key"), nullable=False)
    game_temp_f = Column(Float)
    wind_dir = Column(String(20))
    wind_speed_mph = Column(Float)
    field_condition = Column(String(20))
    precipitation = Column(String(20))
    sky_cond = Column(String(20))
    total_innings = Column(SmallInteger)
    home_hits = Column(SmallInteger)
    away_hits = Column(SmallInteger)
    home_runs = Column(SmallInteger)
    away_runs = Column(SmallInteger)
    home_team_win = Column(Boolean)
    tie = Column(Boolean)
    game_time_minutes = Column(SmallInteger)
    home_ump_id = Column(String(20))
    attendance = Column(Integer)

    def __repr__(self):
        return "<Game (game_key=%s, game_id='%s')>" % (self.game_key, self.game_id)

    def __init__(self, gameid):
        self.game_id = gameid
        self.total_innings = 0
        self.home_hits = 0
        self.away_hits = 0
        self.home_runs = 0
        self.away_runs = 0

    def add_info(self, row):
        gameinfo = {'visteam': 'away_team_key',
                    'hometeam': 'home_team_key',
                    'date': 'game_date',
                    'starttime': 'game_time',
                    'umphome': 'home_ump_id',
                    'temp': 'game_temp_f',
                    'winddir': 'wind_dir',
                    'windspeed': 'wind_speed_mph',
                    'fieldcond': 'field_condition',
                    'precip': 'precipitation',
                    'sky': 'sky_cond',
                    'timeofgame': 'game_time_minutes',
                    'attendance': 'attendance'
                    }
        if row.attribute in gameinfo.keys():
            setattr(self, gameinfo[row.attribute], row.value)

    @staticmethod
    def add_games(games):
        con = Session()
        con.add_all(games)
        con.commit()
        return True

    def add(self):
        con = Session()
        con.add(self)
        con.commit()
        return True

    @staticmethod
    def get_game_lookup():
        con = Session()
        lookup = {}
        for x in con.query(Game):
            lookup[x.game_id] = x.game_key
        return lookup


class HitBoxScore(DecBase):
    game_key = Column(Integer, ForeignKey("game.game_key"), primary_key=True)
    team_key = Column(SmallInteger, ForeignKey("team.team_key"), primary_key=True)
    player_key = Column(Integer, ForeignKey("hitter.player_key"), primary_key=True)
    batting_num = Column(SmallInteger, nullable=False)
    position = Column(String(5), nullable=False)
    plate_app = Column(SmallInteger)
    at_bat = Column(SmallInteger)
    so = Column(SmallInteger)
    hits = Column(SmallInteger)
    bb = Column(SmallInteger)
    ibb = Column(SmallInteger)
    hbp = Column(SmallInteger)
    runs = Column(SmallInteger)
    rbi = Column(SmallInteger)
    single = Column(SmallInteger)
    double = Column(SmallInteger)
    triple = Column(SmallInteger)
    hr = Column(SmallInteger)
    sb = Column(SmallInteger)
    cs = Column(SmallInteger)

    def __repr__(self):
        return "<HitBoxScore (game_key=%s, team_key='%s', player_key='%s')>" % \
               (self.game_key, self.team_key, self.player_key)

    def __init__(self, row=None):
        self.plate_app = 0
        self.at_bat = 0
        self.so = 0
        self.hits = 0
        self.bb = 0
        self.ibb = 0
        self.hbp = 0
        self.runs = 0
        self.rbi = 0
        self.single = 0
        self.double = 0
        self.triple = 0
        self.hr = 0
        self.sb = 0
        self.cs = 0
        if row is not None:
            self.batting_num = row.batnum
            self.position = row.position

    def update(self, row):
        self.batting_num = row.batnum
        self.position = row.position

    def increment_from_play(self, play, base):
        self.rbi += base.rbi
        self.plate_app += int(play.plate_app)
        self.at_bat += int(play.at_bat)
        self.hits += int(play.hit)
        if 'Walk' in play.play_type:
            self.bb += 1
            if 'Intentional Walk' in play.play_type:
                self.ibb += 1
        elif 'Strikeout' in play.play_type:
            self.k += 1
        elif 'Hit By Pitch' in play.play_type:
            self.hbp += 1
        elif play.play_type == 'Single':
            self.single += 1
        elif play.play_type in ('Double', 'Ground Rule Double'):
            self.double += 1
        elif play.play_type == 'Triple':
            self.triple += 1
        elif play.play_type == 'Home Run':
            self.hr += 1

    def increment_from_base(self, base, curbase):
        baseahead = {'first': 'second',
                     'second': 'third',
                     'third': 'home'}
        self.runs += int(getattr(base, curbase+'_scored'))
        self.sb += int(getattr(base, baseahead[curbase]+'_stolen'))
        self.cs += int(getattr(base, baseahead[curbase]+'_caught'))

    @staticmethod
    def add_lineups(lineups):
        con = Session()
        con.add_all(lineups)
        con.commit()
        return True


class PitchBoxScore(DecBase):
    game_key = Column(Integer, ForeignKey("game.game_key"), primary_key=True)
    team_key = Column(SmallInteger, ForeignKey("team.team_key"), primary_key=True)
    player_key = Column(Integer, ForeignKey("pitcher.player_key"), primary_key=True)
    pitch_role = Column(String(10), nullable=False)
    pitch_count = Column(SmallInteger)
    k = Column(SmallInteger)
    bb = Column(SmallInteger)
    ibb = Column(SmallInteger)
    hbp = Column(SmallInteger)
    hits = Column(SmallInteger)
    earned_runs = Column(SmallInteger)
    ip = Column(Float)
    strikes = Column(SmallInteger)
    balls = Column(SmallInteger)
    complete_game = Column(Boolean)
    shut_out = Column(Boolean)
    no_hitter = Column(Boolean)
    win = Column(Boolean)
    loss = Column(Boolean)
    save = Column(Boolean)
    swing_strikes = Column(SmallInteger)
    look_strikes = Column(SmallInteger)
    contact_strikes = Column(SmallInteger)
    flyballs = Column(SmallInteger)
    groundballs = Column(SmallInteger)
    line_drives = Column(SmallInteger)

    def __repr__(self):
        return "<PitchBoxScore (game_key=%s, team_key='%s', player_key='%s')>" % \
               (self.game_key, self.team_key, self.player_key)

    def __init__(self, lineup=None, role=None):
        self.pitch_count = 0
        self.k = 0
        self.bb = 0
        self.ibb = 0
        self.hbp = 0
        self.hits = 0
        self.earned_runs = 0
        self.ip = 0.0
        self.strikes = 0
        self.balls = 0
        self.complete_game = False
        self.shut_out = False
        self.no_hitter = False
        self.win = False
        self.loss = False
        self.save = False
        self.swing_strikes = 0
        self.look_strikes = 0
        self.contact_strikes = 0
        self.flyballs = 0
        self.groundballs = 0
        self.line_drives = 0

        if lineup is not None:
            self.team_key = lineup.team_key
        if role is not None:
            self.pitch_role = role

    def increment_from_play(self, play):
        self.pitch_count += play.strikes + play.balls
        self.strikes += play.strikes
        self.balls += play.balls
        self.swing_strikes += play.swing_x
        self.look_strikes += play.look_x
        self.contact_strikes += play.contact_x
        if 'Strikeout' in play.play_type:
            self.k += 1
        elif 'Walk' in play.play_type:
            self.bb += 1
            if 'Intentional' in play.play_type:
                self.ibb += 1
        elif play.hit:
            self.hits += 1
        ball_type = play.ball_type.replace('Strong ', '').replace('Weak ', '')
        if play.ball_type in ('Fly Ball', 'Pop Up', 'Bunt Pop'):
            self.flyballs += 1
        elif play.ball_type in ('Line Drive', 'Bunt Line Drive'):
            self.line_drives += 1
        elif play.ball_type in ('Ground Ball', 'Bunt Ground Ball'):
            self.groundballs += 1

    @staticmethod
    def AddRosters(rosters):
        con = Session()
        con.add_all(rosters)
        con.commit()
        return True

class Hitter(DecBase):
    player_key = Column(Integer, primary_key=True)
    name = Column(String(30))
    height_inch = Column(Float)
    weight_lbs = Column(Float)
    birth_date = Column(Date)
    mlb_debut_date = Column(Date)
    bat_hand = Column(String(5))
    throw_hand = Column(String(5))
    rs_user_id = Column(String(10))
    br_user_id = Column(String(10))

    def __repr__(self):
        return "<Hitter (player_key=%s, name='%s')>" % (self.player_key, self.name)

    def GetInfofromRS(self):
        rs = PlayerInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % \
              (self.rs_user_id[0].upper(), self.rs_user_id)
        try:
            html = urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8').replace('&#183;', '*')
        except:
            print('Cannot connect to RetroSheet')
            return False
        rs.feed(html)
        self.name = rs.name
        self.bat_hand = rs.batHand
        self.throw_hand = rs.throwHand
        self.birth_date = rs.birthDate
        self.mlb_debut_date = rs.debutDate
        self.height_inch = float(rs.height)
        self.weight_lbs = float(rs.weight)

    @staticmethod
    def GetHitterRSLookup():
        con = Session()
        lookup = {}
        for x in con.query(Hitter):
            lookup[x.rs_user_id] = x.player_key
        return lookup

    @staticmethod
    def AddNewHitters(newhitters):
        con = Session()
        con.add_all(newhitters)
        con.commit()
        return True



class Pitcher(DecBase):
    player_key = Column(Integer, primary_key=True)
    name = Column(String(30))
    height_inch = Column(Float)
    weight_lbs = Column(Float)
    birth_date = Column(Date)
    mlb_debut_date = Column(Date)
    bat_hand = Column(String(5))
    throw_hand = Column(String(5))
    rs_user_id = Column(String(10))
    br_user_id = Column(String(10))

    def __repr__(self):
        return "<Pitcher (player_key=%s, name='%s')>" % (self.player_key, self.name)

    def GetInfofromRS(self):
        rs = PlayerInfoParser()
        url = "http://www.retrosheet.org/boxesetc/%s/P%s.htm" % \
              (self.rs_user_id[0].upper(), self.rs_user_id)
        try:
            html = urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8').replace('&#183;', '*')
        except:
            print('Cannot connect to RetroSheet')
            return False
        rs.feed(html)
        self.name = rs.name
        self.bat_hand = rs.batHand
        self.throw_hand = rs.throwHand
        self.birth_date = rs.birthDate
        self.mlb_debut_date = rs.debutDate
        self.height_inch = float(rs.height)
        self.weight_lbs = float(rs.weight)

    @staticmethod
    def GetPitcherRSLookup():
        con = Session()
        lookup = {}
        for x in con.query(Pitcher):
            lookup[x.rs_user_id] = x.player_key
        return lookup

    @staticmethod
    def AddNewPitchers(newpitchers):
        con = Session()
        con.add_all(newpitchers)
        con.commit()
        return True


class Play(DecBase):
    game_key = Column(Integer, ForeignKey("game.game_key"), primary_key=True)
    play_seq_no = Column(SmallInteger, primary_key=True)
    hitter_key = Column(Integer, ForeignKey("hitter.player_key"))
    pitcher_key = Column(Integer, ForeignKey("pitcher.player_key"))
    top_bot_inn = Column(SmallInteger)
    inning_num = Column(SmallInteger)
    pitch_seq = Column(String(30))
    play_seq = Column(String(100))
    play_type = Column(String(30))
    plate_app = Column(Boolean)
    at_bat = Column(Boolean)
    hit = Column(Boolean)
    strikes = Column(SmallInteger)
    balls = Column(SmallInteger)
    contact_x = Column(SmallInteger)
    swing_x = Column(SmallInteger)
    look_x = Column(SmallInteger)
    ball_loc = Column(String(10))
    ball_type = Column(String(20))

    def __init__(self, sim, row):
        self.play_seq_no = sim.playcount
        self.hitter_key = sim.batter
        self.top_bot_inn = sim.topbotinn
        self.inning_num = sim.inning
        self.pitch_seq = row.pitchseq
        self.play_seq = row.playseq.replace('/MREV', '').replace('/UREV', '')
        if int(sim.topbotinn) == 0:
            self.pitcher_key = sim.activehomepitcher
        else:
            self.pitcher_key = sim.activeawaypitcher
        self.balls = 0
        self.contact_x = 0
        self.look_x = 0
        self.swing_x = 0
        self.calc_pitch_data()

    def calc_pitch_data(self):
        for pitch in self.pitch_seq:
            if pitch in ('F', 'X', 'L', 'O', 'R', 'T'):
                self.contact_x += 1
            elif pitch == 'C':
                self.look_x += 1
            elif pitch in ('S', 'M', 'Q', 'K'):
                self.swing_x += 1
            elif pitch in ('B', 'H', 'I', 'P', 'U', 'Y'):
                self.balls += 1
            self.strikes = self.contact_x + self.look_x + self.swing_x

    def classify_play(self):
        if self.play_type in ('Stolen Base', 'Caught Stealing', 'Pick Off', 'Balk', 'Passed Ball', 'Wild Pitch'
                        'Defensive Indifference', 'Error on Foul', 'Unknown Runner Activity'):
            self.plate_app = False
        else:
            self.plate_app = True
            if 'Walk' in self.play_type or 'Sacrifice' in self.play_type or self.play_type == 'Hit By Pitch':
                self.at_bat = False
            else:
                self.at_bat = True
                if self.play_type in ('Single', 'Double', 'Ground Rule Double', 'Triple', 'Home Run'):
                    self.hit = True


    def __repr__(self):
        return "<Play (game_key=%s, play_seq_no='%s')>" % (self.game_key, self.play_seq_no)

    @staticmethod
    def AddPlays(plays):
        con = Session()
        con.add_all(plays)
        con.commit()
        return True


class Base(DecBase):
    game_key = Column(Integer, ForeignKey("game.game_key"), primary_key=True)
    play_seq_no = Column(SmallInteger, ForeignKey("play.play_seq_no"), primary_key=True)
    run_seq = Column(String(20))
    top_bot_inn = Column(SmallInteger)
    inning_num = Column(SmallInteger)
    start_outs = Column(SmallInteger)
    end_outs = Column(SmallInteger)
    start_first = Column(String(10))
    start_second = Column(String(10))
    start_third = Column(String(10))
    end_first = Column(String(10))
    end_second = Column(String(10))
    end_third = Column(String(10))
    second_stolen = Column(Boolean)
    third_stolen = Column(Boolean)
    home_stolen = Column(Boolean)
    total_sb = Column(SmallInteger)
    second_caught = Column(Boolean)
    third_caught = Column(Boolean)
    home_caught = Column(Boolean)
    total_cs = Column(SmallInteger)
    batter_scored = Column(Boolean)
    first_scored = Column(Boolean)
    second_scored = Column(Boolean)
    third_scored  = Column(Boolean)
    total_runs = Column(SmallInteger)
    rbi = Column(SmallInteger)

    def __repr__(self):
        return "<Base (game_key=%s, play_seq_no='%s')>" % (self.game_key, self.play_seq_no)

    def __init__(self, sim, row):
        self.run_seq = row.playseq.split('.')[1] if len(row.playseq.split('.')) > 1 else ''
        self.top_bot_inn = row.topbotinn
        self.inning_num = row.inningnum
        self.start_outs = sim.outs
        self.end_outs = 0
        self.start_first = sim.first_base
        self.start_second = sim.second_base
        self.start_third = sim.third_base
        self.end_first = ''
        self.end_second = ''
        self.end_third = ''
        self.second_stolen = False
        self.third_stolen = False
        self.home_stolen = False
        self.total_sb = 0
        self.second_caught = False
        self.third_caught = False
        self.home_caught = False
        self.total_cs = 0
        self.batter_scored = False
        self.first_scored = False
        self.second_scored = False
        self.third_scored = False
        self.total_runs = 0
        self.rbi = 0

    def calc_end_play_stats(self, sim):
        sorter = {'3': 1, '2': 2, '1': 3, 'B': 4}
        steallookup = {'*2': 'second_stolen', '*3': 'third_stolen', '*H': 'home_stolen'}
        caughtlookup = {'#2': 'second_caught', '#3': 'third_caught', '#H': 'home_caught'}
        scorelookup = {'B': 'batter_scored', '1': 'first_scored', '2': 'second_scored', '3': 'third_scored'}
        self.end_outs = sim.outs
        self.end_first = sim.first_base
        self.end_second = sim.second_base
        self.end_third = sim.third_base
        runners = filter(None, self.run_seq.split(';'))
        runners = sorted(runners, key=lambda base: sorter[base[0]])
        for run in runners:
            if re.search('^[123](\*[23H])$', run) != None:
                setattr(self, steallookup[re.search('^[123](\*[23H])$', run).group(1)], True)
                if self.home_stolen:
                    self.third_scored = True
            if re.search('^[123](#[23H])', run) != None:
                setattr(self, caughtlookup[re.search('^[123](#[23H])', run).group(1)], True)
            if re.search('^([B123])[-\*]H', run) != None:
                setattr(self, scorelookup[re.search('^([B123])[-\*]H', run).group(1)], True)
                if '(NR)' in run:
                    self.rbi -= 1
        self.total_sb =  self.second_stolen + self.third_stolen + self.home_stolen
        self.total_cs = self.second_caught + self.third_caught + self.home_caught
        self.total_runs = self.first_scored + self.second_scored + self.third_scored + self.batter_scored

    def figure_out_rbi(self, playname):
        if playname in ('Stolen Base', 'Caught Stealing', 'Pick Off', 'Balk', 'Passed Ball', 'Wild Pitch'
                        'Defensive Indifference', 'Error on Foul', 'Unknown Runner Activity',
                        'Ground Double Play', 'Triple Play', 'Ground Triple Play'):
            self.rbi = 0
        elif 'Strikeout' in playname:
            self.rbi = 0
        else:
            self.rbi += self.total_runs


    @staticmethod
    def AddBases(bases):
        con = Session()
        con.add_all(bases)
        con.commit()
        return True


class Team(DecBase):
    team_key = Column(SmallInteger, primary_key=True)
    team_locale = Column(String(50))
    team_mascot = Column(String(50))
    team_abbrev_rs = Column(String(5))
    team_abbrev_br = Column(String(5))
    league = Column(String(2))
    regional_division = Column(String(10))
    first_season = Column(SmallInteger)
    last_season = Column(SmallInteger)

    def __repr__(self):
        return "<Team (team_key=%s, team_abbrev='%s')>" % (self.team_key, self.team_abbrev_br)


class Park(DecBase):
    park_key = Column(SmallInteger, primary_key=True)
    park_name = Column(String(50))
    team_key = Column(SmallInteger, ForeignKey("team.team_key"))
    park_open_date = Column(Date)
    park_close_date = Column(Date)
    park_zip_code = Column(String(10))
    turf_type = Column(String(30))
    roof_type = Column(String(30))
    seating_capacity = Column(Integer)

    def __repr__(self):
        return "<Park (park_key=%s, name='%s')>" % (self.park_key, self.park_name)
