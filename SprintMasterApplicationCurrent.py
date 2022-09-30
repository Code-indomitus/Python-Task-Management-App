from msilib.schema import ComboBox
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3
from tasks import *
from swap import *
from task_sorting import *

root = Tk()
root.geometry('1200x600')
root.title("SPRINT BOARD")

def createNewSprintWindow():

    def create():
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

     
    # Toplevel object which will
    # be treated as a new window
    newSprintWindow = Toplevel(root)
 
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

    createButton = Button(frame, text = "Create Sprint", command = create)
    createButton.place(x = 110, y = 290)

    discardButton = Button(frame, text = "Discard Sprint", command = newSprintWindow.destroy)
    discardButton.place(x = 225, y = 290)

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

def create_sprint_display(mainSprintWindow, sprintNames, sprintStatus, sprintStart, sprintEnd):
    
    # main frame with all sprints and their status displayed
    mainDisplay = Frame(mainSprintWindow, width=300, height=300)
    mainDisplay.place(x = 10, y = 100)
    
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
                            , command = lambda: init_tasks_for_sprint(root))
        detailsButton.grid(row = 5, column = 1, pady = 5, sticky = E)
        
        # edit button
        editButton = Button(sprintFrame, text = "Edit", anchor = W, font=("Arial" ,8, "bold")
                            , command = lambda: init_swap(root))
        editButton.grid(row = 5, column = 2, pady = 5, sticky = W)

        col += 1

createSprintButton = Button(root, text = "Create New Sprint", command = createNewSprintWindow)

# main is calling SprintMasterApplication's main
createTaskButton = Button(root, text = "Add Task", command = lambda: create_task_window(root))

createSprintButton.place(x = 50, y = 20)

createTaskButton.place(x = 1150, y = 20)

names, status, start, end = get_sprints_details()

create_sprint_display(root, names, status, start, end)

root.mainloop()


