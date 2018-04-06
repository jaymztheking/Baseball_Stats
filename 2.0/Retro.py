from Baseball import Game, HitBoxScore, PitchBoxScore
from GameSim import GameSim
import databaseconfig as cfg

class RSLog:
    def __init__(self, file):
        self.filename = file

    def ResetGame(self):
        self.currentGame = Game()
        self.currentSim = GameSim()
        self.plays = {}
        self.lineup = {}
        self.pitroster = {}

    def ScrapeInfoRow(self, row):
        x = row[1]
        if x == 'visteam':
            self.currentGame.values['away_team_key'] = str(row[2].strip())
            return True
        elif x == 'hometeam':
            self.currentGame.values['home_team_key'] = str(row[2].strip())
            return True
        elif x == 'date':
            datePieces = row[2].split('/')
            self.currentGame.values['game_date'] = date(int(datePieces[0]), int(datePieces[1]), int(datePieces[2]))


    def ScrapeLineupRow(self, row):
        pass

    def ScrapePlayRow(self, row):
        pass

    def ParseLog(self, storageMethod):
        text = open(self.filename, 'a')
        text.write('\nid,dunzo') #dummy row to find end of file
        text.close()
        text = open(self.filename, 'r')
        self.currentGame = None

        for line in text:
            line = line.replace('!', '')
            row = line.split(',')
            rowType = row[0]

            if rowType == 'info':
                self.ScrapeInfoRow(row)
            elif rowType == 'start':
                self.ScrapeLineupRow(row)
            elif rowType == 'play':
                self.ScrapePlayRow(row)
            elif rowType == 'sub':
               if int(row[5]) == 1:
                   pass #Sub Pitcher
               elif int(row[5]) == 11:
                   pass  #Sub Hitter
               elif int(row[5]) == 12:
                   pass  #Sub Runner
               else:
                   pass  #Sub Defender
            elif rowType == 'data':
                pass #do something to add earned runs
            elif rowType == 'id':
                if self.currentGame is not None:
                    pass #save all the stuff
                self.ResetGame()
                self.currentGame.values['game_id'] = str(row[1])


