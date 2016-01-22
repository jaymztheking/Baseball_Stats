import HTMLParser

class LineScoreParser(HTMLParser.HTMLParser):
    startData = False
    lineScore = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for att in attrs:
                if att[0] == 'colspan' and att[1] == '4':
                    for att in attrs:
                        if att[0] == 'class' and att[1] == 'padding_top':
                            self.startData = True
    def handle_endtag(self, tag):
        if tag == 'td' and self.startData == True:
            self.startData = False
            return self.lineScore
    def handle_data(self, data):
        if self.startData == True:
            self.lineScore += data
       

