""" for testing with time libarary"""

import time
from datetime import datetime, date, timedelta

t_start = datetime.now()
print(t_start)

time.sleep(1)

t_end = datetime.now()
print(t_end)

delta = t_end - t_start
print(str(delta))

print(t_start + timedelta(seconds=60*25))


# t_start = time.localtime()
# time.sleep(10)
# t_2 = time.localtime()
# print(t_2 - t_start)

# print(time.strftime("%Y%m%d", time.localtime()))
# print(time.strftime("%H%M%S", time.localtime()))