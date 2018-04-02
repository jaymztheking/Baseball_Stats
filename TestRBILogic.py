test = ',FC5/G.3-H(E5/TH)(UR)(NR);2-H(UR)(NR);B-2'
test = test if test.find('.') == -1 else test[test.find('.')+1:]
test = test.strip().split(';')
noRBI = 0

for runner in test:
	if ('NR' in runner) or (('H' in runner) and ('TH' not in runner) and (('E' in runner) and 'MREV' not in runner)):
		noRBI +=1
		print(runner, noRBI)