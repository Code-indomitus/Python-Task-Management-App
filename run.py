from email import message
import math
from msilib.schema import ComboBox
from queue import Empty
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3

# TODO: replace do_nothing() with edit functionality (line 235)
# TODO: replace do_nothing() with delete functionality (line 236)
MainWindow = None
cardStorage = [] # stores tasks as cards
def main():
    
    # connect to database during start
    connect_db = sqlite3.connect('tasks.db')
    
    # create cusror
    cursor = connect_db.cursor()
        
    # create table "tasks" in same dir if it does not exist locally
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks
                    ([task_name], [task_description], [stroy_points], [priority], [status], [assigned_to], [tag])
                    ''')
          
    # attributes

    # create master window
    requiredRow = 8
    requiredCol = 6
    mainWindow = init_main_window("Sprint Master", "2000x630", requiredRow, requiredCol)
    MainWindow = mainWindow
    # Shyam
    createTaskButton = Button(mainWindow, text = "Create New Task", command = createNewTaskWindow)
    filterLabel = Label(mainWindow ,text = "Filter: ") 
    current_tag = StringVar()
    tags = Combobox(mainWindow, textvariable = current_tag)

    tags['values'] = ('NONE','UI', 'CALL', 'TESTING')
    tags['state'] = 'readonly'
    tags.current(0)
    
    # create spacing in grid for C1 and C6
    spaceStart = Frame(mainWindow, width=50, height=50)
    spaceEnd = Frame(mainWindow, width=50, height=50)
    spaceStart.grid(row = 3, column = 1, padx = 3, pady = 3, sticky = "nw")
    spaceEnd.grid(row = 3, column = 6, padx = 3, pady = 3, sticky = "ne")

    # place buttons within main window
    startRow, startCol, spanRow, spanCol = 2, 5, 1, 1 # tags
    tags.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 4, 1, 1 # filter:
    filterLabel.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 2, 1, 2 # create task button
    createTaskButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "w")
    
    # create "Sprint Master" label
    labelSprintMaster = add_label("Sprint Master")
    startRow, startCol, spanRow, spanCol = 1, 1, 1, 6
    labelSprintMaster.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol)
    
    # display all cards
    display(cardStorage)
    
    # run   
    mainWindow.mainloop()

def createNewTaskWindow():

    def create():

        # Create/Connect to a database
        connect_db = sqlite3.connect('tasks.db')
        # Create cusror
        cursor = connect_db.cursor()
        
        # create table "tasks" in same dir if it does not exist locally
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tasks
                       ([task_name], [task_description], [stroy_points], [priority], [status], [assigned_to], [tag])
                       ''')
        
        # input data
        connect_db.execute("INSERT INTO tasks VALUES (:task_name, :task_description, :stroy_points, :priority, :status, :assigned_to, :tag)", 
                        {
                            'task_name': entry1.get(),
                            'task_description': entry2.get(),
                            'stroy_points': entry2.get(),
                            'priority': priority.get(),
                            'status': status.get(),
                            'assigned_to': assigned_to.get(),
                            'tag': tag.get()
                        }
                       
                            )
        
        # show card immediately after task creation
        currentTaskNumber = len(cardStorage)+1 # create the card
        create_task_card(cardStorage, currentTaskNumber, 
                         entry1.get(), entry2.get(), priority.get(), entry2.get(), status.get(),assigned_to.get())
        
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
    assigned_to['values'] = ('Chang Ong Lin', 'Lai Carson', 'Shyam Kamalesh Borkar', 'Tion Yue Khoo')
    assigned_to['state'] = 'readonly'
    assigned_to.current(0)
    assigned_to.place(x = 140, y = 200)

    current_tag = StringVar()
    tag = Combobox(frame, textvariable = current_tag)
    tag['values'] = ('UI', 'CALL', 'TESTING')
    tag['state'] = 'readonly'
    tag.current(0)
    tag.place(x = 140, y = 230)

    createButton = Button(frame, text = "Create", command = create)
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
                     DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign):
    # main frame for card
    mainFrame = Frame(MainWindow, width=280, height=200, highlightbackground="gray", highlightthickness=2)
    # card split into 9Rx8C; cells evenly sized
    for i in range(1, 10): #R1-R9
        mainFrame.grid_rowconfigure(i, weight=1, uniform = "cardrows")
    for i in range(2, 9-1): #C2-C8
        mainFrame.grid_columnconfigure(i, weight = 1, uniform = "cardcolumns")
    mainFrame.grid_propagate(0) # stop auto resize
    
    # print fields and buttons for card
    cardNum = Label(mainFrame, text = "Task ", font=("Arial" ,8, "bold"))
    cardEditTask = Button(mainFrame, text = "Edit", font=("Courier", 8), command = do_nothing)
    cardDelete = Button(mainFrame, text = "X", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF", command = do_nothing)
    cardDescName = Label(mainFrame, text = "Name: ", font=("Arial" ,8, "bold"))
    cardDescDesc = Label(mainFrame, text = "Description: ", font=("Arial" ,8, "bold"))
    cardDescPriority = Label(mainFrame, text = "Priority: ", font=("Arial" ,8, "bold"))
    cardDescPoints = Label(mainFrame, text = "Story Points: ", font=("Arial" ,8, "bold"))
    cardDescStatus = Label(mainFrame, text = "Status: ", font=("Arial" ,8, "bold"))
    cardDescAssign = Label(mainFrame, text = "Assigned to: ", font=("Arial" ,8, "bold"))
    
    # print variable data from database
    variableCardNum = Label(mainFrame, text = taskNumber, font=("Arial" ,8, "bold"))        
    variableDescName = Label(mainFrame, text = DescName)
    variableDescDesc = Label(mainFrame, text = DescDesc)
    variableDescPriority = Label(mainFrame, text = DescPriority)
    variableDescPoints = Label(mainFrame, text = DescPoints)
    for status in ["Not Started", "In Progress", "Complete"]:
        if DescStatus == status:
            variableDescStatus = Label(mainFrame, text = status)
            break
    variableDescAssign = Label(mainFrame, text = DescAssign)
    
    # position of fields and buttons within card
    frontSpace = Label(mainFrame, width=200, height=1, bg = "gray") # coloured status bar
    if DescStatus == "Not Started":
        frontSpace.config(fg = "#FF0000", bg = "#FF0000")
    elif DescStatus == "In Progress":
        frontSpace.config(fg = "#FFD800", bg = "#FFD800")
    elif DescStatus == "Complete":
        frontSpace.config(fg = "#3AFF00", bg = "#3AFF00")
    frontSpace.grid(row = 2, column = 1, columnspan = 8, padx = 3, pady = 3)
    
    cardNum.grid(row = 1, column = 2, columnspan = 1, padx = 2, pady = 2, sticky = "w")
    cardEditTask.grid(row = 1, column = 7, padx = 2, pady = 2, sticky = "e")
    cardDelete.grid(row = 1, column = 8, padx = 2, pady = 2, sticky = "w")
    cardDescName.grid(row = 3, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescDesc.grid(row = 4, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPriority.grid(row = 5, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPoints.grid(row = 6, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescStatus.grid(row = 7, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescAssign.grid(row = 8, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    
    # position of variables within card
    variableCardNum.grid(row = 1, column = 3, columnspan = 1, padx = 2, pady = 2, sticky = "w")
    variableDescName.grid(row = 3, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescDesc.grid(row = 4, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescPriority.grid(row = 5, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescPoints.grid(row = 6, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescStatus.grid(row = 7, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    variableDescAssign.grid(row = 8, column = 4, columnspan = 4, padx = 2, pady = 2, sticky = "w")
    
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
    taskNumber = 1
    for row in rows:
        DescName, DescDesc, DescPriority, DescPoints, DescStatus, DescAssign = row[0], row[1], row[3], row[2], row[4], row[5]
        create_task_card(cardArray, taskNumber, DescName, 
                         DescDesc, DescPriority, DescPoints, DescStatus, DescAssign)
        taskNumber += 1
    
    # display if cardArray not empty
    if cardArray:
        place_card(cardArray)
        
    connect_db.commit
    connect_db.close()
    
def do_nothing():
    pass

main()
