# PomodoroTimer
A little PomodoroTimer program built in Python with tkinter. 
The goal is to get in touch with object oriented programming and to provide a tool for myself which does perfectly fit my personal needs.
I will implement different new features step by step.

# Features:
The main focus yet is on functionality rather than design of the GUI (frontend wise). 
The main properties are:
- live displayed timer
- automatic pomodoro cycles (run, short break)*3 + run + long break
- Button to start the run
- Button for pausing

Later on I will add features for improve the user experience aswell as incorporate a small database to store the data and provide statistics etc.
Addtional features could be:
- Statistics about usage (how many runs, per day, at what times, ...) maybe display with some graphics
- adding a comment field after each run/cycle to add a comment or grade on how efficient the run felt like
- an autoplay mode which directly continues with the break after the run is done
- more and adjustable sounds for the alarm
- a reset button for the current run (if you got distracted)
- some gamification items and things like random motivational pushes within the breaks, maybe also things like levels/expercience etc.
- ... and possibly many more

After I am happy with the progress on the app as well as my learnings for the above mentioned parts I will continue to reimplement it, either as an web application or as an android app. Also recreating it more efficient with C or C# or so might be an option and then ofcourse creating a nice looking GUI would also be nice.

# Documentation on certain decisions and my learnings
I will try to justify my choice of design etc. and maybe document a few interesting insights.

## Choice of database
Basically I considered three options for the database implementation:
- SQLite
- MySQL
- PostgreSQL

While they are all free and frequently used, SQLite is as the name says the most lightweight one, so it stores the whole database (all tables...) in just one file, and doesn't demand any administrative work like creating users etc. Therefore I will use it to implement the database features.
