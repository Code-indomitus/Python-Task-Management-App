from doctest import master
import tkinter as tk
import math
from tkinter import *\
    
# TODO: add a new page if first page cannot display all frames
# TODO: refactor code blocks in main() as functions
# TODO: masterFrame does not seem to move, probably .grid() and .pack() issue
    
# functions
# application
def main():
    
    # attributes
    frameArray = []

    # create master window
    root = new_page("Sprint Master", "1000x500")
    
    # create top label
    add_label(root, "Sprint Master", 500, 10)

    # CREATE FRAME
    # w = frame( master, options)
    masterFrame = Frame(root, bg = "gray", width=400, height=400)
    frame1 = Frame(masterFrame, bg = "cyan", width=100, height=100)
    frame2 = Frame(masterFrame, bg = "magenta", width=100, height=100)
    frame3 = Frame(masterFrame, bg = "yellow", width=100, height=100)
    frame4 = Frame(masterFrame, bg = "red", width=100, height=100)
    frame5 = Frame(masterFrame, bg = "green", width=100, height=100)
    frame6 = Frame(masterFrame, bg = "blue", width=100, height=100)
    frame7 = Frame(masterFrame, bg = "pink", width=100, height=100)
    frame8 = Frame(masterFrame, bg = "white", width=100, height=100)
    frame9 = Frame(masterFrame, bg = "black", width=100, height=100)
    frame10 = Frame(masterFrame, bg = "orange", width=100, height=100)
    #masterFrame.place(anchor = "w")

    # ADD FRAME
    # TODO: replace with object's .add() method
    add_frame(frameArray, frame1)
    add_frame(frameArray, frame2)
    add_frame(frameArray, frame3)
    add_frame(frameArray, frame4)
    add_frame(frameArray, frame5)
    add_frame(frameArray, frame6)
    add_frame(frameArray, frame7)
    add_frame(frameArray, frame8)
    add_frame(frameArray, frame9)
    add_frame(frameArray, frame10)
    
    # determine amount of rows and cols required to display all cards and initialise card display
    requiredRowsDisplay, requiredColsDisplay = init_task_display_dimensions(root, frameArray)        
    
    # set master frame's position
    masterFrame.grid(row = 2, column = 2, rowspan = requiredRowsDisplay, columnspan = requiredColsDisplay, padx = 10, pady = 10)
    
    # set each child frame in master frame
    currRowspan = 1
    currPadY = 5
    currPadX = 15
    for row in range(0, requiredRowsDisplay):
        for col in range(0, requiredColsDisplay):
            try:
                frameArray[col + row*4].grid(row = row, column = col, rowspan = currRowspan, 
                                         padx = currPadX, pady = currPadY)
            except:
                break # nothing else to print in last row

    # run   
    root.mainloop()

# first page
def new_page(title, size):
    newPage = tk.Tk()
    newPage.title(title)
    newPage.geometry(size)
    return newPage

# add frame to array (TODO: replaced by card object later)
def add_frame(frameArray, thisFrame):
    frameArray.append(thisFrame)
    
# add label and position it
def add_label(page, displayText, _x, _y):
    newLabel = Label(page, text = displayText, bd = 5, padx = 3, pady = 3)
    newLabel.place(x = _x,y = _y)
    
# initialise frame to display all cards
def init_task_display_dimensions(page, arrayOfFrames):
    # determine amount of rows and cols required to display all cards
    # rows
    if len(arrayOfFrames)//4 > 1: # more than one row needed
        requiredRows = len(arrayOfFrames) // 4
        if len(arrayOfFrames)%4 != 0: # partial row needed
            requiredRows += 1
    # cols
    requiredCols = 4
    # set the grid 
    page.grid_rowconfigure(requiredRows, weight=1)
    page.grid_columnconfigure(requiredCols, weight=1)
    return requiredRows, requiredCols
    
main()