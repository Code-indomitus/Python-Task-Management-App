import tkinter as tk
from tkinter import *

# root 
root = tk.Tk()

# master window
root.title("Sprint Master")
root.geometry("1000x500")

# CREATE FRAME
# w = frame( master, options)
frame1 = tk.Frame(root, bg = "cyan", width=200, height=200)
frame2 = tk.Frame(root, bg = "magenta", width=200, height=200)
frame3 = tk.Frame(root, bg = "yellow", width = 200, height=200)

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

frame1.grid(row = 0, rowspan = 1, pady = 5)
frame2.grid(row = 2, rowspan = 1, pady = 5)
frame3.grid(row = 4, rowspan = 1, stick = "n", pady = 5)

# label to add gap at top
#topGap = Label(root, text="hi")
#topGap.place(relx=0.5, anchor = 'n')

# run   
root.mainloop()