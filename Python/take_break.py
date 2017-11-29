import webbrowser
import time 

breaks = 3
break_count = 0
print ("Program started on: " + time.ctime())
while(break_count < breaks):
	time.sleep(2*60*60)
	webbrowser.open('https://www.youtube.com/watch?v=NIS4P8xbPtg&list=RDNIS4P8xbPtg')
	break_count += 1