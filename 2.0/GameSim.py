

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
                    currentBase.first_scored = True
                    self.first_base = ''
                elif run[:3] == '2-3':
                    self.third_base = self.second_base
                    self.second_base = ''
                elif run[:3] == '2-H':
                    currentBase.second_scored = True
                    self.second_base = ''
                elif run[:3] == '3-H':
                    currentBase.third_scored = True
                    self.third_base = ''
                elif run[:3] == 'B-1':
                    self.first_base = self.batter
                elif run[:3] == 'B-2':
                    self.second_base = self.batter
                elif run[:3] == 'B-3':
                    self.third_base = self.batter
                elif run[:3] == 'B-H':
                    currentBase.batter_scored = True
                elif run[:2] == '1X':
                    if 'E' not in run:
                        self.outs += 1
                        self.first_base = ''
                    else:
                        run  = run[:3].replace('X', '-')
                        currentBase = self.ProcessRSBase(run, currentBase)
                elif run[:2] == '2X':
                    if 'E' not in run:
                        self.outs += 1
                        self.second_base = ''
                    else:
                        run = run[:3].replace('X', '-')
                        currentBase = self.ProcessRSBase(run, currentBase)
                elif run[:2] == '3X':
                    if 'E' not in run:
                        self.outs += 1
                        self.third_base = ''
                    else:
                        run = run[:3].replace('X', '-')
                        currentBase = self.ProcessRSBase(run, currentBase)
                #Jean Segura Memorial Code
                elif run[:3] == '2-1':
                    self.first_base = self.second_base
                    self.second_base = None
        return currentBase

    def GetRunsRBI(self, playtype, currentBase):
        currentBase.values['total_runs'] = currentBase.values['second_scored'] + currentBase.values['third_scored'] \
            + currentBase.values['batter_scored'] + currentBase.values['first_scored']
        if playtype in ('Interference','Walk','Hit By Pitch','Sacrifice Fly','Sacrifice Hit','Out','Fielders Choice', \
                        'Single','Double','Ground Rule Double','Triple','Home Run'):
            currentBase.values['rbi'] = currentBase.values['total_runs']
        elif playtype == 'Reach on Error' and self.outs < 2:
            currentBase.values['rbi'] = currentBase.values['total_runs']
        else:
            currentBase.values['rbi'] = 0

        if currentBase.values['rbi'] > 0:
            runs = currentBase.values['run_seq']
            for runner in runs.split(';'):
                if('NR' in runner) or ('-H' in runner and '(E' in runner):
                    currentBase.values['rbi'] -= 1
                elif('XH' in runner) and ('E' in runner) and ('MREV' not in runner):
                    currentBase.values['rbi'] -= 1
        return currentBase
