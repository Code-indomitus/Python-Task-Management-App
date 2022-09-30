from email import message
import math
from msilib.schema import ComboBox
from queue import Empty
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3

cardStorage = [] # stores tasks as cards
newCardList = [] # card list for the 

def create_task_window(root):
    
    # connect to database during start
    connect_db = sqlite3.connect('tasks.db')
    
    # create cusror
    cursor = connect_db.cursor()
        
    # create table "tasks" in same dir if it does not exist locally
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks
                    ([task_name], [task_description], [story_points], [priority], [status], [assigned_to], [tag], [id])
                    ''')

    # create master window
    requiredRow = 9
    requiredCol = 6
    
    taskWindow = Toplevel(root, width = 1000, height = 600)

    # Shyam
    createTaskButton = Button(taskWindow, text = "Create New Task")
    filterLabel = Label(taskWindow ,text = "Filter: ") 
    current_tag = StringVar()
    tags = Combobox(taskWindow, textvariable = current_tag)

    tags['values'] = ('ALL','UI', 'CORE', 'TESTING')
    tags['state'] = 'readonly'
    tags.current(0)
    
    filterButton = Button(taskWindow, text = "FILTER", command = lambda: filter(tags.get()))
    # create spacing in grid for C1 and C6
    spaceStart = Frame(taskWindow, width=50, height=50)
    spaceEnd = Frame(taskWindow, width=50, height=50)
    spaceStart.grid(row = 3, column = 1, padx = 3, pady = 3, sticky = "nw")
    spaceEnd.grid(row = 3, column = 6, padx = 3, pady = 3, sticky = "ne")
    
    # space window out if no cards
    # if cardStorage == []:
    #     # add spaces
    #     Label(taskWindow, width = 50, bg = "red", anchor = RIGHT).grid(row = 2, column = 3, columnspan = 4, sticky =)

    # place buttons within main window
    startRow, startCol, spanRow, spanCol = 2, 5, 1, 1 # tags
    tags.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 4, 1, 1 # filter:
    filterLabel.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 3, 1, 1, 5 # filter button:
    filterButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e", padx = 10)
    startRow, startCol, spanRow, spanCol = 2, 2, 1, 2 # create task button
    createTaskButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "w")
    
    # create "Sprint Master" label
    taskWindowTitle = Label(taskWindow, text = "Task Manager", bd = 5, padx = 3, pady = 3)
    startRow, startCol, spanRow, spanCol = 1, 1, 1, 6
    taskWindowTitle.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol)
    
    # display all cards
    # display(taskWindow, cardStorage)
    
    # run   
    taskWindow.mainloop()
    
# create card to represent a task in display
def create_task_card(window, cardStorage, taskNumber, 
                     DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag):
    # main frame for card
    mainFrame = Frame(window, width=280, height=200, highlightbackground="gray", highlightthickness=2)
    # card split into 9Rx8C; cells evenly sized
    for i in range(1, 8): #R1-R8
        mainFrame.grid_rowconfigure(i, weight=1, uniform = "cardrows")
    for i in range(2, 9-1): #C2-C8
        mainFrame.grid_columnconfigure(i, weight = 1, uniform = "cardcolumns")
    mainFrame.grid_propagate(0) # stop auto resize
    
    # print fields and buttons for card
    cardNum = Label(mainFrame, text = "Task ", font=("Arial", 10, "bold"))
    cardEditTask = Button(mainFrame, text = "Edit", font=("Courier", 8))
    cardDelete = Button(mainFrame, text = "X", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF")
    cardDescName = Label(mainFrame, text = "Name: ", font=("Arial" ,8, "bold"))
    cardDescPriority = Label(mainFrame, text = "Priority: ", font=("Arial" ,8, "bold"))
    cardDescPoints = Label(mainFrame, text = "Story Points: ", font=("Arial" ,8, "bold"))
    cardDescTag = Label(mainFrame, text = "Tag: ", font=("Arial" ,8, "bold"))
    
    # print variable data from database
    variableCardNum = Label(mainFrame, text = taskNumber, font=("Arial" , 10, "bold"))        
    variableDescName = Label(mainFrame, text = DescName)
    variableDescPriority = Label(mainFrame, text = DescPriority)
    variableDescPoints = Label(mainFrame, text = DescPoints)
    variableDescTag = Label(mainFrame, text = DescTag)
    
    # position of fields and buttons within card
    frontSpace = Label(mainFrame, width=200, height=1, bg = "gray") # coloured status bar
    if DescStatus == "Not Started":
        frontSpace.config(fg = "#000000", bg = "#FF0000", text = "Not started")
    elif DescStatus == "In Progress":
        frontSpace.config(fg = "#000000", bg = "#FFD800", text = "In Progress")
    elif DescStatus == "Complete":
        frontSpace.config(fg = "#000000", bg = "#3AFF00", text = "Complete")
    frontSpace.grid(row = 2, column = 1, columnspan = 8, padx = 3, pady = 1)
    
    priorityBox = Label(mainFrame, width=2, height=1, bg = "gray", highlightbackground="black", highlightthickness=1) # coloured priority box
    if DescPriority == "Low":
        priorityBox.config(bg = "#FFD800")
    elif DescPriority == "Medium":
        priorityBox.config(bg = "#FFD800")
    elif DescPriority == "High":
        priorityBox.config(bg = "#3AFF00")
    elif DescPriority == "Critical":
        priorityBox.config(text = "!", font=("Arial" , 9, "bold"),
                           fg = "#FF0000", bg = "#FFFFFF", highlightbackground="red", highlightthickness=1)
    priorityBox.grid(row = 1, column = 6, padx = 3, pady = 3)
    
    cardNum.grid(row = 1, column = 2, columnspan = 1, padx = 2, pady = 2, sticky = "w")
    cardEditTask.grid(row = 1, column = 7, padx = 2, pady = 2, sticky = "e")
    cardDelete.grid(row = 1, column = 8, padx = 2, pady = 2, sticky = "w")
    cardDescName.grid(row = 3, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPriority.grid(row = 4, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPoints.grid(row = 5, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescTag.grid(row = 6, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    
    # position of variables within card
    variableCardNum.grid(row = 1, column = 3, columnspan = 1, padx = 2, pady = 2, sticky = "w")
    variableDescName.grid(row = 3, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescPriority.grid(row = 4, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescPoints.grid(row = 5, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescTag.grid(row = 6, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    
    # add card to array
    cardStorage.append(mainFrame)
    
# # place cards in grid
# def place_card(cardStorage):
    
        
def display(window, cardArray):
    # connect to database
    connect_db = sqlite3.connect("tasks.db")
    
    # create cusror
    cursor = connect_db.cursor()
        
    # select all data from table    
    cursor.execute("SELECT * from tasks")
    rows = cursor.fetchall()
    
    # [0]: task_name
    # [1]: task description
    # [2]: story_points
    # [3]: priority
    # [4]: status
    # [5]: assigned_to
    # [6]: tag
    # [7]: id

    for row in rows:
        DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag, taskNumber = row[0], row[1], row[3], row[2], row[4], row[5], row[6], row[7]
        create_task_card(window, cardArray, taskNumber, DescName, 
                         DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag)
    
    # display if cardArray not empty
    if cardStorage:
        currentRow = 4 # first card at R4, C2
        currentCol = 2
        for card in range(0,len(cardStorage)):
            # add column-wise first, then add row if insufficient space ([arbitrary]Rx4C)
            if currentCol == 6:
                currentCol = 2
                currentRow += 1
            cardStorage[card].grid(row = currentRow, column = currentCol, padx = 5, pady = 5, sticky = "s")
            currentCol += 1
        
    connect_db.commit
    connect_db.close()