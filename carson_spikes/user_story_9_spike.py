''' Spike for User Story 9. Creation of Team Board UI. '''
# Written by: Lai Carson
# Last modified: 04/10/2022

from tkinter import *

def init_team_board(root):
    ''' Initialise team board. '''
    
    # frame storing buttons at top
    buttonFrame = Frame(root, height = 20, width = 1200, bg = "cyan")
    buttonFrame.grid_rowconfigure(1, weight = 1)
    buttonFrame.grid_columnconfigure(3, weight = 1)
    buttonFrame.grid_propagate(False)
    buttonFrame.grid(row = 1, column = 1, pady = (30, 10))
    
    # "+"
    plusButton = Button(buttonFrame, text = "+", font = ("Arial", 12), width = 1, height = 5)
    plusButton.grid(row = 1, column = 1, sticky = W)
    
    # "Add Team Member"
    addMemberButton = Button(buttonFrame, text = "Add Team Member", width = 16, height = 4)
    addMemberButton.grid(row = 1, column = 2, sticky = W)
    
    # "Dashboard"
    dashboardButton = Button(buttonFrame, text = "Dashboard", width = 10, height = 4)
    dashboardButton.grid(row = 1, column = 3, sticky = E)
    
    # table listing members of sprint
    memberTableFrame = Frame(root, height = 450, width = 1000, bg = "magenta")
    memberTableFrame.grid_rowconfigure(10, weight = 1)
    memberTableFrame.grid_columnconfigure(4, weight = 1)
    memberTableFrame.grid_propagate(False)
    memberTableFrame.grid(row = 2, column = 1, sticky = "")
    
    # headers for table
    nameHeader = Label(memberTableFrame, text = "NAME", font = ("Roboto", 9, "bold")
                       , width = 52, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    nameHeader.grid(row = 1, column = 1, sticky = W+E)
    
    emailHeader = Label(memberTableFrame, text = "EMAIL", font = ("Roboto", 9, "bold")
                       , width = 60, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    emailHeader.grid(row = 1, column = 2, sticky = W+E)
    
    analyticsHeader = Label(memberTableFrame, text = "ANALYTICS", font = ("Roboto", 9, "bold")
                       , width = 20, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    analyticsHeader.grid(row = 1, column = 3, sticky = W+E)
    
    deleteHeader = Label(memberTableFrame, text = "", font = ("Roboto", 9, "bold")
                       , width = 5, height = 2, bg = "white",
                       highlightbackground = "black", highlightthickness = 1)
    deleteHeader.grid(row = 1, column = 4, sticky = W+E)

# main window
root = Tk()
root.geometry("500x500")
root.title("Team Board UI")

root.grid_rowconfigure(2, weight = 1)
root.grid_columnconfigure(1, weight = 1)

init_team_board(root)

root.mainloop()