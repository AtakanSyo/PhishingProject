import time
starttime = time.time()

x = 0

while True:
    print(x)
    time.sleep(20.0 - ((time.time() - starttime) % 20.0))
    x = x + 1