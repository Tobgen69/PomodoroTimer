from datetime import datetime, date, timedelta 
import sqlite3
from time import mktime # needed for appropriate unix timestamp creation


date_test = datetime.now()

#dt = datetime.datetime(2010, 2, 25, 23, 23)
unix = mktime(date_test.timetuple())
date = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

