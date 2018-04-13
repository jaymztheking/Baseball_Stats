from Retro import RSLog
import time, os


start = time.time()
print(time.strftime('%I:%M:%S %p', time.localtime(start)))
year = 2017
for file in enumerate(os.listdir('.\\Play by Play Logs\\'+str(year))):
	print(file[1])
	x = RSLog('.\\Play by Play Logs\\2017\\'+file[1])
	x.ParseLog()
	print(time.strftime('%I:%M:%S %p', time.localtime(time.time())))





