import tkinter  as tk 
from tkcalendar import DateEntry
main_window = tk.Tk()
main_window.geometry("340x220")  

cal=DateEntry(main_window,selectmode='day')
cal.grid(row=1,column=1,padx=15)

main_window.mainloop()