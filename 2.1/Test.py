from GameSim import *
from Retro import InfoRow

x = GameSim()
test = 'info,starttime,6:42PM'
row = InfoRow('ABC20170101', test.split(','), 1)
print(x.read_info_row_data(row))
