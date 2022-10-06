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
from us9_team_board import *
import re
import time

MainWindow = None
TaskTab = None
SprintTab = None
TeamTab = None
SprintDisplay = None # Child frame of sprint tab for the better
memberDisplay = None # parent frame of member cards
cardStorage = [] # stores tasks as cards
newCardList = [] # card list for the 
sprintCardStorage = [] # card list for sprints
memberStorage = [] # stores members of a sprint

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
    notebook.grid(pady = 15, sticky = N+S+E+W)

    task_tab = Frame(notebook, width = 2000, height = 630, bg = "#FEE1E8")
    sprint_tab = Frame(notebook, width = 2000, height = 630, bg = "#DDF2FD")
    team_tab = Frame(notebook, width = 2000, height = 630, bg = "#ECE3FC")
    team_tab.grid(row = 0, column = 0, sticky = N+S+E+W)

    # task_tab.pack(fill = "both", expand = 1)
    task_tab.grid_rowconfigure(requiredRow, weight = 1)
    task_tab.grid_columnconfigure(requiredCol, weight = 1)

    sprint_tab.grid_rowconfigure(1, weight = 1)
    sprint_tab.grid_columnconfigure(3, weight = 1)
    
    team_tab.grid_rowconfigure(2, weight = 1)
    team_tab.grid_columnconfigure(1, weight = 1)
    
    # in sprint_tab: main frame with all sprints and their info displayed
    sprintDisplay = Frame(sprint_tab, width = 1200, height = 400, bg = "#DDF2FD")
    sprintDisplay.grid_rowconfigure(5, weight = 1)
    sprintDisplay.grid_columnconfigure(5, weight = 1)
    sprintDisplay.grid_propagate(False)
    sprintDisplay.grid(row = 1, column = 2, sticky = "", pady = (5,10))

    global SprintDisplay 
    SprintDisplay = sprintDisplay
    
    # border spacing for main frame
    Label(sprint_tab, width = 7).grid(row = 1, column = 1, sticky = W)
    Label(sprint_tab, width = 7).grid(row = 1, column = 3, sticky = E)

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
    spaceStart = Frame(task_tab, width=50, height=50, bg = "#FEE1E8")
    spaceEnd = Frame(task_tab, width=50, height=50, bg = "#FEE1E8")
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
    # connect to database
    connect_db = sqlite3.connect("sprints.db")
    
    # create cusror
    cursor = connect_db.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprints
                ([sprint_name], [start_date], [end_date], [status])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from sprints")
    sprints = cursor.fetchall()
    
    # [0]: sprint_name
    # [1]: start_date
    # [2]: end_date
    # [3]: status
    
    row = 1
    col = 1
    global sprintCardStorage
    
    # print each card
    for sprint in sprints:
        name = (sprint[0])
        status = (sprint[3])
        start = (sprint[1])
        end = (sprint[2])
        
        if col > 5:
            col = 1
            row += 1
    
        sprintCard = create_sprint_display(sprintDisplay, name, status, start, end)
        sprintCard.grid(row = row, column = col, sticky = "w", padx = (0,10), pady = (0,10))
        
        col += 1
        
    # Team Board widgets
    global memberDisplay
    memberDisplay = init_team_board(TeamTab)
    
    # printing each member of a sprint
    # connect to database
    connect_db = sqlite3.connect("members.db")
    
    # create cusror
    cursor = connect_db.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS members
                ([member_name], [member_email], [member_analytics])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from members")
    members = cursor.fetchall()
    
    # [0]: member_name
    # [1]: member_email
    # [2]: member_analytics
    
    row = 1
    col = 1
    
    global memberStorage
    
    # check if there are members
    if members == []:
            empty = Label(memberDisplay, text = "No members to show.", font = ("Roboto", 10),
                          bg = "white", fg = "black", height = 2,
                          highlightbackground = "black", highlightthickness = 1)
            empty.grid(row = 1, column = 1, columnspan = 4, sticky = E+W)
    else:
        # print each card
        for member in members:
            name = (member[0])
            email = (member[1])
            analytics = (member[2])
            end = (member[2])
        
            memberCard = create_member_card(memberDisplay, name, email, analytics)
            memberCard.grid(row = row, column = col)
            memberStorage.append(memberCard)
            
            row += 1
    
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

        refresh_sprint_cards()

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


def add_member_window(root):

    # Toplevel object which will
    # be treated as a new window
    addMemberWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    addMemberWindow.title("Add Member")
 
    # sets the geometry of toplevel
    addMemberWindow.geometry("400x200")
    
    def check_valid_email(email):
        valid_email = False

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.fullmatch(email_regex, email):
            valid_email = True

        return valid_email


    def add_member():

        if not check_valid_email(member_email_entry.get()):

            messagebox.showerror("Email Error", "Invalid email input entered!")
            return 

        # Create/Connect to a database
        connect_db = sqlite3.connect('members.db')
        # Create cusror
        cursor = connect_db.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS members
                ([member_name], [member_email], [member_analytics])
                ''')

        connect_db.execute("INSERT INTO members VALUES (:member_name, :member_email, :member_analytics)", 
                        {
                            'member_name': member_name_entry.get(),
                            'member_email': member_email_entry.get(),
                            'member_analytics': 0
                        }
                            )
        
        # Commit changes
        connect_db.commit()
        # Close Connnection
        connect_db.close()

        # Clear input boxes
        member_name_entry.delete(0, END)
        member_email_entry.delete(0, END)
        refresh_member_cards()

    frame = Frame(addMemberWindow, width = 400, height = 200)
    frame.pack()

    member_name = Label(frame, text = "Member Name:")
    member_name.place(x = 20, y = 50)

    member_email = Label(frame, text = "Member Email:")
    member_email.place(x = 20, y = 90)

    member_name_entry = Entry(frame, width = 40)
    member_email_entry = Entry(frame, width = 40)
    member_name_entry.place(x = 110, y = 50)
    member_email_entry.place(x = 110, y = 90)

    addButton = Button(frame, text = "Add Member", command = add_member)
    addButton.place(x = 200, y = 150, anchor = CENTER)

def init_team_board(root):
    ''' Initialise team board. '''
    
    # frame storing buttons at top
    buttonFrame = Frame(root, height = 20, width = 1100, bg = "#ECE3FC")
    buttonFrame.grid_rowconfigure(1, weight = 1)
    buttonFrame.grid_columnconfigure(3, weight = 1)
    buttonFrame.grid_propagate(False)
    buttonFrame.grid(row = 1, column = 1, pady = (30, 40))
    
    # "+"
    plusButton = Button(buttonFrame, text = "+", font = ("Arial", 12), width = 1, height = 5,
                        command = lambda: add_member_window(root))
    plusButton.grid(row = 1, column = 1, sticky = W)
    
    # "Add Team Member"
    addMemberButton = Button(buttonFrame, text = "Add Team Member", width = 16, height = 4,
                             command = lambda: add_member_window(root))
    addMemberButton.grid(row = 1, column = 2, sticky = W)
    
    # "Dashboard"
    dashboardButton = Button(buttonFrame, text = "Dashboard", width = 10, height = 4)
    dashboardButton.grid(row = 1, column = 3, sticky = E)
    
    # table listing members of sprint
    memberTableFrame = Frame(root, height = 450, width = 1000, bg = "#ECE3FC")
    memberTableFrame.grid_rowconfigure(10, weight = 1)
    memberTableFrame.grid_columnconfigure(4, weight = 1)
    memberTableFrame.grid_propagate(False)
    memberTableFrame.grid(row = 2, column = 1, sticky = "")
    
    # headers for table
    nameHeader = Label(memberTableFrame, text = "NAME", font = ("Roboto", 9, "bold")
                       , width = 52, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    nameHeader.grid(row = 0, column = 1, sticky = W+E)
    
    emailHeader = Label(memberTableFrame, text = "EMAIL", font = ("Roboto", 9, "bold")
                       , width = 60, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    emailHeader.grid(row = 0, column = 2, sticky = W+E)
    
    analyticsHeader = Label(memberTableFrame, text = "ANALYTICS", font = ("Roboto", 9, "bold")
                       , width = 20, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    analyticsHeader.grid(row = 0, column = 3, sticky = W+E)
    
    deleteHeader = Label(memberTableFrame, text = "", font = ("Roboto", 9, "bold")
                       , width = 5, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    deleteHeader.grid(row = 0, column = 4, sticky = W+E)
    
    return memberTableFrame


def create_member_card(root, name, email, analytics):
    ''' Creates an entry of a member in the table '''
    # turn name into string
    memberName = ""
    
    for char in name:
        memberName += str(char)
        
    # frame storing all fields of a member
    entryFrame = Frame(root, height = 2, width = 1000)
    entryFrame.grid_rowconfigure(1, weight = 1)
    entryFrame.grid_columnconfigure(4, weight = 1)
    entryFrame.grid(columnspan = 4)
    
    # member name
    nameFrame = Label(entryFrame, text = name, font = ("Roboto", 9)
                       , width = 52, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    nameFrame.grid(row = 1, column = 1, sticky = W+E)
    
    # member email
    emailFrame = Label(entryFrame, text = email, font = ("Roboto", 9)
                       , width = 60, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    emailFrame.grid(row = 1, column = 2, sticky = W+E)
    
    # member analytics
    analyticsFrame = Label(entryFrame, text = analytics, font = ("Roboto", 9)
                       , width = 20, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    analyticsFrame.grid(row = 1, column = 3, sticky = W+E)
    
    analyticsButton = Button(analyticsFrame, width = 10, height = 1, text = "Analytics",
                            font = ("Roboto", 8, "bold"), bg = "#0D5588", fg = "white")
    analyticsButton.place(x=32, y=3)
    
    # delete
    deleteFrame = Label(entryFrame, width = 7, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    deleteFrame.grid(row = 1, column = 4, sticky = W+E)
    
    deleteButton = Button(deleteFrame, width = 3, height = 1, text = "X", font = ("Arial", 8, "bold"),
                          bg = "red", fg = "white", command = lambda: remove_member())
    deleteButton.place(x=7, y=3)
    
    def remove_member():
        ''' Nested method that removes a member '''
        connection = sqlite3.connect("members.db")
        cursor = connection.cursor()

        query = ''' DELETE from members where member_name = ?'''
        cursor.execute(query, (memberName,))
        connection.commit()
    
    return entryFrame


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

def create_sprint_display(window, sprintName, sprintStatus, sprintStart, sprintEnd):
        
    if sprintStatus == "Not started":
        colour = "#D80000"
    if sprintStatus == "In progress":
        colour = "#FFEC00"
    elif sprintStatus == "Complete":
        colour = "#4CFF00"
    
    # frame for a sprint
    sprintFrame = Frame(window, width=30, height=40, 
                        highlightbackground = "black", highlightthickness=1)
    
    sprintFrame.grid_rowconfigure(6, weight = 1)
    sprintFrame.grid_columnconfigure(2, weight = 1)
    
    sprintFrame.config(bg = "#FFFFFF")
    
    # sprint name
    curr = Label(sprintFrame, text = sprintName, font=("Arial" ,8, "bold"), 
                    bg = colour, fg = "#000000", width = 30, justify=LEFT, anchor = "w")
    curr.grid(row = 1, column = 1, columnspan = 2, sticky = W)
    # sprint status
    curr = Label(sprintFrame, text = f"Status:         {sprintStatus}", font=("Arial" ,8),
                    bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
    curr.grid(row = 2, column = 1, columnspan = 2, sticky = W)
    
    # start date
    curr = Label(sprintFrame, text = f"Start Date:   {sprintStart}", font=("Arial" ,8),
                    bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
    curr.grid(row = 3, column = 1, columnspan = 2, sticky = W)
    
    # end date
    curr = Label(sprintFrame, text = f"End Date:   {sprintEnd}", font=("Arial" ,8),
                    bg = "#FFFFFF", width = 35, justify=LEFT, anchor = "w")  
    curr.grid(row = 4, column = 1, columnspan = 2, sticky = W)
    
    # details button
    detailsButton = Button(sprintFrame, text = "Details", anchor = E, font=("Arial" ,8, "bold")
                        , command = lambda: init_tasks_for_sprint(MainWindow, sprintName))
    detailsButton.grid(row = 5, column = 1, pady = 5, sticky = E)
    
    # edit button
    editButton = Button(sprintFrame, text = "Edit", anchor = W, font=("Arial" ,8, "bold")
                        , command = lambda: init_swap(MainWindow, sprintName))
    editButton.grid(row = 5, column = 2, pady = 5, sticky = W)
    
    global sprintCardStorage
    sprintCardStorage.append(sprintFrame)
    
    return sprintFrame

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

def init_swap(root, title):
    
    sprintName = ""
    
    for char in title:
        sprintName += str(char)
    
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
    startButton = Button(sprintTasksDisplay, text = " Get Started ", command = lambda: get_started())
    startButton.grid(row = 4, column = 2, padx = 1, sticky = "e")
    
    # save and exit
    saveButton = Button(sprintTasksDisplay, text = " Save and Exit ")
    saveButton.grid(row = 4, column = 4, padx = 1, sticky = "w")
    
    def get_started():
        ''' Changes sprint status when "Get Started" is clicked '''
        connection = sqlite3.connect("sprints.db")
        cursor = connection.cursor()

        query = ''' Update sprints set status = ? where sprint_name = ?'''
        data = ("In progress", sprintName)
        cursor.execute(query, data)
        connection.commit()
        refresh_sprint_cards()


def init_tasks_for_sprint(root, title):
    ''' Initialises the tasks for a particular sprint, sorted according to progress status'''
    # create top level window for task display
    sprintTasksDisplay = Toplevel(root, height=400, width=800)
    
    sprintName = ""
    
    for char in title:
        sprintName += str(char)
    
    rows = 4
    cols = 6
    
    # set up grid
    sprintTasksDisplay.grid_rowconfigure(rows, weight = 1)
    sprintTasksDisplay.grid_columnconfigure(cols, weight = 1)
    
    # window title
    # TODO: get title of sprint using database
    title = Label(sprintTasksDisplay, text = "'Sprint Title' Board", anchor = CENTER)
    title.grid(row = 1, column = 1, columnspan = 5, pady = (15,20))
    
    # spacing
    Label(sprintTasksDisplay, width = 26).grid(row = 2, column = 1)
    Label(sprintTasksDisplay, width = 26).grid(row = 2, column = 5)
    
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
    
    completeButton = Button(sprintTasksDisplay, text = " Complete Sprint ", anchor = CENTER, 
                            command = lambda: complete_sprint())
    completeButton.grid(row = 4, column = 1, columnspan = cols, padx = 1)
    
    scroll = Scrollbar(sprintTasksDisplay)
    scroll.grid(row = 2, column = 6, rowspan = rows, sticky = "ne")
    
    def complete_sprint():
        ''' Changes sprint status when "Complete" is clicked '''
        connection = sqlite3.connect("sprints.db")
        cursor = connection.cursor()

        query = ''' Update sprints set status = ? where sprint_name = ?'''
        data = ("Complete", sprintName)
        cursor.execute(query, data)
        connection.commit()
        refresh_sprint_cards()


def refresh_task_cards():
    """ Refresh all the task cards once changes are made to the database"""
    global cardStorage
    for card in cardStorage:
        card.destroy()
    cardStorage = []
    display(cardStorage)

def refresh_sprint_cards():
    """ Refresh all the sprint cards once changes are made to the database"""
    global sprintCardStorage
    global SprintDisplay
    for card in sprintCardStorage:
        card.destroy()

    connect_db = sqlite3.connect("sprints.db")
    
    # create cusror
    cursor = connect_db.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprints
                ([sprint_name], [start_date], [end_date], [status])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from sprints")
    sprints = cursor.fetchall()
    
    # [0]: sprint_name
    # [1]: start_date
    # [2]: end_date
    # [3]: status

    row = 1
    col = 1
    # print each card
    for sprint in sprints:
        name = (sprint[0])
        status = (sprint[3])
        start = (sprint[1])
        end = (sprint[2])
        
        if col > 5:
            col = 1
            row += 1
    
        sprintCard = create_sprint_display(SprintDisplay, name, status, start, end)
        sprintCard.grid(row = row, column = col, sticky = "w", padx = (0,10), pady = (0,10))
        
        col += 1
        
def refresh_member_cards():
    """ Refresh all the sprint cards once changes are made to the database"""
    global memberStorage
    global memberDisplay
    
    for member in memberStorage:
        member.destroy()

    # connect to database
    connect_db = sqlite3.connect("members.db")
    
    # create cusror
    cursor = connect_db.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS members
                ([member_name], [member_email], [member_analytics])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from members")
    members = cursor.fetchall()
    
    # [0]: member_name
    # [1]: member_email
    # [2]: member_analytics
    
    row = 1
    col = 1
    
    # check if there are members
    if members == []:
            empty = Label(memberDisplay, text = "No members to show.", font = ("Roboto", 10),
                          bg = "white", fg = "black", height = 2,
                          highlightbackground = "black", highlightthickness = 1)
            empty.grid(row = 1, column = 1, columnspan = 4, sticky = E+W)
    else:
        # print each card
        for member in members:
            name = (member[0])
            email = (member[1])
            analytics = (member[2])
            end = (member[2])
        
            memberCard = create_member_card(memberDisplay, name, email, analytics)
            memberCard.grid(row = row, column = col)
            memberStorage.append(memberCard)
            
            row += 1
    
main()
