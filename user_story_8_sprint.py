from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3
from SprintMasterApplication import *

def init_tasks_for_sprint(root):
    ''' Initialises the tasks for a particular sprint, sorted according to progress status'''
    # create top level window for task display
    sprintTasksDisplay = Toplevel(root, height=400, width=800)
    
    # set up grid
    sprintTasksDisplay.grid_rowconfigure(4, weight = 1)
    sprintTasksDisplay.grid_columnconfigure(6, weight = 1)
    
    # window title
    title = Label(sprintTasksDisplay, text = "'Sprint Title' Board", anchor = CENTER)
    title.grid(row = 1, column = 1, columnspan = 5, pady = (15,20))
    
    # spacing
    Label(sprintTasksDisplay, bg = "#DA1B1B", width = 26).grid(row = 2, column = 1)
    Label(sprintTasksDisplay, bg = "#DA1B1B", width = 26).grid(row = 2, column = 5)
    
    # labels for table
    notStartedLabel = Label(sprintTasksDisplay, text = "Not started", font = ("Arial" ,8, "bold"),
                            bg = "#EB8989", fg = "#DA1B1B", highlightbackground = "#DA1B1B", highlightthickness = 2,
                            anchor = CENTER, width = 40)
    notStartedLabel.grid(row = 2, column = 2, sticky = "s", padx = 1)
    
    inProgressLabel = Label(sprintTasksDisplay, text = "In progress", font = ("Arial" ,8, "bold"),
                            bg = "#FFECB5", fg = "#FFAE00", highlightbackground = "#FFAE00", highlightthickness = 2,
                            anchor = CENTER, width = 40)
    inProgressLabel.grid(row = 2, column = 3, sticky = "s", padx = 1)
    
    completeLabel = Label(sprintTasksDisplay, text = "Complete", font = ("Arial" ,8, "bold"),
                            bg = "#BBFC9D", fg = "#287F00", highlightbackground = "#287F00", highlightthickness = 2,
                            anchor = CENTER, width = 40)
    completeLabel.grid(row = 2, column = 4, sticky = "s", padx = 1)
    
    # boxes to place cards
    notStartedFrame = Frame(sprintTasksDisplay, bg = "#FFFFFF", highlightbackground = "#DA1B1B", highlightthickness = 2,
                            height = 300, width = 40)
    notStartedFrame.grid(row = 3, column = 2, sticky = N+S+E+W, padx = 1)
    
    inProgressFrame = Frame(sprintTasksDisplay, bg = "#FFFFFF", highlightbackground = "#FFAE00", highlightthickness = 2,
                            height = 300, width = 40)
    inProgressFrame.grid(row = 3, column = 3, sticky = N+S+E+W, padx = 1)
    
    completeFrame = Frame(sprintTasksDisplay, bg = "#FFFFFF", highlightbackground = "#287F00", highlightthickness = 2,
                            height = 300, width = 40)
    completeFrame.grid(row = 3, column = 4, sticky = N+S+E+W, padx = 1)
    
    # scroll = Scrollbar(sprintTasksDisplay)
    # scroll.grid(row = 2, column = 6, rowspan = 3, sticky = "ne")
    
root = Tk()
root.geometry("1200x600")
root.title("Main")

button = Button(text = "More", command= lambda:init_tasks_for_sprint(root))
button.place(x=20, y=20)
   
root.mainloop()