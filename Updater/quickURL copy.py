from datetime import datetime
import time

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

print(current_time)

while(True):
	if(current_time[3] == '0' and current_time[4] == '0'):
		print("new hour")
		print(current_time)
	print("sleeping")
	time.sleep(50)

