from GameSim import GameSim
from Baseball import Hitter, Pitcher, Game, Play, Base, HitBoxScore, PitchBoxScore

class Row:
    def __init__(self, gameid, row, rowcount):
        self.gameid = gameid
        self.rowcount = rowcount
        self.rowstr = ','.join(row)


class InfoRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.attribute = row[1]
        self.value = row[2]
        super(InfoRow, self).__init__(gameid, row, rowcount)


class PlayRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.inningnum = row[1]
        self.topbotinn = row[2]
        self.playerid = row[3]
        self.pitchcount = row[4]
        self.pitchseq = row[5]
        self.playseq = row[6]
        super(PlayRow, self).__init__(gameid, row, rowcount)

class SubRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.playerid = row[1]
        self.playername = row[2].strip('"')
        self.teamind = row[3]
        self.batnum = row[4]
        self.posnum = row[5]
        super(SubRow, self).__init__(gameid, row, rowcount)

class DataRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.datatype = row[1]
        self.playerid = row[2]
        self.value = row[3]
        super(DataRow, self).__init__(gameid, row, rowcount)

class RSLog:
    def __init__(self, filename):
        self.filename = filename

    def scrape(self):
        rowcount = 0
        currentgame = ''
        currentsim = None
        games = {}
        gamelineups = {}
        gamerosters = {}
        gameplays = {}
        gamebases = {}
        text = open(self.filename, 'a')
        text.write('\nid,dunzo')
        text.close()
        text = open(self.filename, 'r')
        for line in text:
            row = line.strip('\n').split(',')
            rowtype = row[0]
            rowcount += 1
            if rowtype == 'id':
                if currentgame != '':
                    currentsim.currentgame.get_end_game_stats(currentsim)
                    currentsim.roster[currentsim.winningpit].win = True
                    currentsim.roster[currentsim.losingpit].loss = True
                    if currentsim.savingpit != '':
                        currentsim.roster[currentsim.savingpit].save = True
                    for pitcher in currentsim.roster.keys():
                        if currentsim.roster[pitcher].ip >= 9.0:
                            currentsim.roster[pitcher].complete_game = True
                            if currentsim.roster[pitcher].runs == 0:
                                currentsim.roster[pitcher].shut_out = True
                                if currentsim.roster[pitcher].hits == 0:
                                    currentsim.roster[pitcher].no_hitter = True
                    games[currentgame] = currentsim.currentgame
                    gamelineups[currentgame] = currentsim.lineup
                    gamerosters[currentgame] = currentsim.roster
                    gameplays[currentgame] = currentsim.plays
                    gamebases[currentgame] = currentsim.bases
                if row[1] != 'dunzo':
                    currentgame = row[1]
                    currentsim = GameSim(row[1])
            elif rowtype == 'info':
                currentsim.read_info_row_data(InfoRow(currentgame, row, rowcount))
            elif rowtype == 'start':
                currentsim.add_lineup(SubRow(currentgame, row, rowcount))
                if int(row[5]) == 1:
                    currentsim.add_roster(SubRow(currentgame, row, rowcount), 'Starter')
            elif rowtype == 'play':
                currentsim.read_play_row_data(PlayRow(currentgame, row, rowcount))
            elif rowtype == 'sub':
                currentsim.read_sub_row_data(SubRow(currentgame, row, rowcount))
            elif rowtype == 'data':
                currentsim.read_data_row_data(DataRow(currentgame, row, rowcount))

        return {'games': games, 'lineups': gamelineups, 'rosters': gamerosters, 'plays': gameplays, 'bases': gamebases}

    def add_to_db(self, games=None, lineups=None, rosters=None, plays=None, bases=None):
        addplays = []
        addbases = []
        addlineups = []
        addrosters = []
        newhitters = []
        newpitchers = []
        if lineups != None:
            print('Getting New Hitters')
            hitterlookup = Hitter().get_hitter_rs_lookup()
            for game in games:
                for h in lineups[game].keys():
                    if h not in hitterlookup:
                        newhitter = Hitter()
                        newhitter.rs_user_id = h
                        newhitter.get_info_from_rs()
                        newhitters.append(newhitter)
                        hitterlookup[h] = Hitter()
            Hitter().add_new_hitters(newhitters)
            hitterlookup = Hitter().get_hitter_rs_lookup()
        else:
            hitterlookup = Hitter().get_hitter_rs_lookup()
        if rosters != None:
            print('Getting New Pitchers')
            pitcherlookup = Pitcher().get_pitcher_rs_lookup()
            for game in games:
                for h in rosters[game].keys():
                    if h not in pitcherlookup:
                        newpitcher = Pitcher()
                        newpitcher.rs_user_id = h
                        newpitcher.get_info_from_rs()
                        newpitchers.append(newpitcher)
                        pitcherlookup[h] = Pitcher()
            Pitcher().add_new_pitchers(newpitchers)
            pitcherlookup = Pitcher().get_pitcher_rs_lookup()
        else:
            pitcherlookup = Pitcher().get_pitcher_rs_lookup()
        if games != None:
            print('Adding Games')
            Game.add_games(games.values())
            gamelookup = Game.get_game_lookup()

            for gameid in games.keys():
                thisgame = gamelookup[gameid]
                games[gameid].game_key = thisgame
                if plays != None:
                    for play in plays[gameid]:
                        play.game_key = thisgame
                        play.hitter_key = hitterlookup[play.hitter_key]
                        play.pitcher_key = pitcherlookup[play.pitcher_key]
                        addplays.append(play)
                if bases != None:
                    for base in bases[gameid]:
                        base.game_key = thisgame
                        addbases.append(base)
                if lineups != None:
                    for lineup in lineups[gameid].keys():
                        val = lineups[gameid][lineup]
                        val.game_key = thisgame
                        val.player_key = hitterlookup[lineup]
                        addlineups.append(val)
                if rosters != None:
                    for roster in rosters[gameid].keys():
                        val = rosters[gameid][roster]
                        val.game_key = thisgame
                        val.player_key = pitcherlookup[roster]
                        addrosters.append(val)
            print('Adding Plays')
            Play.add_plays(addplays)
            print('Adding Bases')
            Base.add_bases(addbases)
            print('Adding Lineups')
            HitBoxScore.add_lineups(addlineups)
            print('Adding Rosters')
            PitchBoxScore.add_rosters(addrosters)