from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3
from SprintMasterApplication import *

def init_swap(root):
    ''' Initialises the tasks for a particular sprint, sorted according to progress status'''
    # create top level window for task display
    sprintTasksDisplay = Toplevel(root, height=400, width=800)
    
    rows = 4
    cols = 6
    
    # set up grid
    sprintTasksDisplay.grid_rowconfigure(rows, weight = 1)
    sprintTasksDisplay.grid_columnconfigure(cols, weight = 1)
    
    # window title
    # TODO: get title of sprint using database
    title = Label(sprintTasksDisplay, text = "Manage Sprint", anchor = CENTER)
    title.grid(row = 1, column = 1, columnspan = 5, pady = (15,20))
    
    # spacing
    Label(sprintTasksDisplay, width = 26).grid(row = 2, column = 1)
    Label(sprintTasksDisplay, width = 26).grid(row = 2, column = 5)
    Label(sprintTasksDisplay, width = 26).grid(row = 2, column = 3)
    
    # labels for table
    productBacklog = Label(sprintTasksDisplay, text = "Product Backlog", font = ("Arial" ,8, "bold"),
                            bg = "#82CCFF", fg = "#000000", highlightbackground = "#82CCFF", highlightthickness = 2,
                            anchor = CENTER, width = 40)
    productBacklog.grid(row = 2, column = 2, sticky = "s", padx = 1)
    
    sprintBacklog = Label(sprintTasksDisplay, text = "Sprint Backlog", font = ("Arial" ,8, "bold"),
                            bg = "#F6FF82", fg = "#000000", highlightbackground = "#F6FF82", highlightthickness = 2,
                            anchor = CENTER, width = 40)
    sprintBacklog.grid(row = 2, column = 4, sticky = "s", padx = 1)
    
    # boxes to place cards
    productBacklogFrame = Frame(sprintTasksDisplay, bg = "#FFFFFF", highlightbackground = "#82CCFF", highlightthickness = 2,
                            height = 300, width = 40)
    productBacklogFrame.grid(row = 3, column = 2, sticky = N+S+E+W, padx = 1)
    
    sprintBacklogFrame = Frame(sprintTasksDisplay, bg = "#FFFFFF", highlightbackground = "#F6FF82", highlightthickness = 2,
                            height = 300, width = 40)
    sprintBacklogFrame.grid(row = 3, column = 4, sticky = N+S+E+W, padx = 1)
    
    scroll = Scrollbar(sprintTasksDisplay)
    scroll.grid(row = 2, column = 6, rowspan = rows, sticky = "ne")
    
    # buttons
    # start
    startButton = Button(sprintTasksDisplay, text = " Get Started ", anchor = CENTER)
    startButton.grid(row = 4, column = 2, padx = 1, sticky = "e")
    
    # save and exit
    saveButton = Button(sprintTasksDisplay, text = " Save and Exit ", anchor = CENTER)
    saveButton.grid(row = 4, column = 4, padx = 1, sticky = "w")
    
# root = Tk()
# root.geometry("1200x600")
# root.title("Main")

# button = Button(text = "More", command= lambda:init_swap(root))
# button.place(x=20, y=20)
   
# root.mainloop()