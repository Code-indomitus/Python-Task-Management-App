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
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import *
import random

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
sprintCount = 0 # number of exisiting sprints

def main():
    
    # connect to database during start
    connect_db = sqlite3.connect('tasks.db')
    
    # create cusror
    cursor = connect_db.cursor()
        
    # create table "tasks" in same dir if it does not exist locally
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks
                    ([task_name], [task_description], [story_points], [priority], [status], [assigned_to], [tag], [id], [pos], [belongs])
                    ''')
          
    # attributes

    # create master window
    requiredRow = 9
    requiredCol = 6
    mainWindow = init_main_window("Sprint Master", "2000x630", requiredRow, requiredCol)
    MainWindow = mainWindow

    # Image for application logo
    #sprintMasterLogo = PhotoImage(file = "C:\\Users\\Shyam\\OneDrive\\Desktop\\FIT2101 REPO\\group-c3\\SprintMaster.png")
    # set icon logo for application
    #mainWindow.iconphoto(False, sprintMasterLogo)
    
    # setup tabs
    notebook = ttk.Notebook(mainWindow)
    notebook.grid(pady = 15, sticky = N+S+E+W)

    task_tab = Frame(notebook, width = 2000, height = 630, bg = "#f5dd9d")
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
    Label(sprint_tab, width = 7, bg = "#DDF2FD").grid(row = 1, column = 1, sticky = W)
    Label(sprint_tab, width = 7, bg = "#DDF2FD").grid(row = 1, column = 3, sticky = E)

    global TaskTab
    global SprintTab
    global TeamTab

    TaskTab = task_tab
    SprintTab = sprint_tab
    TeamTab = team_tab

    # Task Board widgets
    createTaskButton = Button(task_tab, text = "Create New Task", command = createNewTaskWindow, bg = "#ffbc11")
    filterLabel = Label(task_tab ,text = "Filter: ", bg = "#f5dd9d") 
    current_tag = StringVar()
    tags = Combobox(task_tab, textvariable = current_tag)

    tags['values'] = ('ALL','UI', 'CORE', 'TESTING')
    tags['state'] = 'readonly'
    tags.current(0)
    
    filterButton = Button(task_tab, text = "FILTER", bg = "#ffbc11", command = lambda: filter(tags.get()))
    # create spacing in grid for C1 and C6
    spaceStart = Frame(task_tab, width=50, height=50, bg = "#f5dd9d")
    spaceEnd = Frame(task_tab, width=50, height=50, bg = "#f5dd9d")
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
    createTaskButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, padx = 5,pady = 12, sticky = "w")
    
    # Sprint Board widgets
    createSprintButton = Button(sprint_tab, text = "Create New Sprint", bg = "#abe4ff", command = createNewSprintWindow)
    createSprintButton.place(x = 54, y = 20)

    #log time 
    logTimeButton = Button(sprint_tab, text = "Log Time", bg = "#abe4ff", command = log_time_window)
    logTimeButton.place(x = 1000, y = 20)

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
                ([sprint_name], [start_date], [end_date], [status], [id])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from sprints")
    sprints = cursor.fetchall()
    
    # [0]: sprint_name
    # [1]: start_date
    # [2]: end_date
    # [3]: status
    # [4]: id
    
    row = 1
    col = 1
    global sprintCardStorage
    
    # print each card
    for sprint in sprints:
        name = (sprint[0])
        status = (sprint[3])
        start = (sprint[1])
        end = (sprint[2])
        id = (sprint[4])
        
        if col > 5:
            col = 1
            row += 1
    
        sprintCard = create_sprint_display(sprintDisplay, name, status, start, end, id)
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

    # Create/Connect to a database
    connect_db = sqlite3.connect('log.db')
    # Create cusror
    cursor = connect_db.cursor()

    # create table "log" in same dir if it does not exist locally
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS log
                ([member_name], [hours_logged], [times_logged])
                ''')

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

    def createSprint(window):
        # Create/Connect to a database
        connect_db = sqlite3.connect('sprints.db')
        # Create cusror
        cursor = connect_db.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprints
                ([sprint_name], [start_date], [end_date], [status], [id])
                ''')
        
        # get all exising sprint ids
        query = cursor.execute('''
                                SELECT id FROM sprints
                                ''')
        
        # determine id for newly created sprint
        ids = []
        for id in query:
            ids.append(id[0]) # append all exisiting ids for reference
            
        if ids != []:
            sprintId = max(ids) + 1 # not first sprint to be created
        else:
            sprintId = 1 # if first sprint to be created

        connect_db.execute("INSERT INTO sprints VALUES (:sprint_name, :start_date, :end_date, :status, :id)", 
                        {
                            'sprint_name': sprint_name_entry.get(),
                            'start_date': start_date_entry.get_date().strftime("%m/%d/%Y"),
                            'end_date': end_date_entry.get_date().strftime("%m/%d/%Y"),
                            'status': 'Not started', # default status
                            'id': sprintId
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
        window.destroy()

    # Toplevel object which will
    # be treated as a new window
    newSprintWindow = Toplevel(MainWindow)

    newSprintWindow.configure(bg = "#DDF2FD")

    # sets the title of the
    # Toplevel widget
    newSprintWindow.title("New Sprint")
 
    # sets the geometry of toplevel
    newSprintWindow.geometry("400x400")


    frame = Frame(newSprintWindow, width = 400, height = 400, bg = "#DDF2FD")
    frame.pack()

    sprint_name = Label(frame, text = "Sprint Name:", bg = "#DDF2FD")
    sprint_name.place(x = 20, y = 50)

    start_date = Label(frame, text = "Start Date:", bg = "#DDF2FD")
    start_date.place(x = 20, y = 90)

    end_date = Label(frame, text = "End Date:", bg = "#DDF2FD")
    end_date.place(x = 20, y = 140)

    sprint_name_entry = Entry(frame, width = 40)
    start_date_entry = DateEntry(frame,selectmode='day')  # Date entry allows user to get date input using a calendar. The date input is in datetime.date format/object
    end_date_entry = DateEntry(frame,selectmode='day')
    sprint_name_entry.place(x = 110, y = 50)
    start_date_entry.place(x = 110, y = 90)
    end_date_entry.place(x = 110, y = 140)

    createButton = Button(frame, text = "Create Sprint", bg = "#abe4ff", command = lambda: createSprint(newSprintWindow))
    createButton.place(x = 110, y = 290)

    discardButton = Button(frame, text = "Discard Sprint", bg = "#abe4ff", command = newSprintWindow.destroy)
    discardButton.place(x = 225, y = 290)

def log_time_window():
    # Toplevel object which will
    # be treated as a new window
    logTimeWindow = Toplevel(MainWindow)

    logTimeWindow.configure(bg = "#DDF2FD")

    # sets the title of the
    # Toplevel widget
    logTimeWindow.title("Log Time")
 
    # sets the geometry of toplevel
    logTimeWindow.geometry("300x300")


    def log_time():
        #connect to database
        sqliteConnection = sqlite3.connect('log.db')
        #connect to cursor
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * from log where member_name")
        member = cursor.fetchall()
        sqlite_select_query = """SELECT * from log where member_name = ?"""
        cursor.execute(sqlite_select_query, (member_name.get(),))
        record = cursor.fetchone()

        prev_time_logged = int(record[1])
        prev_times_logged = int(record[2])

        new_time_logged = prev_time_logged + int(time_spent_entry.get())
        new_times_logged = prev_times_logged + 1

        #update the selected row
        sql_update_query = "Update log set hours_logged = ?, times_logged = ? where member_name = ?"
        data = (new_time_logged, new_times_logged, member_name.get())
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

        logTimeWindow.destroy()
        
    connect_db = sqlite3.connect("members.db")
    # create cusror
    cursor = connect_db.cursor()
    # select all data from table    
    cursor.execute("SELECT * from members")
    members = cursor.fetchall()
    # [0]: member_name
    # [1]: member_email
    # [2]: member_analytics
    member_name_list = [] # list of member names
    for member in members:
        member_name_list.append(member[0])


    frame = Frame(logTimeWindow, width = 400, height = 400, bg = "#DDF2FD")
    frame.pack()
    
    member_name_label = Label(frame, text = "Member:", bg = "#DDF2FD")
    member_name_label.place(x = 20, y = 50)

    time_spent = Label(frame, text = "Time Spent:", bg = "#DDF2FD")
    time_spent.place(x = 20, y = 90)

    date = Label(frame, text = "End Date:", bg = "#DDF2FD")
    date.place(x = 20, y = 130)

    memberName = StringVar()
    member_name = Combobox(frame, textvariable = memberName)

    # check if there are any members added to the project
    if len(member_name_list) > 0:
        member_name['values'] = tuple(member_name_list)
    else:
        member_name['values'] = ('None')

    member_name['state'] = 'readonly'
    member_name.current(0)
    member_name.place(x = 110, y = 50)

    time_spent_entry = Entry(frame, width = 23)
    date_entry = DateEntry(frame,selectmode='day')

    time_spent_entry.place(x = 110, y = 90)
    date_entry.place(x = 110, y = 130)

    if len(member_name_list) > 0:
        logButton = Button(frame, text = "Log Time", bg = "#abe4ff", command = log_time)
        logButton.place(x = 115, y = 210)
    else:
        no_member_label = Label(frame, text = "NO MEMBERS AVAILABLE", bg = "#abe4ff")
        no_member_label.place(x = 80, y = 210)

def add_member_window(root):

    # Toplevel object which will
    # be treated as a new window
    addMemberWindow = Toplevel(root)

    addMemberWindow.configure(bg = "#ECE3FC")
 
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


    def add_member(window):

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
        
        #Update the log database with new member

        # Create/Connect to a database
        connect_log_db = sqlite3.connect('log.db')
        # Create cusror
        cursor_log = connect_log_db.cursor()

        # create table "log" in same dir if it does not exist locally
        cursor_log.execute('''
                    CREATE TABLE IF NOT EXISTS log
                    ([member_name], [hours_logged], [times_logged])
                    ''')
        
        connect_log_db.execute("INSERT INTO log VALUES (:member_name, :hours_logged, :times_logged)", 
                {
                    'member_name': member_name_entry.get(),
                    'hours_logged': 0,
                    'times_logged': 0
                }
                    )

        # Commit changes
        connect_db.commit()
        # Close Connnection
        connect_db.close()

        # Commit changes
        connect_log_db.commit()
        # Close Connnection
        connect_log_db.close()

        # Clear input boxes
        member_name_entry.delete(0, END)
        member_email_entry.delete(0, END)
        refresh_member_cards()
        window.destroy()

    frame = Frame(addMemberWindow, width = 400, height = 200, bg = "#ECE3FC")
    frame.pack()

    member_name = Label(frame, text = "Member Name:", bg = "#ECE3FC")
    member_name.place(x = 20, y = 50)

    member_email = Label(frame, text = "Member Email:", bg = "#ECE3FC")
    member_email.place(x = 20, y = 90)

    member_name_entry = Entry(frame, width = 40)
    member_email_entry = Entry(frame, width = 40)
    member_name_entry.place(x = 110, y = 50)
    member_email_entry.place(x = 110, y = 90)

    addButton = Button(frame, text = "Add Member", bg = "#d9abff", command = lambda: add_member(addMemberWindow))
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
    plusButton = Button(buttonFrame, text = "+", font = ("Arial", 12), width = 1, height = 5, bg = "#d9abff",
                        command = lambda: add_member_window(root))
    plusButton.grid(row = 1, column = 1, sticky = W)
    
    # "Add Team Member"
    addMemberButton = Button(buttonFrame, text = "Add Team Member", width = 16, height = 4, bg = "#d9abff",
                             command = lambda: add_member_window(root))
    addMemberButton.grid(row = 1, column = 2, sticky = W)
    
    # "Dashboard"
    dashboardButton = Button(buttonFrame, text = "Dashboard", width = 10, height = 4, bg = "#d9abff",
                             command = lambda: dashboard(root))
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

def dashboard(root):
    dashboardWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    dashboardWindow.title("Team Dashboard")
 
    # sets the geometry of toplevel
    dashboardWindow.geometry("800x630")

    dashboardWindow.grid_rowconfigure(4, weight = 1)
    dashboardWindow.grid_columnconfigure(1, weight = 1)

    dashboardLabel = Label(dashboardWindow, text = "DASHBOARD", font = ("Roboto", 14, "bold"), fg = "#001449", pady = 30, padx = 30)
    dashboardLabel.grid(row = 1, column = 1, sticky = W+E)

    dateFrame = Frame(dashboardWindow, height = 100, width = 200, bg = "blue")
    dateFrame.grid_rowconfigure(3, weight = 1)
    dateFrame.grid_columnconfigure(2, weight = 1)
    dateFrame.grid(row = 2, column = 1, sticky = "")

    startDate = Label(dateFrame, text = "Start Date", font = ("Roboto", 9, "bold")
                       , width = 10, height = 2, bg = "#647687", fg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    endDate = Label(dateFrame, text = "End Date", font = ("Roboto", 9, "bold")
                       , width = 10, height = 2, bg = "#647687", fg = "white",
                       highlightbackground = "black", highlightthickness = 1)

    startDate.grid(row = 0, column = 0, sticky = W+E)
    endDate.grid(row = 0, column = 1, sticky = W+E)

    startDateEntryLabel = Label(dateFrame, text = "", font = ("Roboto", 9, "bold")
                       , width = 10, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    endDateEntryLabel = Label(dateFrame, text = "", font = ("Roboto", 9, "bold")
                       , width = 10, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)

    startDateEntryLabel.grid(row = 1, column = 1, sticky = W+E)
    endDateEntryLabel.grid(row = 1, column = 0, sticky = W+E)

    start_date_entry = DateEntry(startDateEntryLabel, selectmode='day')  # Date entry allows user to get date input using a calendar. The date input is in datetime.date format/object
    end_date_entry = DateEntry(endDateEntryLabel, selectmode='day')
    start_date_entry.grid(sticky = "we")
    end_date_entry.grid(sticky = "we")

    getResultLabel = Label(dateFrame, text = "", font = ("Roboto", 9, "bold")
                       , width = 20, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    getResultLabel.grid(row = 2, column = 0, columnspan = 2, sticky = W+E)

    getResultButton = Button(getResultLabel, text = "Get Results", width = 30, height = 1,
                             command = lambda: get_results(dashboardWindow))
    getResultButton.grid(sticky = W+E)

    backButton = Button(dashboardWindow, text = "Back", command = lambda: dashboardWindow.destroy())
    backButton.grid(row = 1, column = 1, padx = 40, pady = 40, sticky = E)


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
                            font = ("Roboto", 8, "bold"), bg = "#0D5588", fg = "white",
                            command = lambda: check_analytics(root, name))
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

        ''' Nested method that removes a member '''
        connection = sqlite3.connect("log.db")
        cursor = connection.cursor()

        query = ''' DELETE from log where member_name = ?'''
        cursor.execute(query, (memberName,))
        connection.commit()


        refresh_member_cards()
    
    return entryFrame


def createNewTaskWindow():

    def createTask(window):

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
        connect_db.execute("INSERT INTO tasks VALUES (:task_name, :task_description, :story_points, :priority, :status, :assigned_to, :tag, :id, :pos, :belongs)", 
                        {
                            'task_name': entry1.get(),
                            'task_description': entry2.get(),
                            'story_points': entry3.get(),
                            'priority': priority.get(),
                            'status': status.get(),
                            'assigned_to': assigned_to.get(),
                            'tag': tag.get(),
                            'id': currentTaskNumber,
                            'pos': 1,
                            'belongs': 0
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

        window.destroy()

    # Toplevel object which will
    # be treated as a new window
    newTaskWindow = Toplevel(MainWindow)

    newTaskWindow.configure(bg = "#f5dd9d")
 
    # sets the title of the
    # Toplevel widget
    newTaskWindow.title("New Task")
 
    # sets the geometry of toplevel
    newTaskWindow.geometry("500x500")


    frame = Frame(newTaskWindow, width = 400, height = 400, bg = "#f5dd9d")
    frame.pack()

    task_name = Label(frame, text = "Task Name:", bg = "#f5dd9d")
    task_name.place(x = 20, y = 50)

    task_description = Label(frame, text = "Task Description:", bg = "#f5dd9d")
    task_description.place(x = 20, y = 80)

    task_story_points = Label(frame, text = "Story Points:", bg = "#f5dd9d")
    task_story_points.place(x = 20, y = 110)

    task_priority = Label(frame, text = "Priority:", bg = "#f5dd9d")
    task_priority.place(x = 20, y = 140)

    task_status = Label(frame, text = "Status:", bg = "#f5dd9d")
    task_status.place(x = 20, y = 170)

    task_assigned_to = Label(frame, text = "Assigned To:", bg = "#f5dd9d")
    task_assigned_to.place(x = 20, y = 200)

    task_tag = Label(frame, text = "Tag:", bg = "#f5dd9d")
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

    connect_db = sqlite3.connect("members.db")
    # create cusror
    cursor = connect_db.cursor()
    # select all data from table    
    cursor.execute("SELECT * from members")
    members = cursor.fetchall()
    # [0]: member_name
    # [1]: member_email
    # [2]: member_analytics
    member_name_list = [] # list of member names
    for member in members:
        member_name_list.append(member[0])

    current_assigned_to = StringVar()
    assigned_to = Combobox(frame, textvariable = current_assigned_to)

    if len(member_name_list) > 0:
        member_name_list.insert(0, "Everyone")
        assigned_to['values'] = tuple(member_name_list)
    else:
        assigned_to['values'] = ('Everyone')
    assigned_to['state'] = 'readonly'
    assigned_to.current(0)
    assigned_to.place(x = 140, y = 200)

    current_tag = StringVar()
    tag = Combobox(frame, textvariable = current_tag)
    tag['values'] = ('UI', 'CORE', 'TESTING')
    tag['state'] = 'readonly'
    tag.current(0)
    tag.place(x = 140, y = 230)

    createButton = Button(frame, text = "Create", bg = "#ffbc11", command = lambda: createTask(newTaskWindow))
    createButton.place(x = 125, y = 350)

    discardButton = Button(frame, text = "Close", bg = "#ffbc11", command = newTaskWindow.destroy)
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
        frontSpace.config(fg = "#000000", bg = "#DD8300", text = "Not started")
    elif DescStatus == "In Progress":
        frontSpace.config(fg = "#000000", bg = "#FFD800", text = "In Progress")
    elif DescStatus == "Complete":
        frontSpace.config(fg = "#000000", bg = "#3AFF00", text = "Complete")
    frontSpace.grid(row = 2, column = 1, columnspan = 8, padx = 3, pady = 1)
    
    priorityBox = Label(mainFrame, width=2, height=1, bg = "gray", highlightbackground="black", highlightthickness=1) # coloured priority box
    if DescPriority == "Low":
        priorityBox.config(bg = "#3CDD00")
    elif DescPriority == "Medium":
        priorityBox.config(bg = "#FFE400")
    elif DescPriority == "High":
        priorityBox.config(bg = "#FF3200")
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

def create_sprint_display(window, sprintName, sprintStatus, sprintStart, sprintEnd, id):
        
    if sprintStatus == "Not started":
        colour = "#DD8300"
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
                        , command = lambda: init_swap(MainWindow, sprintName, id))
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



def init_swap(root, title, id):
    
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
    startButton = Button(sprintTasksDisplay, text = " Get Started ", command = lambda: get_started(sprintTasksDisplay))
    startButton.grid(row = 4, column = 2, padx = 1, sticky = "e")
    
    # save and exit
    saveButton = Button(sprintTasksDisplay, text = " Save and Exit ", command = lambda: close_windows(sprintTasksDisplay))
    saveButton.grid(row = 4, column = 4, padx = 1, sticky = "w")
    
    def get_started(sprintTasksDisplay):
        ''' Changes sprint status when "Get Started" is clicked '''
        connection = sqlite3.connect("sprints.db")
        cursor = connection.cursor()

        query = ''' Update sprints set status = ? where sprint_name = ?'''
        data = ("In progress", sprintName)
        cursor.execute(query, data)
        connection.commit()
        refresh_sprint_cards()
        sprintTasksDisplay.destroy()

    def close_windows(sprintTasksDisplay):
        sprintTasksDisplay.destroy()


    def changePos(id, pos, mainFrame, belongs, sprint_id):
        if pos == 1:
            pos = 2
            belongs = sprint_id
        elif pos == 2:
            pos = 1
            belongs = 0

        #connect to database
        sqliteConnection = sqlite3.connect('tasks.db')
        #connect to cursor
        cursor = sqliteConnection.cursor()

        #update the selected row
        sql_update_query = "Update tasks set pos = ?, belongs = ? where id = ?"
        data = (pos,belongs, int(id))
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

#        global copyCardStorage
        global places
        mainFrame.destroy()        
        copyCardStorage = []
        places = []
        display_swap(copyCardStorage, sprint_id)


    global copyCardStorage
    copyCardStorage = []
    global places
    places = []
##############################################################################################################################
    def create_task_card_swap(cardStorage,taskNumber, 
                     DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag, pos, belongs, sprint_id):
        if pos == 1:
            # main frame for card
            mainFrame = Frame(productBacklogFrame, width=280, height=200, highlightbackground="gray", highlightthickness=2)
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
            cardSwap = Button(mainFrame, text = "swap", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF", command= lambda:changePos(taskNumber, pos, mainFrame, belongs, sprint_id))
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
                priorityBox.config(bg = "#DD8300")
            elif DescPriority == "High":
                priorityBox.config(bg = "#DD0000")
            elif DescPriority == "Critical":
                priorityBox.config(text = "!", font=("Arial" , 9, "bold"),
                                fg = "#FF0000", bg = "#FFFFFF", highlightbackground="red", highlightthickness=1)
            priorityBox.grid(row = 1, column = 5, padx = 3, pady = 3)
            
            cardNum.grid(row = 1, column = 2, columnspan = 1, padx = 2, pady = 2, sticky = "w")
            cardEditTask.grid(row = 1, column = 6, padx = 2, pady = 2, sticky = "w")
            cardDelete.grid(row = 1, column = 7, padx = 2, pady = 2, sticky = "w")
            cardSwap.grid(row = 1, column = 8, padx = 2, pady = 2, sticky = "w")
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
            cardStorage.append([mainFrame, belongs])
            copyCardStorage.append([mainFrame, belongs])
            places.append([taskNumber, belongs])

        elif pos == 2:
            # main frame for card
            mainFrame = Frame(sprintBacklogFrame, width=280, height=200, highlightbackground="gray", highlightthickness=2)
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
            cardSwap = Button(mainFrame, text = "swap", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF", command= lambda:changePos(taskNumber, pos, mainFrame, belongs, sprint_id))
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
            priorityBox.grid(row = 1, column = 5, padx = 3, pady = 3)
            
            cardNum.grid(row = 1, column = 2, columnspan = 1, padx = 2, pady = 2, sticky = "w")
            cardEditTask.grid(row = 1, column = 6, padx = 2, pady = 2, sticky = "w")
            cardDelete.grid(row = 1, column = 7, padx = 2, pady = 2, sticky = "w")
            cardSwap.grid(row = 1, column = 8, padx = 2, pady = 2, sticky = "w")
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
            cardStorage.append([mainFrame, belongs])
            copyCardStorage.append([mainFrame, belongs])
            places.append([taskNumber, belongs])

    # place cards in grid
    def place_card_swap(cardStorage, sprint_id, places):
        currentRow = 1 
        currentCol = 1
        for card in range(0,len(cardStorage)):
            # add column-wise first, then add row if insufficient space ([arbitrary]Rx4C)
            if places[card][1] == sprint_id:
                if currentCol == 2:
                    currentCol = 1
                    currentRow += 1
                cardStorage[card][0].grid(row = currentRow, column = currentCol, padx = 5, pady = 5, sticky = "s")
                currentCol += 1
            elif places[card][1] == 0:
                if currentCol == 2:
                    currentCol = 1
                    currentRow += 1
                cardStorage[card][0].grid(row = currentRow, column = currentCol, padx = 5, pady = 5, sticky = "s")
                currentCol += 1
        
    
    def display_swap(cardStorage, sprint_id):
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
        # [8]: pos
        # [9]: belongs

        for row in rows:
            DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag, taskNumber, pos, belongs = row[0], row[1], row[3], row[2], row[4], row[5], row[6], row[7], row[8], row[9]
            create_task_card_swap(cardStorage, taskNumber, DescName, 
                            DescDesc, DescPriority, DescPoints, DescStatus, DescAssign, DescTag, pos, belongs, sprint_id)
        
        # display if cardArray not empty
        if cardStorage:
            place_card_swap(cardStorage, sprint_id, places)
            
        connect_db.commit
        connect_db.close()


    cardStorage = []
    display_swap(cardStorage, id)
####################################################################################################################################



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
                ([sprint_name], [start_date], [end_date], [status], [id])
                ''')
        
    # select all data from table    
    cursor.execute("SELECT * from sprints")
    sprints = cursor.fetchall()
    
    # [0]: sprint_name
    # [1]: start_date
    # [2]: end_date
    # [3]: status
    # [4]: id

    row = 1
    col = 1
    # print each card
    for sprint in sprints:
        name = (sprint[0])
        status = (sprint[3])
        start = (sprint[1])
        end = (sprint[2])
        id = (sprint[4])
        
        if col > 5:
            col = 1
            row += 1
    
        sprintCard = create_sprint_display(SprintDisplay, name, status, start, end, id)
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
            
def check_analytics(root, name):
    """ Plots a graph of hours logged against time (previous 7 days) """
    # covert name to string for title
    strName = ""
    for char in name:
        strName += char
    
    # get dates (x-axis)
    duration = 7 # previous 7 days
    x = []
    for i in range(0, duration):
        x.append((datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y'))
    
    # hours logged (y-axis)
    y = []
    for i in range(duration):
        y.append(random.randrange(1,12))
        
    # tkinter window that will house plot
    plotWindow = Toplevel(root)
    
    figure = Figure(figsize = (5, 5), dpi = 100) # figure that contains plot
    plot1 = figure.add_subplot(111) # occupy all subplots
    
    barChart = plot1.bar(x, y, color = "#00DDD3", width = 0.4) # plot bar chart
    plot1.bar_label(barChart, label_type='edge') # label y bars
    plot1.set_xticklabels(x, rotation=45, fontsize=8) # rotate x tick labels
    figure.tight_layout(rect=[0.04, 0.04, 0.95, 0.95]) # fit to window, [west ,south ,east ,north]
    
    # plot labels
    plot1.set_xlabel("Day")
    plot1.set_ylabel("Hours logged")
    plot1.set_title(f"{strName}'s Analytics")
    
    # place chart in canvas
    canvas = FigureCanvasTkAgg(figure, master = plotWindow)  
    canvas.draw()
    canvas.get_tk_widget().pack(side = TOP, fill = 'both', expand = True)
    
def create_log_card(root, name, hours):
    ''' Creates an entry of a member in the table '''
    # turn name into string
    memberName = ""
    
    for char in name:
        memberName += str(char)
        
    # frame storing all fields of a member
    entryFrame = Frame(root, height = 2, width = 1000)
    entryFrame.grid_rowconfigure(1, weight = 1)
    entryFrame.grid_columnconfigure(2, weight = 1)
    entryFrame.grid(columnspan = 4)
    
    # member name
    nameFrame = Label(entryFrame, text = name, font = ("Roboto", 9)
                       , width = 45, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    nameFrame.grid(row = 1, column = 1, sticky = W+E)
    
    # member hours
    hoursFrame = Label(entryFrame, text = hours, font = ("Roboto", 9)
                       , width = 45, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    hoursFrame.grid(row = 1, column = 2, sticky = W+E)
    
    return entryFrame

def get_results(root):
    tableFrame = Frame(root, bg = "red", width = 300, height = 300)
    tableFrame.grid(row = 4, column = 1)
    
    tableFrame.grid_columnconfigure(2, weight = 1)
    tableFrame.grid_rowconfigure(10, weight = 1)
    
    nameLabel = Label(tableFrame, text = "Member Name", bg = "#647687", fg = "white",
                      font = ("Roboto", 9, "bold"), width = 45, height = 2,
                      highlightbackground="black", highlightthickness=1)
    nameLabel.grid(row = 1, column = 1, sticky = W+E)
    
    hoursLabel = Label(tableFrame, text = "Average Time (Hours)", bg = "#647687", fg = "white",
                       font = ("Roboto", 9, "bold"), width = 45, height = 2,
                       highlightbackground="black", highlightthickness=1)
    hoursLabel.grid(row = 1, column = 2, sticky = W+E)
    
    # Create/Connect to a database
    connect_db = sqlite3.connect('log.db')
    # Create cusror
    cursor = connect_db.cursor()

    # create table "log" in same dir if it does not exist locally
    logs = cursor.execute('''
                SELECT * from log
                ''')
    
    hasData = False
    
    row = 2
    col = 1
    for log in logs:
        hasData = True
        # [0], [1], [2] = [member_name], [hours_logged], [times_logged]
        memberName = log[0]
        if log[1] == 0 or log[2] == 0:
            avgHours = 0
        else:
            avgHours = log[1]/log[2]
        logCard = create_log_card(tableFrame, memberName, avgHours)
        logCard.grid(row = row, column = col, columnspan = 2,
                     sticky = N)
        
        row += 1
        
    if not hasData:
        noLogs = Label(tableFrame, text = "No data to display.", width = 45, height = 2,
                    highlightbackground="black", highlightthickness=1, bg = "white")
        noLogs.grid(row = 2, column = 1, columnspan = 2, sticky=W+E)
    
main()
