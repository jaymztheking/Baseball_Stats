

class Lineup:
    game = 0
    team = 0
    player = 0
    player_bat_num = 0
    player_pos = ''
    AB = 0
    Hits = 0
    BB = 0
    HBP = 0
    Runs = 0
    RBI = 0
    Single = 0
    Double = 0
    Triple = 0
    HR = 0
    SB = 0
    CS = 0
    
    def __init__(self, game, team, player, batnum, pos):
        self.game = game
        self.team = team
        self.player = player
        self.player_bat_num = batnum
        self.player_pos = pos
    
    