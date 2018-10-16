"""
author: Tobias Genz
date: 16.10.2018
For initially setting up the database
"""

import sqlite3


conn = sqlite3.connect('Pomodoro.db') # if it doesn't exist, SQLite will create this file/db
c = conn.cursor() # defines the cursor, which is the "thing" that does all the stuff (executions etc.)

def create_table(): # good practice is to capitalize SQL-keywords and keep the own input (tablenames, fieldnames) smallcap
    c.execute('CREATE TABLE IF NOT EXISTS pomodoroRuns(unix REAL, datestamp TEXT, type TEXT, pomo_run INT, pomo_small INT, pomo_big INT)')
    #(fieldname DATATYPE, ...)
    # don't need an autoincrement id, as the "rowid" is automatically included as primary key integer

def _manual_data_entry():
    c.execute("INSERT INTO pomodoroRuns VALUES(4129847214, '2018-01-01', 'Start Pomodoro', 1500, 300, 900)") # insert data
    conn.commit() # commit the transaction
    c.close() # close the data
    conn.close() # close the connection to the database #

create_table()


def insert_pomo_actions(pomo_date ,type = 'Default'):
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    type = 'Test for Pomos'
    c.execute("INSERT INTO pomodoroRuns (unix, datestamp, type) VALUES (?, ?, ?)", (unix, date, type))
    conn.commit()


