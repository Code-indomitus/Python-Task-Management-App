from email import message
from msilib.schema import ComboBox
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3

def main():
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
    
    mainWindow.mainloop()

def createNewTaskWindow(mainWindow):

    def create():

        # Create/Connect to a database
        connect_db = sqlite3.connect('tasks.db')
        # Create cusror
        cursor = connect_db.cursor()
        
        # CARSON: create table "tasks" in same dir if it does not exist
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS test
                       ([task_name], [task_description], [stroy_points], [priority], [status], [assigned_to], [tag])
                       ''')
        
        connect_db.commit
        
        # input data
        connect_db.execute("INSERT INTO test VALUES (:task_name, :task_description, :stroy_points, :priority, :status, :assigned_to, :tag)", 
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
    
def init_main_window(title, size, splitRow, splitCol):
    main = new_page(title,size)
    # breakdown window into cells in a grid (splitRow x splitCol)
    main.grid_rowconfigure(splitRow, weight = 1)
    main.grid_columnconfigure(splitCol, weight = 1)
    return main

def new_page(title, size):
    newPage = Tk()
    newPage.title(title)
    newPage.geometry(size)
    return newPage

main()