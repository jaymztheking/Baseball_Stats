from Baseball import Game, HitBoxScore, PitchBoxScore, Play, Base
from datetime import date, datetime
import re
from RetroPlayConverter import get_rs_play, get_rs_run_seq, get_rs_ball_type

import json

PosLookup = ['X', 'P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'X', 'PH', 'PR']
with open('TeamLookup.json', 'r') as out:
    TeamLookup = json.load(out)


class GameSim:
    def __init__(self, gameid):
        self.currentgame = Game(gameid)
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
        self.outs = 0
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

    def add_roster(self, row, role):
        if int(row.teamind) == 0:
            self.roster[row.playerid] = PitchBoxScore(row, role)
            self.roster[row.playerid].team_key = self.currentgame.away_team_key
            self.activeawaypitcher = row.playerid
        else:
            self.roster[row.playerid] = PitchBoxScore(row, role)
            self.roster[row.playerid].team_key = self.currentgame.home_team_key
            self.activehomepitcher = row.playerid

    def read_play_row_data(self, row):
        if row.topbotinn != self.topbotinn:
            self.reset_base_out_state()
        self.topbotinn = row.topbotinn
        self.inning = row.inningnum
        self.batter = row.playerid
        pitcher = self.activeawaypitcher if int(self.topbotinn) == 1 else self.activehomepitcher
        if row.playseq != 'NP':
            self.playcount += 1
            if self.currentgame.game_id == 'BOS201705120':
                print('Yo')
            currentplay = Play(self, row)
            currentbase = Base(self, row)
            currentplay.play_type = get_rs_play(currentplay.play_seq)
            currentplay.classify_play()
            currentplay.ball_loc, currentplay.ball_type = get_rs_ball_type(currentplay.play_seq.split('.')[0])
            currentbase.run_seq = get_rs_run_seq(currentbase.run_seq, currentplay.play_seq, currentplay.play_type, self)
            self.get_outs(currentplay.play_type, currentbase.run_seq)
            self.move_runners(currentbase.run_seq)
            currentbase.calc_end_play_stats(self)
            currentbase.figure_out_rbi(currentplay.play_type, self.outs)
            self.lineup[row.playerid].increment_from_play(currentplay, currentbase)
            baserunners = {currentplay.hitter_key: 'batter',
                           currentbase.start_first: 'first',
                           currentbase.start_second: 'second',
                           currentbase.start_third: 'third'}
            for br in baserunners.keys():
                if br != '':
                    self.lineup[br].increment_from_base(currentbase, baserunners[br])
            self.roster[pitcher].increment_from_play(currentplay)
            if int(self.topbotinn) == 0:
                self.awayhits += int(currentplay.hit)
                self.awayruns += currentbase.total_runs
            else:
                self.homehits += int(currentplay.hit)
                self.homeruns += currentbase.total_runs
            self.plays.append(currentplay)
            self.bases.append(currentbase)

    def get_outs(self, playtype, runseq):
        if playtype == 'Triple Play':
            self.outs = 3
        else:
            for char in runseq:
                if char in ('#','X'):
                    self.outs += 1

    def move_runners(self, runseq):
        sorter = {'3': 1, '2': 2, '1': 3, 'B': 4}
        baselookup = {'B':'batter', '1':'first_base', '2':'second_base', '3':'third_base'}
        runseq = runseq.split(';')
        runners = filter(None, runseq)
        runners = sorted(runners, key=lambda base: sorter[base[0]])
        #Stupid Jean Segura Play
        if len(runners) > 0 and '2-1' in runners[0]:
            runners.insert(len(runners), runners.pop(0))
        #Successful Advance
        for run in runners:
            # Successful Advance
            if re.search('([B123])[-\*]([123])', run) != None:
                setattr(self, baselookup[re.search('([B123])[-\*]([123])', run).group(2)],
                        getattr(self, baselookup[re.search('([B123])[-\*]([123])', run).group(1)]))
                if re.search('([B123])[-\*]([123])', run).group(2) != re.search('([B123])[-\*]([123])', run).group(1):
                    setattr(self, baselookup[re.search('([B123])[-\*]([123])', run).group(1)], '')
            #Runner back to dugout
            elif re.search('([B123])[#X][123H]', run) != None:
                if re.search('\([1-9]?E[1-9](/TH)?\)', run) != None:
                    runners.remove(run)
                    runners.append(run.replace('X','-'))
                    self.move_runners(';'.join(runners))
                    break
                else:
                    setattr(self, baselookup[re.search('([B123])[#X][123H]', run).group(1)], '')
            #Runner scores
            if re.search('([B123])[-\*]H', run) != None:
                setattr(self, baselookup[re.search('([B123])[-\*]H', run).group(1)], '')

    def read_sub_row_data(self, row):
        if int(row.posnum) == 1:
            if int(self.topbotinn) == 0:
                self.sub_in_reliever(self.activeawaypitcher, row)
            else:
                self.sub_in_reliever(self.activehomepitcher, row)
        elif int(row.posnum) == 12:
            basevalues = ['first_base', 'second_base', 'third_base']
            base = ''
            for b in basevalues:
                if getattr(self, b) == row.playerid:
                    base = b
            self.sub_in_pinch_runner(row, base)
        else:
            self.sub_in_hitter(row)

    def sub_in_reliever(self, exitpitch, row):
        self.calc_ip(exitpitch, row)
        if row.playerid not in self.lineup.keys():
            self.add_lineup(row)
        else:
            self.update_lineup(row)
        if row.playerid not in self.roster.keys():
            self.add_roster(row, 'Reliever')

    def calc_ip(self, pitcher, row):
        # Figure out Innings Pitcher for Mound Exiter
        IP = float(self.inning) - 1 + float(self.outs / 3.0)
        for pit in self.roster.keys():
            if int(row.teamind) == 0 and self.roster[pit].team_key == self.currentgame.away_team_key:
                IP -= self.roster[pit].ip
            elif self.roster[pit].team_key == self.currentgame.home_team_key:
                IP -= self.roster[pit].ip
        self.roster[pitcher].ip = IP

    def sub_in_hitter(self, row):
        if row.playerid not in self.lineup.keys():
            self.add_lineup(row)
        else:
            self.update_lineup(row)

    def sub_in_pinch_runner(self, row, base):
        self.add_lineup(row)
        setattr(self, base, row.playerid)

    def read_data_row_data(self, row):
        if row.datatype == 'er':
            self.roster[row.playerid].earned_runs += int(row.value)

