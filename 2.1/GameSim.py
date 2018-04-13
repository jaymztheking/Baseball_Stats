from Baseball import Game, HitBoxScore
import json

PosLookup = ['X', 'P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'X', 'PH', 'PR']
with open('TeamLookup.json', 'r') as out:
    TeamLookup = json.load(out)


class GameSim:
    def __init__(self):
        self.currentgame = Game()
        self.awayteam = ''
        self.hometeam = ''
        self.playcount = 0
        self.plays = []
        self.bases = []
        self.lineup = {}
        self.roster = {}
        self.activehomepitcher = ''
        self.activeawaypitcher = ''
        self.batter = ''
        self.first_base = ''
        self.second_base = ''
        self.third_base = ''
        self.inning = 1
        self.topbotinn = 0
        self.homeruns = 0
        self.awayruns = 0
        self.homehits = 0
        self.awayhits = 0
        self.winningpit = ''
        self.losingpit = ''
        self.savingpit = ''

    def reset_base_out_state(self):
        self.outs = 0
        self.first_base = ''
        self.second_base = ''
        self.third_base = ''

    def read_info_row_data(self, row):
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
        siminfo = {'visteam': 'awayteam',
                   'hometeam': 'hometeam',
                   'wp': 'winningpit',
                   'lp': 'losingpit',
                   'save': 'savingpit'
                   }
        if row.attribute in gameinfo.keys():
            if row.attribute in ('visteam','hometeam'):
                setattr(self.currentgame, gameinfo[row.attribute], TeamLookup[row.value])
            else:
                setattr(self.currentgame, gameinfo[row.attribute], row.value)
        if row.attribute in siminfo.keys():
            setattr(self, gameinfo[row.attribute], row.value)

    def read_start_row_data(self, row):
        if row.playerid not in self.lineup:
            self.lineup[row.playerid] = HitBoxScore()
            self.lineup[row.playerid].player_key = row.playerid
        self.lineup[row.playerid].batting_num = row.batnum
        self.lineup[row.playerid].position = PosLookup[int(row.posnum)]
        teamkey = self.currentgame.home_team_key if int(row.teamind) == 1 else self.currentgame.away_team_key
        self.lineup[row.playerid].team_key = teamkey

    def read_play_row_data(self, row):
        pass

    def read_sub_row_data(self, row):
        pass

    def read_data_row_data(self, row):
        pass


class BaseballDicts:
    games = {}
    plays = {}
    bases = {}
    lineups = {}
    rosters = {}