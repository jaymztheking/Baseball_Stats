from Retro import RSLog
import time


start = time.time()
x = RSLog('.\\Play by Play Logs\\2017\\2017MIA.EVN')
x.ParseLog()
end = time.time()
print(end-start)


