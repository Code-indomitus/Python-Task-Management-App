from email import message
from msilib.schema import ComboBox
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3

# TODO: tidy up code and add comments
# TODO: integrate cards with database

def main():
    
    # attributes
    cardStorage = []

    # create master window
    requiredRow = 8
    requiredCol = 6
    mainWindow = init_main_window("Sprint Master", "2000x630", requiredRow, requiredCol)
    
    # Shyam
    createTaskButton = Button(mainWindow, text = "Create New Task", command = createNewTaskWindow(mainWindow))
    filterLabel = Label(mainWindow ,text = "Filter: ") 
    current_tag = StringVar()
    tags = Combobox(mainWindow, textvariable = current_tag)

    tags['values'] = ('NONE','UI', 'CALL', 'TESTING')
    tags['state'] = 'readonly'
    tags.current(0)
    
    # create space in grid for C1
    space = Frame(mainWindow, width=50, height=50)
    spaceEnd = Frame(mainWindow, width=50, height=50)
    space.grid(row = 3, column = 1, padx = 3, pady = 3, sticky = "nw")
    spaceEnd.grid(row = 3, column = 6, padx = 3, pady = 3, sticky = "ne")

    startRow, startCol, spanRow, spanCol = 2, 5, 1, 1
    tags.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 4, 1, 1
    filterLabel.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "e")
    startRow, startCol, spanRow, spanCol = 2, 2, 1, 2
    createTaskButton.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol, sticky = "w")
    
    # create top label
    labelSprintMaster = add_label(mainWindow, "Sprint Master")
    startRow, startCol, spanRow, spanCol = 1, 1, 1, 6
    labelSprintMaster.grid(row = startRow, column = startCol, rowspan = spanRow, columnspan = spanCol)
    
    # add cards
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    create_task_card(mainWindow, cardStorage)
    
    # show cards
    place_card(cardStorage)
    
    # run   
    mainWindow.mainloop()

def createNewTaskWindow(mainWindow):

    def create():

        # Create/Connect to a database
        connect_db = sqlite3.connect('tasks.db')
        # Create cusror
        cursor = connect_db.cursor()
        
        # CARSON: create table "tasks" in same dir if it does not exist
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tasks
                       ([task_name], [task_description], [stroy_points], [priority], [status], [assigned_to], [tag])
                       ''')
        
        connect_db.commit
        
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
    newTaskWindow = Toplevel(mainWindow)
 
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

# first page
def new_page(title, size):
    newPage = Tk()
    newPage.title(title)
    newPage.geometry(size)
    return newPage

# add frame to array (TODO: replaced by card object later)
def add_frame(frameArray, thisFrame):
    frameArray.append(thisFrame)
    
# add label and position it
def add_label(page, displayText):
    newLabel = Label(page, text = displayText, bd = 5, padx = 3, pady = 3)
    return newLabel

# create card to represent a task in display
def create_task_card(window, cardStorage):
    # main frame for card
    mainFrame = Frame(window, bg = "gray", width=280, height=200)
    # card split into 5Rx8C; cells evenly sized
    for i in range(1, 8): #R1-R7
        mainFrame.grid_rowconfigure(i, weight=1, uniform = "cardrows")
    for i in range(2, 9-1): #C2-C7
        mainFrame.grid_columnconfigure(i, weight = 1, uniform = "cardcolumns")
    mainFrame.grid_propagate(0) # stop auto resize
    
    # print fields and buttons for card
    cardName = Label(mainFrame, text = "Task 1")
    cardName.config(font=("Courier", 8))
    cardStatus = Label(mainFrame, text = "..", font=("Courier", 8), bg = "#3AFF00", fg = "#3AFF00")
    cardEditTask = Button(mainFrame, text = "Edit", font=("Courier", 8))
    cardDelete = Button(mainFrame, text = "X", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF")
    cardDescName = Label(mainFrame, text = "Name: ")
    cardDescPriority = Label(mainFrame, text = "Priority: ")
    cardDescPoints = Label(mainFrame, text = "Story Points: ")
    cardDescStatus = Label(mainFrame, text = "Status: ")
    
    # position of fields and buttons within card
    frontSpace = Label(mainFrame, width=1, height=1, bg = "gray") #R2C1 space
    endSpace = Label(mainFrame, width=1, height=1, bg = "gray") # R2C8 space
    frontSpace.grid(row = 2, column = 1, padx = 3, pady = 3, sticky = "nw")
    endSpace.grid(row = 2, column = 8, padx = 3, pady = 3, sticky = "ne")
    
    cardName.grid(row = 1, column = 2, columnspan = 3, padx = 2, pady = 2, sticky = "w")
    cardStatus.grid(row = 1, column = 6, padx = 2, pady = 2, sticky = "e")
    cardEditTask.grid(row = 1, column = 7, padx = 2, pady = 2, sticky = "e")
    cardDelete.grid(row = 1, column = 8, padx = 2, pady = 2, sticky = "w")
    cardDescName.grid(row = 3, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPriority.grid(row = 4, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescPoints.grid(row = 5, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "w")
    cardDescStatus.grid(row = 6, column = 2, columnspan = 2, padx = 2, pady = 2, sticky = "nw")
    
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

main()
