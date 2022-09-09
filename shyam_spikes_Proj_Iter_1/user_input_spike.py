from tkinter import *

mainWindow = Tk()
frame = Frame(mainWindow, width = 300, height = 200)
frame.pack()

label1 = Label(frame, text = "Username")
label1.place(x = 30, y = 50)

label2 = Label(frame, text = "Password")
label2.place(x = 30, y = 80)

entry1 = Entry(frame)
entry2 = Entry(frame)
entry1.place(x = 100, y = 50)
entry2.place(x = 100, y = 80)

button = Button(frame, text = "Enter", command = mainWindow.destroy)
button.place(x = 140, y = 140)

mainWindow.title("User Input")
mainWindow.mainloop()
