from Baseball import Game, HitBoxScore, PitchBoxScore, Play, Base
from datetime import date, datetime
import RetroPlayConverter

import json

PosLookup = ['X', 'P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'X', 'PH', 'PR']
with open('TeamLookup.json', 'r') as out:
    TeamLookup = json.load(out)


class GameSim:
    def __init__(self, gameid):
        self.currentgame = Game(gameid)
        self.playstarted = False
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
        siminfo = {'visteam': 'awayteam',
                   'hometeam': 'hometeam',
                   'wp': 'winningpit',
                   'lp': 'losingpit',
                   'save': 'savingpit'
                   }
        if row.attribute in ('visteam','hometeam'):
            row.value = TeamLookup[row.value.strip('\n')]
            self.currentgame.add_info(row)
        elif row.attribute == 'date':
            dateparts = row.value.split('/')
            row.value = date(int(dateparts[0]), int(dateparts[1]), int(dateparts[2]))
            self.currentgame.add_info(row)
        elif row.attribute == 'starttime':
            row.value = datetime.strptime(row.value, '%I:%M%p').time()
            self.currentgame.add_info(row)
        elif row.attribute in siminfo.keys():
            setattr(self, siminfo[row.attribute], row.value)
        else:
            self.currentgame.add_info(row)

    def add_lineup(self, row):
        row.position = PosLookup[int(row.posnum)]
        self.lineup[row.playerid] = HitBoxScore(row)
        if int(row.teamind) == 0:
            self.lineup[row.playerid].team_key = self.currentgame.away_team_key
        else:
            self.lineup[row.playerid].team_key = self.currentgame.home_team_key

    def update_lineup(self, row):
        row.position = PosLookup[int(row.posnum)]
        self.lineup[row.playerid].update(row)

    def read_play_row_data(self, row):
        if self.playstarted is False:
            self.sub_in_starters()
            self.playstarted = True
        if row.topbotinn != self.topbotinn:
            self.reset_base_out_state()
        self.topbotinn = row.topbotinn
        self.inning = row.inningnum
        self.batter = row.playerid
        if row.playseq == 'NP':
            self.playcount += 1
            currentplay = Play(self, row)
            currentbase = Base(self, row)
            currentplay.play_type = get_rs_play(currentplay.playseq)
            self.get_ball_type()

    def get_ball_type(self):
        for x in self.play_seq.split('/')[1:]:
            if re.search('^[0-9]{1,2}$', x) != None:
                self.ball_loc = x
            if re.search('^B?[LFGP][0-9]', x) != None:
                self.ball_loc = re.search('^B?[LFGP]([0-9])', x).group(1)
            if re.search('L', x) != None:
                self.ball_type = 'Line Drive'
            if re.search('F', x) != None:
                self.ball_type = 'Fly Ball'
            if re.search('G', x) != None:
                self.ball_type = 'Ground Ball'
            if re.search('P', x) != None and re.search('DP', x) == None:
                self.ball_type = 'Pop Up'
            if re.search('BP', x) != None:
                self.ball_type = 'Bunt Pop'
            if re.search('BL', x) != None:
                self.ball_type = 'Bunt Line Drive'
            if re.search('BG', x) != None:
                self.ball_type = 'Bunt Ground Ball'

    def sub_in_starters(self):
        for userid in self.lineup.keys():
            if self.lineup[userid].position == 'P':
                self.roster[userid] = PitchBoxScore(self.lineup[userid], 'Starter')
                if self.roster[userid].team_key == self.currentgame.home_team_key:
                    self.activehomepitcher = userid
                else:
                    self.activeawaypitcher = userid

    def read_sub_row_data(self, row):
        pass

    def read_data_row_data(self, row):
        pass


