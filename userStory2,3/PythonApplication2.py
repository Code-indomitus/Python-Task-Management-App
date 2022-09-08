
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x300")

l1 = ttk.Label(root, text = "Name")
l2 = ttk.Label(root, text = "Description")
l3 = ttk.Label(root, text = "Story Point")
l4 = ttk.Label(root, text = "Priority")
l5 = ttk.Label(root, text = "Status")
l6 = ttk.Label(root, text = "Assigned To")
l7 = ttk.Label(root, text = "Tag")

l1.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
l2.grid(row = 2, column = 0, sticky = tk.W, pady = 2)
l3.grid(row = 3, column = 0, sticky = tk.W, pady = 2)
l4.grid(row = 4, column = 0, sticky = tk.W, pady = 2)
l5.grid(row = 5, column = 0, sticky = tk.W, pady = 2)
l6.grid(row = 6, column = 0, sticky = tk.W, pady = 2)
l7.grid(row = 7, column = 0, sticky = tk.W, pady = 2)

var = tk.StringVar()
var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()
var5 = tk.StringVar()
var6 = tk.StringVar()

var.set('hello')
var1.set('hello')
var2.set('hello')
var3.set('hello')
var4.set('hello')
var5.set('hello')
var6.set('hello')

t1 = ttk.Label(root, textvariable=var)
t2 = ttk.Label(root, textvariable=var1)
t3 = ttk.Label(root, textvariable=var2)
t4 = ttk.Label(root, textvariable=var3)
t5 = ttk.Label(root, textvariable=var4)
t6 = ttk.Label(root, textvariable=var5)
t7 = ttk.Label(root, textvariable=var6)

t1.grid(row = 1, column = 1, pady=5, sticky = tk.W)
t2.grid(row = 2, column = 1, pady=5, sticky = tk.W)
t3.grid(row = 3, column = 1, pady=5, sticky = tk.W)
t4.grid(row = 4, column = 1, pady=5, sticky = tk.W)
t5.grid(row = 5, column = 1, pady=5, sticky = tk.W)
t6.grid(row = 6, column = 1, pady=5, sticky = tk.W)
t7.grid(row = 7, column = 1, pady=5, sticky = tk.W)

def changeWord():
    newWindow = tk.Toplevel(root)
    newWindow.geometry("300x300")
    newWindow.title("edit task")
    
    ll1 = ttk.Label(newWindow, text = "Name")
    ll2 = ttk.Label(newWindow, text = "Description")
    ll3 = ttk.Label(newWindow, text = "Story Point")
    ll4 = ttk.Label(newWindow, text = "Priority")
    ll5 = ttk.Label(newWindow, text = "Status")
    ll6 = ttk.Label(newWindow, text = "Assigned To")
    ll7 = ttk.Label(newWindow, text = "Tag")

    ll1.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
    ll2.grid(row = 2, column = 0, sticky = tk.W, pady = 2)
    ll3.grid(row = 3, column = 0, sticky = tk.W, pady = 2)
    ll4.grid(row = 4, column = 0, sticky = tk.W, pady = 2)
    ll5.grid(row = 5, column = 0, sticky = tk.W, pady = 2)
    ll6.grid(row = 6, column = 0, sticky = tk.W, pady = 2)
    ll7.grid(row = 7, column = 0, sticky = tk.W, pady = 2)

    tt1 = ttk.Entry(newWindow,  textvariable = var)
    tt2 = ttk.Entry(newWindow,  textvariable = var1)
    tt3 = ttk.Entry(newWindow,  textvariable = var2)
    tt4 = ttk.Combobox(newWindow,  textvariable = var3)
    tt5 = ttk.Combobox(newWindow,  textvariable = var4)
    tt6 = ttk.Combobox(newWindow,  textvariable = var5)
    tt7 = ttk.Combobox(newWindow,  textvariable = var6)

    tt1.grid(row = 1, column = 1, pady=5, sticky = tk.W)
    tt2.grid(row = 2, column = 1, pady=5, sticky = tk.W)
    tt3.grid(row = 3, column = 1, pady=5, sticky = tk.W)
    tt4.grid(row = 4, column = 1, pady=5, sticky = tk.W)
    tt5.grid(row = 5, column = 1, pady=5, sticky = tk.W)
    tt6.grid(row = 6, column = 1, pady=5, sticky = tk.W)
    tt7.grid(row = 7, column = 1, pady=5, sticky = tk.W)

    tt4['values'] = ('High','Medium','Low')
    tt5['values'] = ('Not Started','In progress','Complete')
    tt6['values'] = ('a','b','c')
    tt7['values'] = ('d','e','f')


B = tk.Button(root, text ="edit", command = changeWord)
B.grid(row = 0, column = 2, sticky = tk.E)

def delete():
    list = root.grid_slaves()
    for l in list:
        l.destroy()


B1 = tk.Button(root, text ="delete", command = delete)
B1.grid(row = 0, column = 3, sticky = tk.E)

root.mainloop() # the window is now displayed
