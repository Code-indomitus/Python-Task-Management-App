from email import message
import math
from msilib.schema import ComboBox
from queue import Empty
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3


mainWindow = Tk()
mainWindow.geometry('800x600')
mainWindow.title("SPRINT BOARD")


def createNewSprintWindow():

    def create():
        # Create/Connect to a database
        connect_db = sqlite3.connect('sprints.db')
        # Create cusror
        cursor = connect_db.cursor()

        connect_db.execute("INSERT INTO tasks VALUES (:sprint_name, :start_date, :end_date)", 
                        {
                            'sprint_name': sprint_name_entry.get(),
                            'start_date': start_date_entry.get(),
                            'end_date': end_date_entry.get(),
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
    newSprintWindow = Toplevel(mainWindow)
 
    # sets the title of the
    # Toplevel widget
    newSprintWindow.title("New Sprint")
 
    # sets the geometry of toplevel
    newSprintWindow.geometry("300x300")


    frame = Frame(newSprintWindow, width = 400, height = 400)
    frame.pack()

    sprint_name = Label(frame, text = "Sprint Name:")
    sprint_name.place(x = 20, y = 50)

    start_date = Label(frame, text = "Start Date:")
    start_date.place(x = 20, y = 90)

    end_date = Label(frame, text = "End Date:")
    end_date.place(x = 20, y = 140)

    sprint_name_entry = Entry(frame, width = 25)
    start_date_entry = Entry(frame, width = 25)
    end_date_entry = Entry(frame, width = 25)
    sprint_name_entry.place(x = 110, y = 50)
    start_date_entry.place(x = 110, y = 90)
    end_date_entry.place(x = 110, y = 140)


    createButton = Button(frame, text = "Create Sprint", command = create)
    createButton.place(x = 125, y = 290)

    discardButton = Button(frame, text = "Discard Sprint", command = newSprintWindow.destroy)
    discardButton.place(x = 225, y = 290)

createSprintButton = Button(mainWindow, text = "Create New Sprint", command = createNewSprintWindow)


createSprintButton.place(x = 20, y = 20)

mainWindow.mainloop()
