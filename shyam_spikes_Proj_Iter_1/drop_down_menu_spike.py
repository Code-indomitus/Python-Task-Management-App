from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

mainWindow = Tk()
current = StringVar()
items = Combobox(mainWindow, textvariable = current)
items['values'] = ['h', 'e', 'l', 'p']
items.current(0)
items['state'] = 'readonly'
mainWindow.title("DropDown List")
mainWindow.mainloop()
