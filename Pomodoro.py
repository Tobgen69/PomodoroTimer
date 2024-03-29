"""
Pomodoro Timer, by Tobias Genz, 12.10.2018

This little application is supposed to be a very simple Pomodoro Timer. 
However it is primarily a project to learn (object oriented) programming and therefore the final product is not most important.
If possible I will add functionality gradually such as:
- Short/Long Break - DONE
- Pause Button DONE
- Counter for Pomodor Cycle - semiDONE, add label in GUI DONE
- adjustable times DONE
- Store Cycles into an database (probably SQLite) DONE
- Add Comments to the cycles 
- make more appealing GUI
- ...

Some tkinter docs: 
https://www.tutorialspoint.com/python/python_gui_programming.htm
http://effbot.org/tkinterbook/


create executable with pyinstaller --noconsole Pomodoro.py --add-data ".\Success_sound.wav;." in cmd
whereby the ;. is used for the destination and .\Success_sound.wav is the source
"""

import tkinter as tk
#from tkinter import messagebox 
from datetime import datetime, date, timedelta
import winsound # for the beep sound
import sqlite3  # for saving data to a database
from time import mktime # needed for appropriate unix time..
from setup_sqldatabase import create_table # to setup the database table
from os import path # to check if database file exists

class Application(tk.Frame): # initialize a class to use later to create the application
    
    def __init__(self, master): 
        """
        Initializes the main parameters and graphical objects of tkinter. 
        The __init__ always gets called when a new class object is created.
        """
    #fontsize = 12 # some basic parameter settings
    #textwidth = 9 # some basic parameter settings

        tk.Frame.__init__(self, master) # ?? sets up the frame and shows/packs it
        self.pack()
        
        # Default attributes: // instead of global variables, no global because shall be possible to change
        self.pomo_run = 25*60  #/250 # /250 for testing purposes
        self.pomo_small = 5*60 #/250
        self.pomo_big = 15*60  #/250
        self.pomo_counter = 0

        self.pomos_finished = 0
        self.t_pause = False # initialize pause mode
        self.t_end = 0 # initialize t_end
        self.t_pause_start = 0
        self.t_pause_end = 0
        self.t_pause_duration = timedelta(seconds = 0) # initialize t_pause_start for safe time when pause was started
        self.active = False 
        self.runtime_period = 0
      
        tk.Label(self, text = "Pomodoro Time in minutes:", font=("Helvetica", 22)).pack()
        self.timer_display = tk.StringVar() # initialize variable to display
        self.timer_display.set('Start below') # set default value if no update happend
        tk.Label(self, textvariable = self.timer_display, font=("Helvetica", 128)).pack()
        self.pomo_c_display = tk.StringVar()
        self.pomo_c_display.set('Pomodoros done: ' + str(0))        
        tk.Label(self, textvariable = self.pomo_c_display, font=("Helvetica", 40)).pack()

        tk.Button(self, text='Start Countdown', command=self.CountdownButton).pack() # create CountdownButton
        tk.Button(self, text='Pause', command = self.pause).pack() # create PauseButton
        tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).pack() # create exit button

        #messagebox.showinfo("Welcome", "Click on \"Start Countdown\" to start the Pomodoro cycle. ") # tutorial mode, don't show why in dev

        # ENTRY FIELDS
        tk.Label(self, text = "Set Pomodoro runtime:(sec) ").pack(side = "top")
        self.pomo_run_custom = tk.StringVar(value = self.pomo_run)
        self.entry_pomo_run = tk.Entry(self, textvariable = self.pomo_run_custom).pack(side = "top")

        tk.Label(self, text = "Set small break runtime:(sec) ").pack(side = "top")
        self.pomo_small_custom = tk.StringVar(value = self.pomo_small)
        self.entry_pomo_small = tk.Entry(self, textvariable = self.pomo_small_custom).pack(side = "top")

        tk.Label(self, text = "Set big break runtime:(sec) ").pack(side = "top")
        self.pomo_big_custom = tk.StringVar(value = self.pomo_big)
        self.entry_pomo_big = tk.Entry(self, textvariable = self.pomo_big_custom).pack(side = "top")

        
      
    def CountdownRun(self):
        """
        The main countdown method which updates the countdown by using the datetime.
        """
        self.active = True # prevent to have several countdowns run in parallel (hidden)
        t_current = datetime.now()
        t_delta = self.t_end - t_current
        t_delta_display = str(t_delta)[:-7] # don't show decimal seconds

        if t_delta.total_seconds()>=0 and self.t_pause == False:  
            self.timer_display.set(t_delta_display)
            self.after(100, self.CountdownRun) # the .after of tkinter can take additional arguments for the function which is to call
        elif self.t_pause == True:
            pass
        else: 
            t_delta_display = str(timedelta(seconds = 0))[:-7] # set timer to 0, otherwise it is negative
            self.pomos_finished = 1 + int(self.pomo_counter/2) # can bet set to a label later to display in App # int floors doubles --> int(0.5)=0
            self.pomo_counter += 1            
            self.timer_display.set(t_delta_display)
            self.pomo_c_display.set('Pomodoros done: ' + str(self.pomos_finished))
            self.beep()
            insert_pomo_actions(self.t_end, 'End_Pomodoro', self.pomo_run, self.pomo_small, self.pomo_big) ## BAD DESIGN
            #print(self.pomos_finished)  ## $%& TESTING     
            self.active = False

    def CountdownButton(self):  
        """
        Used to initialize the time value when the button is hit. 
        Afterwards the Countdown Run method is called which has the self.after loop to always update the visible values in the window.
        """
        
        t_start = datetime.now() # set current datetime as start time
        self.pomo_run = int(self.pomo_run_custom.get())
        self.pomo_small = int(self.pomo_small_custom.get())
        self.pomo_big = int(self.pomo_big_custom.get())

        if self.pomo_counter%2 == 0 and self.active == False:            
            self.runtime_period = self.pomo_run # run normal pomodoro
            insert_pomo_actions(t_start, 'Start_Pomodoro_Run (Button)', self.pomo_run, self.pomo_small, self.pomo_big) ## BAD DESIGN
        elif self.pomo_counter%7 ==0 and self.active == False:
            self.runtime_period = self.pomo_big
            insert_pomo_actions(t_start, 'Start_Pomodoro_Big Break (Button)', self.pomo_run, self.pomo_small, self.pomo_big) ## BAD DESIGN
        elif (self.pomo_counter+1)%2 == 0 and self.active == False:
            self.runtime_period = self.pomo_small
            insert_pomo_actions(t_start, 'Start_Pomodoro_Small Break (Button)', self.pomo_run, self.pomo_small, self.pomo_big) ## BAD DESIGN
        elif self.active == True:
            print('already one countdown active, prevent to start another one')    
        else:
            print('Something is wrong with CountdownButton-Else') # better: some proper exception handling

        self.t_end = datetime.now() + timedelta(seconds = self.runtime_period)
        t_delta = self.t_end - t_start 
        t_delta_display = str(t_delta)

        self.timer_display.set(t_delta_display)
        if self.active == False:
            self.CountdownRun()
        else:
            pass

    def beep(self):
        """ 
        Makes a sound. Used to make sound when Pomodoro is finished.
        """   
        winsound.PlaySound("./Success_sound.wav",winsound.SND_ASYNC)

    def pause(self):
        """
        Makes it possible to pause/unpause the pomodoro or break.
        """ 
        if self.t_pause == False:
            self.t_pause = True
            self.t_pause_start = datetime.now()
        elif self.t_pause == True:
            self.t_pause = False
            self.t_pause_end = datetime.now()
            self.t_pause_duration = self.t_pause_end - self.t_pause_start
            self.t_end = self.t_end + self.t_pause_duration
            self.CountdownRun()
        else:
            print("something is wrong with Pause-Else")


#### Methods realted to saving the data into the database (possibly put out of this file?)
def insert_pomo_actions(ts, type = 'DEFAULT', p_run = 1500, p_small = 300, p_big = 900):
    unix = mktime(ts.timetuple())
    date = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    c.execute("""INSERT INTO pomodoroRuns (unix, datestamp, type, pomo_run, pomo_small, pomo_big ) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
            , (unix, date, type, p_run, p_small, p_big))
    #c.execute("INSERT INTO pomodoroRuns (unix, datestamp, type) VALUES (:unix, :date, :type)", 
    # {'unix':unix, 'date':date, 'type':type}) # more readable
    conn.commit()
       

root = tk.Tk() # initialize main tk-window of an application
root.wm_title('Pomodoro Timer by Tobias Genz') # set title
app = Application(master=root) # initialize app object

if path.exists("Pomodoro.db"):
    pass
else: 
    create_table()

conn = sqlite3.connect('Pomodoro.db') # if it doesn't exist, SQLite will create this file/db
c = conn.cursor() # defines the cursor, which is the "thing" that does all the stuff (executions etc.)

root.mainloop()

