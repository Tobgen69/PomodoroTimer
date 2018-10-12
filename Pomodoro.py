"""
Pomodoro Timer, by Tobias Genz, 12.10.2018

This little application is supposed to be a very simple Pomodoro Timer. 
However it is primarily a project to learn (object oriented) programming and therefore the final product is not most important.
If possible I will add functionality gradually such as:
- Short/Long Break
- Pause Button
- Counter for Pomodor Cycle
- adjustable times
- Store Cycles into an database (probably SQLite)
- Add Comments to the cycles
- make more appealing GUI
- ...

"""
import tkinter as tk
from datetime import datetime, date, timedelta
import winsound # for the beep sound

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

        tk.Label(self, text = "Pomodoro Time in minutes:").pack()
        self.PomoTimer = tk.StringVar() # initialize variable to display
        self.PomoTimer.set('waiting...') # set default value if no update happend
        tk.Label(self, textvariable = self.PomoTimer).pack()

        tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).pack() # create exit button
        tk.Button(self, text='Start Countdown', command=self.CountdownButton).pack() # create CountdownButton

        # Default attributes: // instead of global variables, no global because shall be possible to change
        self.pomo_run = 0.1*60
        self.pomo_small = 0.05*60
        self.pomo_big = 0.075*60
        self.pomo_counter = 0

      
    def CountdownRun(self, t_end):
        """
        The main countdown method which updates the countdown by using the datetime.
        """

        t_current = datetime.now()
        t_delta = t_end - t_current
        t_delta_display = str(t_delta)[:-4] # to omit the 3rd to 6th second decimal

        if t_delta.total_seconds()>=0:  
            self.PomoTimer.set(t_delta_display)
            self.after(100, self.CountdownRun, t_end) # the .after of tkinter can take additional arguments for the function which is to call
        else: 
            t_delta_display = str(timedelta(seconds = 0))[:-4] # set timer to 0, otherwise it is negative
            self.pomo_counter += 1
            self.PomoTimer.set(t_delta_display)
            self.beep()       

    def CountdownButton(self):  
        """
        Used to initialize the time value when the button is hit. 
        Afterwards the Countdown Run method is called which has the self.after loop to always update the visible values in the window.
        """

        t_start = datetime.now() # set current datetime as start time
        if self.pomo_counter%2 == 0:
            runtime_period = self.pomo_run # run normal pomodoro
        elif self.pomo_counter%7 ==0:
            runtime_period = self.pomo_big
        elif (self.pomo_counter+1)%2 == 0:
            runtime_period = self.pomo_small
        else:
            print('Something is wrong') # better: some proper exception handling
            
        t_end = datetime.now() + timedelta(seconds = runtime_period)
        t_delta = t_end - t_start 
        t_delta_display = str(t_delta)

        self.PomoTimer.set(t_delta_display)
        self.CountdownRun(t_end)

    def beep(self):
        """ 
        Makes a sound. Used to make sound when Pomodoro is finished.
        """
        winsound.MessageBeep()    

root = tk.Tk() # initialize main tk-window of an application
root.wm_title('Pomodoro Timer by Tobias Genz') # set title
app = Application(master=root) # initialize app object

root.mainloop()