from tkinter import *
from tkinter import messagebox
import hashlib
import os

PASSWORD_FILE = "admin_password.txt"

# hasher
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- load or create password file
def loadPasswordHash():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w") as f:
            f.write(hashPassword("admin123"))
        return hashPassword("admin123")

    with open(PASSWORD_FILE, "r") as f:
        return f.read().strip()

def savePasswordHash(new_hash):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new_hash)

# stored admin password hash (NOW persistent)
currentAdminPasswordHash = loadPasswordHash()

def passwordWall(parentWindow, adminGUI):
    def passwordCheck():
        if hashPassword(entry.get()) == currentAdminPasswordHash:
            passwordWallWindow.destroy()
            parentWindow.destroy()
            adminGUI()
        else:
            messagebox.showerror("Error", "Wrong password")
            entry.delete(0, END)

    passwordWallWindow = Toplevel()
    passwordWallWindow.geometry("300x120")
    passwordWallWindow.title("Admin Login")

    Label(passwordWallWindow, text="Enter Admin Password:").pack(pady=5)
    entry = Entry(passwordWallWindow, show="*")
    entry.pack()
    Button(passwordWallWindow, text="Login", command=passwordCheck).pack(pady=5)

def changePassword():
    def submit():
        global currentAdminPasswordHash

        new_pass = entryPassword.get()
        if not new_pass:
            messagebox.showwarning("Warning", "Password cannot be empty")
            return

        new_hash = hashPassword(new_pass)
        savePasswordHash(new_hash)
        currentAdminPasswordHash = new_hash

        messagebox.showinfo("Success", "Password changed successfully")
        passwordWindow.destroy()

    passwordWindow = Toplevel()
    passwordWindow.geometry("300x120")
    passwordWindow.title("Change Admin Password")

    Label(passwordWindow, text="New Password:").pack(pady=5)
    entryPassword = Entry(passwordWindow, show="*")
    entryPassword.pack()
    Button(passwordWindow, text="Save", command=submit).pack(pady=5)
