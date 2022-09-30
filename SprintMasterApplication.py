from email import message
import math
from msilib.schema import ComboBox
from queue import Empty
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
import sqlite3
from tasks import *
from task_sorting import *

MainWindow = None
TaskTab = None
SprintTab = None
TeamTab = None
cardStorage = [] # stores tasks as cards
newCardList = [] # card list for the 
sprintCardStorage = [] # card list for sprints
def main():
    
    # connect to database during start
    connect_db = sqlite3.connect('tasks.db')
    
    # create cusror
    cursor = connect_db.cursor()
        
    # create table "tasks" in same dir if it does not exist locally
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks
                    ([task_name], [task_description], [story_points], [priority], [status], [assigned_to], [tag], [id])
                    ''')
          
    # attributes

    # create master window
    requiredRow = 9
    requiredCol = 6
    mainWindow = init_main_window("Sprint Master", "2000x630", requiredRow, requiredCol)
    MainWindow = mainWindow
    
    # setup tabs
    notebook = ttk.Notebook(mainWindow)
    notebook.grid(pady = 15)

    task_tab = Frame(notebook, width = 2000, height = 630)
    sprint_tab = Frame(notebook, width = 2000, height = 630)
    team_tab = Frame(notebook, width = 2000, height = 630, bg = "purple")

    # task_tab.pack(fill = "both", expand = 1)
    task_tab.grid_rowconfigure(requiredRow, weight = 1)
    task_tab.grid_columnconfigure(requiredCol, weight = 1)

    sprint_tab.grid_rowconfigure(requiredRow, weight = 1)
    sprint_tab.grid_columnconfigure(requiredCol, weight = 1)
    # sprint_tab.pack(fill = "both", expand = 1)
    # team_tab.pack(fill = "both", expand = 1)

    global TaskTab
    global SprintTab
    global TeamTab

    TaskTab = task_tab
    SprintTab = sprint_tab
    TeamTab = team_tab

    # Task Board widgets
    createTaskButton = Button(task_tab, text = "Create New Task", command = createNewTaskWindow)
    filterLabel = Label(task_tab ,text = "Filter: ") 
    current_tag = StringVar()
    tags = Combobox(task_tab, textvariable = current_tag)

    tags['values'] = ('ALL','UI', 'CORE', 'TESTING')
    tags['state'] = 'readonly'
    tags.current(0)
    
    filterButton = Button(task_tab, text = "FILTER", command = lambda: filter(tags.get()))
    # create spacing in grid for C1 and C6
    spaceStart = Frame(task_tab, width=50, height=50)
    spaceEnd = Frame(task_tab, width=50, height=50)
    spaceStart.grid(row = 3, column = 1, padx = 3, pady = 3, sticky = "nw")
    spaceEnd.grid(row = 3, column = 6, padx = 3, pady = 3, sticky = "ne")

    # place buttons within main window
    startRow, startCol, spanRow, spanCol = 2, 5, 1, 1 # tags
    tags.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 4, 1, 1 # filter:
    filterLabel.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 3, 1, 1, 5 # filter button:
    filterButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e", padx = 10)
    startRow, startCol, spanRow, spanCol = 2, 2, 1, 2 # create task button
    createTaskButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "w")
    
    # Sprint Board widgets
    createSprintButton = Button(sprint_tab, text = "Create New Sprint", command = createNewSprintWindow)
    createSprintButton.place(x = 50, y = 20)

    # add tabs to the notebook
    notebook.add(task_tab, text = "Task Board")
    notebook.add(sprint_tab, text = "Sprint Board")
    notebook.add(team_tab, text = "Team Board")
    
    # display all task cards
    display(cardStorage)

    # display all sprint cards
    names, status, start, end = get_sprints_details()
    create_sprint_display(sprint_tab, names, status, start, end)
    
    # run   
    mainWindow.mainloop()

def get_sprints_details():
     # connect to database
    connect_db = sqlite3.connect("sprints.db")
    
    # create cusror
    cursor = connect_db.cursor()
        
    # select all data from table    
    cursor.execute("SELECT * from sprints")
    sprints = cursor.fetchall()
    
    sprintNames = []
    sprintStatus = []
    sprintStart = []
    sprintEnd = []
    
    # [0]: sprint_name
    # [1]: start_date
    # [2]: end_date
    # [3]: status
    
    for sprint in sprints:
        sprintNames.append(sprint[0])
        sprintStatus.append(sprint[3])
        sprintStart.append(sprint[1])
        sprintEnd.append(sprint[2])
        
    # print(sprintNames); print(sprintStatus)
    
    return sprintNames, sprintStatus, sprintStart, sprintEnd
def createNewSprintWindow():

    def createSprint():
        # Create/Connect to a database
        connect_db = sqlite3.connect('sprints.db')
        # Create cusror
        cursor = connect_db.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprints
                ([sprint_name], [start_date], [end_date], [status])
                ''')

        connect_db.execute("INSERT INTO sprints VALUES (:sprint_name, :start_date, :end_date, :status)", 
                        {
                            'sprint_name': sprint_name_entry.get(),
                            'start_date': start_date_entry.get_date().strftime("%m/%d/%Y"),
                            'end_date': end_date_entry.get_date().strftime("%m/%d/%Y"),
                            'status': 'Not started' # default status
                        }
                            )
        
        # Commit changes
        connect_db.commit()
        # Close Connnection
        connect_db.close()

        # Clear input boxes
        sprint_name_entry.delete(0, END)
        start_date_entry.delete(0, END)
        end_date_entry.delete(0, END)

        global sprintCardStorage

        for card in sprintCardStorage:
            card.destroy()
        
        sprintCardStorage = []
        names, status, start, end = get_sprints_details()

        create_sprint_display(SprintTab, names, status, start, end)


    # Toplevel object which will
    # be treated as a new window
    newSprintWindow = Toplevel(MainWindow)
 
    # sets the title of the
    # Toplevel widget
    newSprintWindow.title("New Sprint")
 
    # sets the geometry of toplevel
    newSprintWindow.geometry("400x400")


    frame = Frame(newSprintWindow, width = 400, height = 400)
    frame.pack()

    sprint_name = Label(frame, text = "Sprint Name:")
    sprint_name.place(x = 20, y = 50)

    start_date = Label(frame, text = "Start Date:")
    start_date.place(x = 20, y = 90)

    end_date = Label(frame, text = "End Date:")
    end_date.place(x = 20, y = 140)

    sprint_name_entry = Entry(frame, width = 40)
    start_date_entry = DateEntry(frame,selectmode='day')  # Date entry allows user to get date input using a calendar. The date input is in datetime.date format/object
    end_date_entry = DateEntry(frame,selectmode='day')
    sprint_name_entry.place(x = 110, y = 50)
    start_date_entry.place(x = 110, y = 90)
    end_date_entry.place(x = 110, y = 140)

    createButton = Button(frame, text = "Create Sprint", command = createSprint)
    createButton.place(x = 110, y = 290)

    discardButton = Button(frame, text = "Discard Sprint", command = newSprintWindow.destroy)
    discardButton.place(x = 225, y = 290)

def createNewTaskWindow():

    def createTask():

        # Create/Connect to a database
        connect_db = sqlite3.connect('tasks.db')
        # Create cusror
        cursor = connect_db.cursor()
        
        # create table "tasks" in same dir if it does not exist locally
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tasks
                       ([task_name], [task_description], [story_points], [priority], [status], [assigned_to], [tag], [id])
                       ''')
        
        currentTaskNumber = len(cardStorage)+1 # create the card
        
        # input data
        connect_db.execute("INSERT INTO tasks VALUES (:task_name, :task_description, :story_points, :priority, :status, :assigned_to, :tag, :id)", 
                        {
                            'task_name': entry1.get(),
                            'task_description': entry2.get(),
                            'story_points': entry3.get(),
                            'priority': priority.get(),
                            'status': status.get(),
                            'assigned_to': assigned_to.get(),
                            'tag': tag.get(),
                            'id': currentTaskNumber
                        }
                       
                            )
        
        # show card immediately after task creation
        create_task_card(cardStorage, currentTaskNumber, 
                         entry1.get(), entry2.get(), priority.get(), entry3.get(), status.get(),assigned_to.get(), tag.get())
        
        currentRow = 4 + math.floor((len(cardStorage)-1)//4) # determine row and col to print
        currentCol = currentTaskNumber - (currentRow-4)*4 + 1
        
        cardStorage[-1].grid(row = currentRow, column = currentCol, padx = 5, pady = 5, sticky = "s") # print card
        
        # Commit changes
        connect_db.commit()
        # Close Connnection
        connect_db.close()

        # Clear input boxes
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        priority.set('')
        status.set('')
        assigned_to.set('')
        tag.set('')

    # Toplevel object which will
    # be treated as a new window
    newTaskWindow = Toplevel(MainWindow)
 
    # sets the title of the
    # Toplevel widget
    newTaskWindow.title("New Task")
 
    # sets the geometry of toplevel
    newTaskWindow.geometry("500x500")


    frame = Frame(newTaskWindow, width = 400, height = 400)
    frame.pack()

    task_name = Label(frame, text = "Task Name:")
    task_name.place(x = 20, y = 50)

    task_description = Label(frame, text = "Task Description:")
    task_description.place(x = 20, y = 80)

    task_story_points = Label(frame, text = "Story Points:")
    task_story_points.place(x = 20, y = 110)

    task_priority = Label(frame, text = "Priority:")
    task_priority.place(x = 20, y = 140)

    task_status = Label(frame, text = "Status:")
    task_status.place(x = 20, y = 170)

    task_assigned_to = Label(frame, text = "Assigned To:")
    task_assigned_to.place(x = 20, y = 200)

    task_tag = Label(frame, text = "Tag:")
    task_tag.place(x = 20, y = 230)


    entry1 = Entry(frame, width = 50)
    entry2 = Entry(frame, width = 50)
    entry3 = Entry(frame, width = 50)
    entry1.place(x = 140, y = 50)
    entry2.place(x = 140, y = 80)
    entry3.place(x = 140, y = 110)

    current_priority = StringVar()
    priority = Combobox(frame, textvariable = current_priority)
    priority['values'] = ('Low', 'Medium', 'High', 'Critical')
    priority['state'] = 'readonly'
    priority.current(0)
    priority.place(x = 140, y = 140)

    current_Status = StringVar()
    status = Combobox(frame, textvariable = current_Status)
    status['values'] = ('Not Started', 'In Progress', 'Complete')
    status['state'] = 'readonly'
    status.current(0)
    status.place(x = 140, y = 170)

    current_assigned_to = StringVar()
    assigned_to = Combobox(frame, textvariable = current_assigned_to)
    assigned_to['values'] = ('Chang Lin Ong', 'Lai Carson', 'Shyam Kamalesh Borkar', 'Tiong Yue Khoo')
    assigned_to['state'] = 'readonly'
    assigned_to.current(0)
    assigned_to.place(x = 140, y = 200)

    current_tag = StringVar()
    tag = Combobox(frame, textvariable = current_tag)
    tag['values'] = ('UI', 'CORE', 'TESTING')
    tag['state'] = 'readonly'
    tag.current(0)
    tag.place(x = 140, y = 230)

    createButton = Button(frame, text = "Create", command = createTask)
    createButton.place(x = 125, y = 350)

    discardButton = Button(frame, text = "Close", command = newTaskWindow.destroy)
    discardButton.place(x = 225, y = 350)
    
# initialise main window layout
def init_main_window(title, size, splitRow, splitCol):
    main = new_page(title,size)
    # breakdown window into cells in a grid (splitRow x splitCol)
    main.grid_rowconfigure(splitRow, weight = 1)
    main.grid_columnconfigure(splitCol, weight = 1)
    return main

# new page (window)
def new_page(title, size):
    newPage = Tk()
    newPage.title(title)
    newPage.geometry(size)
    return newPage
    
# add label and position it
def add_label(displayText):
    newLabel = Label(MainWindow, text = displayText, bd = 5, padx = 3, pady = 3)
    return newLabel

# create card to represent a task in display
def create_task_card(cardStorage, taskNumber, 
                     DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag):
    global TaskTab
    # main frame for card
    mainFrame = Frame(TaskTab, width=280, height=200, highlightbackground="gray", highlightthickness=2)
    # card split into 9Rx8C; cells evenly sized
    for i in range(1, 8): #R1-R8
        mainFrame.grid_rowconfigure(i, weight=1, uniform = "cardrows")
    for i in range(2, 9-1): #C2-C8
        mainFrame.grid_columnconfigure(i, weight = 1, uniform = "cardcolumns")
    mainFrame.grid_propagate(0) # stop auto resize
    
    # print fields and buttons for card
    cardNum = Label(mainFrame, text = "Task ", font=("Arial", 10, "bold"))
    cardEditTask = Button(mainFrame, text = "Edit", font=("Courier", 8), command = lambda: editTask(taskNumber))
    cardDelete = Button(mainFrame, text = "X", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF", command = lambda: delete(mainFrame, taskNumber))
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
    
# place cards in grid
def place_card(cardStorage):
    currentRow = 4 # first card at R4, C2
    currentCol = 2
    for card in range(0,len(cardStorage)):
        # add column-wise first, then add row if insufficient space ([arbitrary]Rx4C)
        if currentCol == 6:
            currentCol = 2
            currentRow += 1
        cardStorage[card].grid(row = currentRow, column = currentCol, padx = 5, pady = 5, sticky = "s")
        currentCol += 1
        
def display(cardArray):
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
        create_task_card(cardArray, taskNumber, DescName, 
                         DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag)
    
    # display if cardArray not empty
    if cardArray:
        place_card(cardArray)
        
    connect_db.commit
    connect_db.close()

def create_sprint_display(mainSprintWindow, sprintNames, sprintStatus, sprintStart, sprintEnd):
    
    # main frame with all sprints and their status displayed
    mainDisplay = Frame(mainSprintWindow, width=300, height=300)
    mainDisplay.place(x = 10, y = 100)
    global sprintCardStorage
    sprintCardStorage.append(mainDisplay)
    
    # grid configure
    mainDisplay.grid_rowconfigure(5, weight = 1)
    mainDisplay.grid_columnconfigure(6, weight = 1)
    
    # border spacing
    Label(mainDisplay, width = 5).grid(row = 0, column = 0)
    Label(mainDisplay, width = 5).grid(row = 0, column = 6)
    
    row = 1 
    col = 1
        
    for i in range(len(sprintNames)):
        
        if col > 5:
            #Label(mainDisplay, text = "ROWSPACE", font=("Arial" ,8, "bold"), bg = "#FF0000" ,width = 10, height = 2).grid(
            #row = row + 2, column = 0, columnspan = 6)
            row += 3
            col = 1
            
        if sprintStatus[i] == "Not started":
            colour = "#D80000"
        if sprintStatus[i] == "In progress":
            colour = "#FFEC00"
        elif sprintStatus[i] == "Complete":
            colour = "#4CFF00"
        
        # frame for a sprint
        sprintFrame = Frame(mainDisplay, width=30, height=40, 
                            highlightbackground = "black", highlightthickness=1)
        
        sprintFrame.grid_rowconfigure(6, weight = 1)
        sprintFrame.grid_columnconfigure(2, weight = 1)
        
        sprintFrame.grid(row = row, column = col, padx = 8, pady = (0, 15))
        
        sprintFrame.config(bg = "#FFFFFF")
        
        # sprint name
        curr = Label(sprintFrame, text = sprintNames[i], font=("Arial" ,8, "bold"), 
                     bg = colour, fg = "#000000", width = 30, justify=LEFT, anchor = "w")
        curr.grid(row = 1, column = 1, columnspan = 2, sticky = W)
        # sprint status
        curr = Label(sprintFrame, text = f"Status:         {sprintStatus[i]}", font=("Arial" ,8),
                     bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
        curr.grid(row = 2, column = 1, columnspan = 2, sticky = W)
        
        # start date
        curr = Label(sprintFrame, text = f"Start Date:   {sprintStart[i]}", font=("Arial" ,8),
                     bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
        curr.grid(row = 3, column = 1, columnspan = 2, sticky = W)
        
        # end date
        curr = Label(sprintFrame, text = f"Start Date:   {sprintEnd[i]}", font=("Arial" ,8),
                     bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
        curr.grid(row = 4, column = 1, columnspan = 2, sticky = W)
        
        # details button
        detailsButton = Button(sprintFrame, text = "Details", anchor = E, font=("Arial" ,8, "bold")
                            , command = lambda: init_tasks_for_sprint(MainWindow))
        detailsButton.grid(row = 5, column = 1, pady = 5, sticky = E)
        
        # edit button
        editButton = Button(sprintFrame, text = "Edit", anchor = W, font=("Arial" ,8, "bold")
                            , command = lambda: init_swap(MainWindow))
        editButton.grid(row = 5, column = 2, pady = 5, sticky = W)

        col += 1

def editTask(taskNumber):
    #create a new window
    newWindow = Toplevel(MainWindow)
    newWindow.geometry("300x300")
    newWindow.title("edit task")
    
    #connect to database
    sqliteConnection = sqlite3.connect('tasks.db')
    #connect to cursor
    cursor = sqliteConnection.cursor()

    #Select a single row from SQLite table
    sqlite_select_query = """SELECT * from tasks where id = ?"""
    cursor.execute(sqlite_select_query, (taskNumber,))
    record = cursor.fetchone()

    #assign all variable to StringVar()
    DescName = StringVar()
    DescDesc = StringVar()
    DescPoints = StringVar()
    DescPriority = StringVar()
    DescStatus = StringVar()
    DescAssign = StringVar()
    DescTag = StringVar()

    #put data into variable
    DescName.set(record[0])
    DescDesc.set(record[1])
    DescPoints.set(record[2])
    DescPriority.set(record[3])
    DescStatus.set(record[4])
    DescAssign.set(record[5])
    DescTag.set(record[6])

    #making label
    editName = Label(newWindow, text = "Name")
    editDesc = Label(newWindow, text = "Description")
    editPoints = Label(newWindow, text = "Story Point")
    editPriority = Label(newWindow, text = "Priority")
    editStatus = Label(newWindow, text = "Status")
    editAssign = Label(newWindow, text = "Assigned To")
    editTag = Label(newWindow, text = "Tag")

    editName.grid(row = 1, column = 0, sticky = "w", pady = 2)
    editDesc.grid(row = 2, column = 0, sticky = "w", pady = 2)
    editPoints.grid(row = 3, column = 0, sticky = "w", pady = 2)
    editPriority.grid(row = 4, column = 0, sticky = "w", pady = 2)
    editStatus.grid(row = 5, column = 0, sticky = "w", pady = 2)
    editAssign.grid(row = 6, column = 0, sticky = "w", pady = 2)
    editTag.grid(row = 7, column = 0, sticky = "w", pady = 2)

    entry1 = Entry(newWindow,  textvariable = DescName)
    entry2 = Entry(newWindow,  textvariable = DescDesc)
    entry3 = Entry(newWindow,  textvariable = DescPoints)
    entry4 = Combobox(newWindow,  textvariable = DescPriority)
    entry5 = Combobox(newWindow,  textvariable = DescStatus)
    entry6 = Combobox(newWindow,  textvariable = DescAssign)
    entry7 = Combobox(newWindow,  textvariable = DescTag)
    
    entry1.grid(row = 1, column = 1, pady=5, sticky = "w")
    entry2.grid(row = 2, column = 1, pady=5, sticky = "w")
    entry3.grid(row = 3, column = 1, pady=5, sticky = "w")
    entry4.grid(row = 4, column = 1, pady=5, sticky = "w")
    entry5.grid(row = 5, column = 1, pady=5, sticky = "w")
    entry6.grid(row = 6, column = 1, pady=5, sticky = "w")
    entry7.grid(row = 7, column = 1, pady=5, sticky = "w")

    entry4['values'] = ('Low', 'Medium', 'High', 'Critical')
    entry5['values'] = ('Not Started', 'In Progress', 'Complete')
    entry6['values'] = ('Chang Lin Ong', 'Lai Carson', 'Shyam Kamalesh Borkar', 'Tiong Yue Khoo')
    entry7['values'] = ('UI', 'CORE', 'TESTING')
    
    entry4['state'] = 'readonly'
    entry5['state'] = 'readonly'
    entry6['state'] = 'readonly'
    entry7['state'] = 'readonly'


    def update():
        #connect to database
        sqliteConnection = sqlite3.connect('tasks.db')
        #connect to cursor
        cursor = sqliteConnection.cursor()

        #update the selected row
        sql_update_query = "Update tasks set task_name = ?, task_description = ?, story_points = ?, priority = ?, status = ?, assigned_to = ?, tag = ? where id = ?"
        data = (str(entry1.get()), str(entry2.get()), int(entry3.get()), str(entry4.get()), str(entry5.get()), str(entry6.get()), str(entry7.get()), int(taskNumber))
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

        newWindow.destroy()
        global cardStorage
        for card in cardStorage:
            card.destroy()
        cardStorage = []
        display(cardStorage)

    
    editButton = Button(newWindow, text = "confirm", command = update)
    editButton.grid(row = 8, column = 2, pady=5, sticky = "w")

    editButton = Button(newWindow, text = "delete", command = lambda: delete(newWindow, taskNumber))
    editButton.grid(row = 8, column = 1, pady=5, sticky = "w")

    cursor.close()
    sqliteConnection.close()


def delete(mainFrame, taskNumber):
    #delete card
    mainFrame.destroy()

    #connect database
    sqliteConnection = sqlite3.connect('tasks.db')
    #connect cursor
    cursor = sqliteConnection.cursor()

    #delete selected row
    sql_update_query = """DELETE from tasks where id = ?"""
    cursor.execute(sql_update_query, (taskNumber,))
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()

    global cardStorage
    for card in cardStorage:
        card.destroy()
    cardStorage = []
    display(cardStorage)

def filter(tag):
    global cardStorage
    global newCardList
    if tag == 'ALL':
        for card in cardStorage:
            card.destroy()
        for card in newCardList:
            card.destroy()
        cardStorage = []
        display(cardStorage) 
        return

    for card in cardStorage:
        card.destroy()
    for card in newCardList:
        card.destroy()
    newCardList = []
    displayFilter(newCardList, tag)

def displayFilter(cardArray, tag):
    # connect to database
    connect_db = sqlite3.connect("tasks.db")
    
    # create cusror
    cursor = connect_db.cursor()
        
    # select all data from table according to the tag
    
    sql_filter_query = """SELECT * from tasks where tag = ?"""   
    cursor.execute(sql_filter_query, (tag,))
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
        create_task_card(cardArray, taskNumber, DescName, 
                         DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag)
    
    # display if cardArray not empty
    if cardArray:
        place_card(cardArray)
        
    connect_db.commit
    connect_db.close()
   #('ALL','UI', 'CORE', 'TESTING') 

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
    
main()
