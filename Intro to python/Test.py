from datetime import date
import time

timestamp = time.time()
current_date = date.fromtimestamp(timestamp)
print(current_date) 

import calendar
print(calendar.month(1993, 9))