from Retro import RSLog
import time, os

'''
start = time.time()
print(time.strftime('%I:%M:%S %p', time.localtime(start)))
year = 2017
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	x = RSLog('.\\Play by Play Logs\\2017\\'+file[1])
	x.ParseLog()
	print(time.strftime('%I:%M:%S %p', time.localtime(time.time())))
'''

x = RSLog('.\\Play by Play Logs\\2017\\2017COL.EVN')
y = x.ParseLog()
x = y[3]['COL201709250']['arenn001']
play = y[2]['COL201709250']
print(x.plate_app, x.at_bat, x.runs)






