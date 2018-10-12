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


    #pass 

# region old window defs
    # tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
    #          text='Local Time').grid(row=0, column=0) # create label with simple text
    # self.LocalDate = tk.StringVar() # initialize textvariable for later use
    # self.LocalDate.set('waiting...') # set text variable "default" value
    # tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
    #          textvariable=self.LocalDate).grid(row=0, column=1) # create label to display the LocalDate

    # tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
    #          text='Local Date').grid(row=1, column=0) # label for Local Date
    # self.LocalTime = tk.StringVar() # init variable for localtime
    # self.LocalTime.set('waiting...') # set default localtime
    # tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
    #          textvariable=self.LocalTime).grid(row=1, column=1) 

    # tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
    #          text='GMT Time').grid(row=2, column=0)
    # self.nowGdate = tk.StringVar()
    # self.nowGdate.set('waiting...')
    # tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
    #          textvariable=self.nowGdate).grid(row=2, column=1)

    # tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
    #          text='GMT Date').grid(row=3, column=0)
    # self.nowGtime = tk.StringVar()
    # self.nowGtime.set('waiting...')
    # tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
    #          textvariable=self.nowGtime).grid(row=3, column=1)
#endregion old window defs
    
    
    #self.gettime() # always run gettime after finishing the button/label definitions
# region old gettime def
#     def gettime(self):
#     gdt, gtm, ldt, ltm = GetDateTime() # get current date time variables etc.
#     gdt = gdt[0:4] + '/' + gdt[4:6] + '/' + gdt[6:8]
#     gtm = gtm[0:2] + ':' + gtm[2:4] + ':' + gtm[4:6] + ' Z'  
#     ldt = ldt[0:4] + '/' + ldt[4:6] + '/' + ldt[6:8]
#     ltm = ltm[0:2] + ':' + ltm[2:4] + ':' + ltm[4:6]  
#     self.nowGtime.set(gdt) # set variables which are used in the labels of tkinter (textvariable)
#     self.nowGdate.set(gtm) # set variables which are used in the labels of tkinter (textvariable)
#     self.LocalTime.set(ldt) # set variables which are used in the labels of tkinter (textvariable)
#     self.LocalDate.set(ltm) # set variables which are used in the labels of tkinter (textvariable)

#     self.after(10000, self.gettime) # rerun the gettime method after .1 seconds 
#    #print (ltm)  # Prove it is running this and the external code, too.
#   pass
#endregion old gettime def
    

root = tk.Tk() # initialize main tk-window of an application
root.wm_title('Pomodoro Timer') # set title
app = Application(master=root) # initialize app object

# region other stuff old
# w = 200 # width for the Tk root
# h = 125 # height for the Tk root

# # get display screen width and height
# ws = root.winfo_screenwidth()  # width of the screen
# hs = root.winfo_screenheight() # height of the screen

# # calculate x and y coordinates for positioning the Tk root window

# #centered
# #x = (ws/2) - (w/2)
# #y = (hs/2) - (h/2)

# #right bottom corner (misfires in Win10 putting it too low. OK in Ubuntu)
# x = ws - w
# y = hs - h - 35  # -35 fixes it, more or less, for Win10

# #set the dimensions of the screen and where it is placed
# root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#endregion other stuff old

root.mainloop()