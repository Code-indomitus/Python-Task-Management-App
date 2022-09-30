import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

main_window = Tk()
main_window.title("SprintMaster")
main_window.geometry("800x600")


notebook = ttk.Notebook(main_window)
notebook.pack(pady = 15)

tab1 = Frame(notebook, width = 800, height = 600, bg = "pink")
tab2 = Frame(notebook, width = 800, height = 600, bg = "blue")
tab3 = Frame(notebook, width = 800, height = 600, bg = "purple")

tab1.pack(fill = "both", expand = 1)
tab2.pack(fill = "both", expand = 1)
tab3.pack(fill = "both", expand = 1)


def createNewTaskWindow():

    def createTask():
        # Create/Connect to a database
        connect_db = sqlite3.connect('tasks.db')
        # Create cusror
        cursor = connect_db.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks
                    ([task_name], [task_description], [story_points], [priority], [status], [assigned_to], [tag], [id])
                    ''')
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
    newTaskWindow = Toplevel(main_window)
 
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
    priority = ttk.Combobox(frame, textvariable = current_priority)
    priority['values'] = ('Low', 'Medium', 'High', 'Critical')
    priority['state'] = 'readonly'
    priority.current(0)
    priority.place(x = 140, y = 140)

    current_Status = StringVar()
    status = ttk.Combobox(frame, textvariable = current_Status)
    status['values'] = ('Not Started', 'In Progress', 'Complete')
    status['state'] = 'readonly'
    status.current(0)
    status.place(x = 140, y = 170)

    current_assigned_to = StringVar()
    assigned_to = ttk.Combobox(frame, textvariable = current_assigned_to)
    assigned_to['values'] = ('Chang Ong Lin', 'Lai Carson', 'Shyam Kamalesh Borkar', 'Tion Yue Khoo')
    assigned_to['state'] = 'readonly'
    assigned_to.current(0)
    assigned_to.place(x = 140, y = 200)

    current_tag = StringVar()
    tag = ttk.Combobox(frame, textvariable = current_tag)
    tag['values'] = ('UI', 'CALL', 'TESTING')
    tag['state'] = 'readonly'
    tag.current(0)
    tag.place(x = 140, y = 230)

    createButton = Button(frame, text = "Create", command = createTask)
    createButton.place(x = 125, y = 350)

    discardButton = Button(frame, text = "Close", command = newTaskWindow.destroy)
    discardButton.place(x = 225, y = 350)

def createNewSprintWindow():

    def createSprint():
        # Create/Connect to a database
        connect_db = sqlite3.connect('sprints.db')
        # Create cusror
        cursor = connect_db.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS sprints
                ([sprint_name], [start_date], [end_date])
                ''')

        connect_db.execute("INSERT INTO sprints VALUES (:sprint_name, :start_date, :end_date)", 
                        {
                            'sprint_name': sprint_name_entry.get(),
                            'start_date': start_date_entry.get_date().strftime("%m/%d/%Y"),
                            'end_date': end_date_entry.get_date().strftime("%m/%d/%Y")
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
    newSprintWindow = Toplevel(main_window)
 
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

createTaskButton = Button(tab1, text = "Create New Task", command = createNewTaskWindow)
createTaskButton.place(x = 20, y = 20)

createSprintButton = Button(tab2, text = "Create New Sprint", command = createNewSprintWindow)
createSprintButton.place(x = 20, y = 20)

notebook.add(tab1, text = "Task Board")
notebook.add(tab2, text = "Sprint Board")
notebook.add(tab3, text = "Team Board")

main_window.mainloop()
