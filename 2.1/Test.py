from GameSim import GameSim
from Retro import InfoRow, SubRow, PlayRow
from Baseball import Base, Play, HitBoxScore, PitchBoxScore
from RetroPlayConverter import get_rs_play, get_rs_run_seq, get_rs_ball_type
from datetime import date

'''
rowcount = 0
file = '.\\Play by Play Logs\\2017AAA.EVN'
text = open(file, 'r')
for line in text:
	row = line.strip('\n').split(',')
	rowtype = row[0]
	rowcount += 1
	if rowtype == 'id':
		currentgame = row[1]
		x = GameSim(currentgame)
	elif rowtype == 'info':
		x.read_info_row_data(InfoRow(currentgame, row, rowcount))
	elif rowtype == 'start':
		x.add_lineup(SubRow(currentgame, row, rowcount))
	elif rowtype == 'play':
		x.read_play_row_data(PlayRow(currentgame, row, rowcount))
print(x.activehomepitcher, x.activeawaypitcher)
'''

sim = GameSim('ABC201701010')
lineup = {'joe001': HitBoxScore(), 'chris001': HitBoxScore(), 'sue001': HitBoxScore()}
roster = {'dave001': PitchBoxScore()}
sim.batter = 'joe001'
sim.first_base = 'sue001'
sim.second_base = ''
sim.third_base = 'chris001'
testrow = PlayRow(sim.currentgame.game_id, 'play,1,0,bob001,00,BCBBX,S9/F.3-H;1#2'.split(','), 1)
testbase = Base(sim, testrow)
testplay = Play(sim, testrow)

testplay.play_type = get_rs_play(testplay.play_seq)
testplay.classify_play()
testplay.ball_loc, testplay.ball_type = get_rs_ball_type(testplay.play_seq.split('.')[0])
testbase.run_seq = get_rs_run_seq(testbase.run_seq, testplay.play_seq, testplay.play_type, sim)
sim.move_runners(testbase.run_seq)
testbase.calc_end_play_stats(sim)
testbase.figure_out_rbi(testplay.play_type)
lineup['joe001'].increment_from_play(testplay, testbase)
baserunners = {testbase.start_first: 'first',
			   testbase.start_second: 'second',
			   testbase.start_third: 'third'}
for br in baserunners.keys():
	if br != '':
		lineup[br].increment_from_base(testbase, baserunners[br])
roster['dave001'].increment_from_play(testplay)
print(vars(testplay))
print(vars(roster['dave001']))