# main.py
from tkinter import Tk
from auth import AuthWindow
from user_interface import open_user_interface
from admin_dashbord import open_admin_dashboard

def on_login_success(username, role):
    root.destroy()  # Close the login/signup window

    if role == "User":
        open_user_interface(username)
    elif role == "Admin":
        open_admin_dashboard(username)

# Start the login/signup screen
root = Tk()
app = AuthWindow(root, on_login_success)
root.mainloop()