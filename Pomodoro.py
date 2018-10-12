"""
Pomodoro Timer
"""
import tkinter as tk
from datetime import datetime, date, timedelta
import winsound # for the beep sound


# DEFINE GLOBAL VARIABLES
global POMO_DEFAULT 
POMO_DEFAULT = 0.1*60 # 25 minutes default pomodoro timer
global POMO_COUNTER 
POMO_COUNTER = 0


class Application(tk.Frame): # initialize a class to use later to create the application
    
    def __init__(self, master): # get's executed when new application object is initialized

    #fontsize = 12 # some basic parameter settings
    #textwidth = 9 # some basic parameter settings

        tk.Frame.__init__(self, master) # ?? sets up the frame and shows/packs it
        self.pack()

        tk.Label(self, text = "Pomodoro Time in minutes:").pack()
        self.PomoTimer = tk.StringVar() # initialize variable to display
        self.PomoTimer.set('waiting...') # set default value if no update happend
        tk.Label(self, textvariable = self.PomoTimer).pack()

        tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).pack() # create exit button
        tk.Button(self, text='Start Countdown', command=self.CountdownButton).pack() # create CountdownButton
      
    def CountdownRun(self):
        """
        The main countdown method which updates the countdown by using the datetime.
        """
        global T_END

        t_current = datetime.now()
        t_delta = T_END - t_current
        t_delta_display = str(t_delta)[:-4] # to omit the 3rd to 6th second decimal

        if t_delta.total_seconds()>=0:  
            self.PomoTimer.set(t_delta_display)
            self.after(100, self.CountdownRun)
        else: 
            t_delta_display = str(timedelta(seconds = 0))[:-4] # set timer to 0, otherwise it is negative
            self.PomoTimer.set(t_delta_display)
            self.beep()        

    def CountdownButton(self):  
        """
        Used to initialize the time value when the button is hit. 
        Afterwards the Countdown Run method is called which has the self.after loop to always update the visible values in the window.
        """
        global POMO_DEFAULT
        global T_END
        # need to incorporate the timer to safe the start date of initial countdown pressing and stop the recursion when t_start +POMO_COUNTER > t_current
        # somehow check if t_start was already set... but only set it the first time the button is pressed 
        # ... so maybe a second method... one which only runs once when the button is hit, and that one calls another which has the self.after recursion!
        # Thats it!!!
        t_start = datetime.now() # set current datetime as start time
        T_END = datetime.now() + timedelta(seconds = POMO_DEFAULT)
        t_delta = T_END - t_start 
        t_delta_display = str(t_delta)
        #POMO_COUNTER += 1
        self.PomoTimer.set(t_delta_display)
        self.CountdownRun()

    def beep(self):
        """ 
        Makes a sound. Used to make sound when Pomodoro is finished.
        """
        winsound.MessageBeep()    

root = tk.Tk() # initialize main tk-window of an application
root.wm_title('Pomodoro Timer') # set title
app = Application(master=root) # initialize app object

root.mainloop()