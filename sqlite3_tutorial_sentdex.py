"""
Author: Tobias Genz
Date: 16.10.2018
Goal of this file is to document my learnings on using SQLite3 for my Pomodoro application.
Therefore I for instance use sentdex videos as a source, but not exclusivly. I won't create versions
of this small tutorial, so I might change the script later on such that previous comments are obsolete.
Sentdex: https://www.youtube.com/watch?v=o-vsdfCBpsU


"""
#######################################################################################################################################################


""" Basic Documentation on SQLite:
SQLite is a really lightweight version of SQL which directly comes with Python. 
Unlike a full verison like MySQL, SQLite doesn't need you to setup a real server or any User or so. All tables and all data goes into one single file.
So if you only have very simple applications with not many parallel query's etc. probably you're good to go with SQLite.
However, there are several reasons why SQLite is way better than simply use plain files. 
"""


import sqlite3
import time     # imported later
import datetime # imported later

#first of all you need to define a connection and a cursor 

conn = sqlite3.connect('tutorial.db') # if it doesn't exist, SQLite will create this file/db
c = conn.cursor() # defines the cursor, which is the "thing" that does all the stuff (executions etc.)

def create_table(): # good practice is to capitalize SQL-keywords and keep the own input (tablenames, fieldnames) smallcap
    c.execute('CREATE TABLE IF NOT EXISTS pomodoroRuns(unix REAL, datestamp TEXT, type TEXT)')
    #(fieldname DATATYPE, ...)

def data_entry():
    c.execute("INSERT INTO pomodoroRuns VALUES(4129847214, '2018-01-01', 'Start Pomodoro')") # insert data
    conn.commit() # commit the transaction
    c.close() # close the data
    conn.close() # close the connection to the database #


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    type = 'Test for Pomos'
    c.execute("INSERT INTO pomodoroRuns (unix, datestamp, type) VALUES (?, ?, ?)", (unix, date, type))
    conn.commit()

    
create_table() # just want to run that once (even if with "Create table if not exists" recreating would be no problem)
#data_entry()    

for i in range(10):
    dynamic_data_entry()
    time.sleep(1) # to have the timestamp go up a second
c.close()
conn.close()


"""
To query the database we could just use simple command line 
... or use an extension for the editor (I use VisualStudioCode) or use the SQLite Browser.
Use the extension by "STRG+SHIFT+P" and type in SQLite ... then "Open database". 
I then got a SQLite Explorer on the left side (file overview etc.) 
We can look at the databses, tables, columns and see their types ecetera.
So far we entered data by manually typing that in... how can we input variables?
"""






