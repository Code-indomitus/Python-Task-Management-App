from doctest import master
import tkinter as tk
import math
from tkinter import *
from turtle import color

def new_page(title, size):
    newPage = tk.Tk()
    newPage.title(title)
    newPage.geometry(size)
    return newPage

root = new_page("Card Display Spike", "2000x1500")

# tasks
card1 = Frame(root, bg = "cyan", width=160, height=200)
card2 = Frame(root, bg = "magenta", width=160, height=200)

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(6, weight=1)

card1.grid(row = 1, column = 1, padx = 20, pady = 10)
card2.grid(row = 2, column = 2, padx = 20, pady = 10)

# information to display
card1TaskName = Label(card1, text = "Task 1")
card1TaskName.config(font=("Courier", 8))
card1Status = Label(card1, text = "S", font=("Courier", 8), fg = "#FF0000")
card1Edit = Button(card1, text = "Edit", font=("Courier", 8))
card1Delete = Button(card1, text = "X", font=("Arial", 8, "bold"), bg = "#FF0000", fg = "#FFFFFF")
card1NameDesc = Label(card1, text = "Name: ")
card1PriorityDesc = Label(card1, text = "Priority: ")
card1PointsDesc = Label(card1, text = "Story Points: ")
card1StatusDesc = Label(card1, text = "Status: ")

# place in grid layout
card1TaskName.grid(row = 1, column = 1, columnspan = 1, padx = 3, pady = 2, sticky = "w")
card1Status.grid(row = 1, column = 2, columnspan = 1, sticky = "w")
card1Edit.grid(row = 1, column = 3, columnspan = 1, padx = 2, sticky = "e")
card1Delete.grid(row = 1, column = 4, columnspan = 1, padx = 2, sticky = "e")
card1NameDesc.grid(row = 2, column = 1, columnspan = 1, padx = 2, pady = 2, sticky = "w")
card1PriorityDesc.grid(row = 3, column = 1, columnspan = 1, padx = 2, pady = 2, sticky = "w")
card1PointsDesc.grid(row = 4, column = 1, columnspan = 1, padx = 2, pady = 2, sticky = "w")
card1StatusDesc.grid(row = 5, column = 1, columnspan = 1, padx = 2, pady = 2, sticky = "nw")

# create task display
card1.grid_rowconfigure(5, weight = 1)
card1.grid_columnconfigure(4, weight = 1)
card1.grid_propagate(0) # stop auto resize

root.mainloop()