import tkinter  as tk 
from tkcalendar import DateEntry
main_window = tk.Tk()
main_window.geometry("340x220")  

cal=DateEntry(main_window,selectmode='day')
cal.grid(row=1,column=1,padx=15)

date = cal.get_date()
date = date.strftime("%m/%d/%Y")
print(date)
print(type(date))
main_window.mainloop()