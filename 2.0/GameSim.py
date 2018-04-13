

class GameSim:
    def __init__(self):
        self.batter = ''
        self.activeHomePitcher = ''
        self.activeAwayPitcher = ''
        self.top_or_bot = 0
        self.inning = 1
        self.first_base = ''
        self.second_base = ''
        self.third_base = ''
        self.outs = 0

    def ProcessRSBase(self, runstr, currentBase):
        batter_scored  = first_scored = second_scored = third_scored = False
        sorter = {'3': 1, '2': 2, '1': 3, 'B': 4}
        if runstr != '':
            runners = filter(None, runstr.split(';'))
            runners = sorted(runners, key=lambda base: sorter[base[0]])
            if '2-1' in runners[0]:
                runners.insert(len(runners), runners.pop(0))
            for run in runners:
                if run[:3] == '1-2':
                    self.second_base = self.first_base
                    self.first_base = ''
                elif run[:3] == '1-3':
                    self.third_base = self.first_base
                    self.first_base = ''
                elif run[:3] == '1-H':
                    first_scored = True
                    self.first_base = ''
                elif run[:3] == '2-3':
                    self.third_base = self.second_base
                    self.second_base = ''
                elif run[:3] == '2-H':
                    second_scored = True
                    self.second_base = ''
                elif run[:3] == '3-H':
                    third_scored = True
                    self.third_base = ''
                elif run[:3] == 'B-1':
                    self.first_base = self.batter
                elif run[:3] == 'B-2':
                    self.second_base = self.batter
                elif run[:3] == 'B-3':
                    self.third_base = self.batter
                elif run[:3] == 'B-H':
                    batter_scored = True
                elif run[:2] == '1X':
                    if 'E' not in run:
                        self.outs += 1
                        self.first_base = ''
                    else:
                        run = run[:3].replace('X', '-')
                        (batter_scored, first_scored, second_scored, third_scored) = \
                            self.ProcessRSBase(run, currentBase)
                elif run[:2] == '2X':
                    if 'E' not in run:
                        self.outs += 1
                        self.second_base = ''
                    else:
                        run = run[:3].replace('X', '-')
                        (batter_scored, first_scored, second_scored, third_scored) = \
                            self.ProcessRSBase(run, currentBase)
                elif run[:2] == '3X':
                    if 'E' not in run:
                        self.outs += 1
                        self.third_base = ''
                    else:
                        run = run[:3].replace('X', '-')
                        (batter_scored, first_scored, second_scored, third_scored) = \
                            self.ProcessRSBase(run, currentBase)
                elif run[:2] == 'BX':
                    if 'E' not in run:
                        self.outs += 1
                    else:
                        run = run[:3].replace('X', '-')
                        (batter_scored, first_scored, second_scored, third_scored) = \
                            self.ProcessRSBase(run, currentBase)
                #Jean Segura Memorial Code
                elif run[:3] == '2-1':
                    self.first_base = self.second_base
                    self.second_base = None
        return (batter_scored, first_scored, second_scored, third_scored)

    def GetRunsRBI(self, playtype, currentBase):
        currentBase.total_runs = currentBase.second_scored + currentBase.third_scored \
            + currentBase.batter_scored + currentBase.first_scored
        if playtype in ('Interference','Walk','Hit By Pitch','Sacrifice Fly','Sacrifice Hit','Out','Fielders Choice', \
                        'Single','Double','Ground Rule Double','Triple','Home Run'):
            currentBase.rbi = currentBase.total_runs
        elif playtype == 'Reach on Error' and self.outs < 2:
            currentBase.rbi = currentBase.total_runs
        else:
            currentBase.rbi = 0

        if currentBase.rbi > 0:
            runs = currentBase.run_seq
            for runner in runs.split(';'):
                if('NR' in runner) or ('-H' in runner and '(E' in runner):
                    currentBase.rbi -= 1
                elif('XH' in runner) and ('E' in runner) and ('MREV' not in runner):
                    currentBase.rbi -= 1
        return (currentBase.total_runs, currentBase.rbi)

    def ProcessRSPlayType(self, playtype):
        if playtype in ('Stolen Base', 'Caught Stealing', 'Pick Off', 'Balk', 'Passed Ball','Wild Pitch', \
                        'Defensive Indifference', 'Error on Foul', 'Unknown Runner Activity'):
            plate_app = False
            at_bat =  False
        else:
            plate_app = True
            if playtype in ('Interference', 'Intentional Walk', 'Walk', 'Hit By Pitch', 'Sacrifice Fly' \
                            'Sacrifice Hit'):
                at_bat = False
            else:
                at_bat = True
        if playtype in ('Single', 'Double', 'Ground Rule Double', 'Triple', 'Home Run'):
            hit = True
        else:
            hit = False
        return (plate_app, at_bat, hit)
