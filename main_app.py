from tkinter import *
from guest_gui import guestGUI
from admin_gui import adminGUI
from passwords_and_checking import passwordWall

# First Window to Show
loginWindow = Tk()
loginWindow.geometry('300x100')
loginWindow.title('Library Entrance')

def passworldWallAndDestroy():
    passwordWall(loginWindow, adminGUI)

def guestguiAndDestroy():
    guestGUI(loginWindow)

loginAdmin = Button(loginWindow, text='Admin', command=passworldWallAndDestroy)
loginAdmin.pack(pady=5)

loginUser = Button(loginWindow, text='Guest', command=guestguiAndDestroy)
loginUser.pack(pady=5)

loginWindow.mainloop()
