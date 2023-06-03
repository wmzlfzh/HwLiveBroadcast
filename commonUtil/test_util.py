import time

stamp =time.time()
yy = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))
print(yy)