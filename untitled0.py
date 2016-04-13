x = 'SB2;SBH'

if re.search('SB[23H]', x) != None:
    if 'SB2' in x:
        print('Stole 2nd')
    if 'SB3' in x:
        print('Stole 3rd')
    if 'SBH' in x:
        print('Stole Home')