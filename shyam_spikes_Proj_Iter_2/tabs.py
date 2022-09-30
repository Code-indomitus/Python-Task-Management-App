from tkinter import *
from tkinter import ttk

main_window = Tk()
main_window.title("SprintMaster")
main_window.geometry("500x500")


notebook = ttk.Notebook(main_window)
notebook.pack(pady = 15)

tab1 = Frame(notebook, width = 500, height = 500, bg = "pink")
tab2 = Frame(notebook, width = 500, height = 500, bg = "blue")
tab3 = Frame(notebook, width = 500, height = 500, bg = "purple")

tab1.pack(fill = "both", expand = 1)
tab2.pack(fill = "both", expand = 1)
tab3.pack(fill = "both", expand = 1)

notebook.add(tab1, text = "Task Board")
notebook.add(tab2, text = "Sprint Board")
notebook.add(tab3, text = "Team Board")

main_window.mainloop()


