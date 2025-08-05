import sqlite3
from tkinter import *
from tkinter import messagebox
from db import connect_db, init_db

class AuthWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.master.title("Login / Sign Up")
        self.master.geometry("400x400")
        self.master.config(bg="blue")
        self.on_login_success = on_login_success
        init_db()
        self.show_login()

    def show_login(self):
        self.clear_window()
        Label(self.master, text="Login", font=("Arial Black", 20), bg="white").place(x=150, y=30)

        Label(self.master, text="Username:", bg="white").place(x=50, y=100)
        self.login_username = Entry(self.master)
        self.login_username.place(x=150, y=100)

        Label(self.master, text="Password:", bg="white").place(x=50, y=140)
        self.login_password = Entry(self.master, show="*")
        self.login_password.place(x=150, y=140)

        Button(self.master, text="Login", bg="green", fg="white",
               command=self.login_user).place(x=150, y=180)

        Label(self.master, text="Don't have an account?", bg="white").place(x=100, y=230)
        Button(self.master, text="Sign Up", command=self.show_signup, bg="black", fg="white").place(x=240, y=225)

    def show_signup(self):
        self.clear_window()
        Label(self.master, text="Sign Up", font=("Arial Black", 20), bg="white").place(x=140, y=30)

        Label(self.master, text="Username:", bg="white").place(x=50, y=90)
        self.signup_username = Entry(self.master)
        self.signup_username.place(x=150, y=90)

        Label(self.master, text="Password:", bg="white").place(x=50, y=130)
        self.signup_password = Entry(self.master, show="*")
        self.signup_password.place(x=150, y=130)

        Label(self.master, text="Role:", bg="white").place(x=50, y=170)
        self.role_var = StringVar(value="User")
        OptionMenu(self.master, self.role_var, "User", "Admin").place(x=150, y=165)

        Button(self.master, text="Register", bg="yellow", fg="black",
               command=self.register_user).place(x=150, y=210)

        Label(self.master, text="Already have an account?", bg="white").place(x=90, y=260)
        Button(self.master, text="Login", command=self.show_login).place(x=250, y=255)

    def login_user(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            messagebox.showinfo("Login Success", f"Welcome {username} ({role})")
            self.on_login_success(username, role)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_user(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully.")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        conn.close()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()