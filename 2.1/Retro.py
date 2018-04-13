class Row:
    def __init__(self, gameid, row, rowcount):
        self.gameid = gameid
        self.rowcount = rowcount
        self.rowstr = ','.join(row)


class InfoRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.attribute = row[1]
        self.value = str(row[2])
        super(InfoRow, self).__init__(gameid, row, rowcount)


class StartRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.playerid = row[1]
        self.playername = row[2].strip('"')
        self.teamind = row[3]
        self.batnum = row[4]
        self.posnum = row[5]
        super(StartRow, self).__init__(gameid, row, rowcount)


class PlayRow(Row):
    def __init__(self, gameid, row, rowcount):
        self.inningnum = row[1]
        self.toporbotinn = row[2]
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

    def generate_rows(self):
        rows = []
        rowcount = 0
        text = open(self.filename, 'r')
        currentgame = None
        for line in text:
            row = line.split(',')
            rowtype = row[0]
            rowcount += 1
            if rowtype == 'id':
                currentgame = row[1]
            elif rowtype == 'info':
                rows.append(InfoRow(currentgame, row, rowcount))
            elif rowtype == 'start':
                rows.append(StartRow(currentgame, row, rowcount))
            elif rowtype == 'play':
                rows.append(PlayRow(currentgame, row, rowcount))
            elif rowtype == 'sub':
                rows.append(SubRow(currentgame, row, rowcount))
            elif rowtype == 'data':
                rows.append(StartRow(currentgame, row, rowcount))
        return rows

