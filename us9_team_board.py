''' User Story 9: Team Board.
Contains all UI elements and functions related to the team board.
'''
# Written by: Lai Carson, Shyam Borkar
# Last modified: 04/10/2022

from tkinter import *
import sqlite3

def init_team_board(root):
    ''' Initialise team board. '''
    
    # frame storing buttons at top
    buttonFrame = Frame(root, height = 20, width = 1100)
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
    memberTableFrame = Frame(root, height = 450, width = 1000)
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
    
def add_member_window(root):

    def add_member():
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

    # Toplevel object which will
    # be treated as a new window
    addMemberWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    addMemberWindow.title("Add Member")
 
    # sets the geometry of toplevel
    addMemberWindow.geometry("400x200")


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
   