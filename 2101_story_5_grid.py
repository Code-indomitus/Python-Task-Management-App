import tkinter as tk
import math
from tkinter import *\
    
# TODO: add a new page if first page cannot display all frames
    
# functions
# application
def main():
    
    # attributes
    frameArray = []

    # root 
    root = tk.Tk()

    # master window
    root.title("Sprint Master")
    root.geometry("1000x500")

    # CREATE FRAME
    # w = frame( master, options)
    masterFrame = Frame(root, bg = "gray", width=1000, height=500)
    frame1 = Frame(masterFrame, bg = "cyan", width=100, height=100)
    frame2 = Frame(masterFrame, bg = "magenta", width=100, height=100)
    frame3 = Frame(masterFrame, bg = "yellow", width=100, height=100)
    frame4 = Frame(masterFrame, bg = "red", width=100, height=100)
    frame5 = Frame(masterFrame, bg = "green", width=100, height=100)
    frame6 = Frame(masterFrame, bg = "blue", width=100, height=100)
    frame7 = Frame(masterFrame, bg = "pink", width=100, height=100)
    frame8 = Frame(masterFrame, bg = "white", width=100, height=100)
    frame9 = Frame(masterFrame, bg = "black", width=100, height=100)

    # ADD FRAME
    # TODO: replace with object's .add() method
    addFrame(frameArray, frame1)
    addFrame(frameArray, frame2)
    addFrame(frameArray, frame3)
    addFrame(frameArray, frame4)
    addFrame(frameArray, frame5)
    addFrame(frameArray, frame6)
    addFrame(frameArray, frame7)
    addFrame(frameArray, frame8)
    addFrame(frameArray, frame9)
    
    # determine amount of rows and cols required to display all cards
    requiredRows = math.ceil(math.sqrt(len(frameArray)))
    requiredCols = math.ceil(math.sqrt(len(frameArray)))

    # set grid
    root.grid_rowconfigure(requiredRows, weight=1)
    root.grid_columnconfigure(requiredCols, weight=1)
    
    # set master frame's position
    masterFrame.grid(row = 2, column = 2, rowspan = requiredRows, columnspan = requiredCols, padx = 10, pady = 10)
    
    # set each child frame in master frame
    currRowspan = 1
    currPadY = 5
    currPadX = 5
    for col in range(0, requiredCols):
        for row in range(0, requiredRows):
            frameArray[row + col*3].grid(row = row, column = col, rowspan = currRowspan, 
                                         padx = currPadX, pady = currPadY)

    # run   
    root.mainloop()

# add frame to array (TODO: replaced by card object later)
def addFrame(frameArray, thisFrame):
    frameArray.append(thisFrame)
    
main()