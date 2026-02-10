import tkinter as tk
from tkinter import messagebox
from auth.user_db import verify_user

def show_login(on_success, on_signup):
    win = tk.Toplevel()
    win.title("Login – Devil Will Cry")
    win.geometry("300x240")
    win.resizable(False, False)

    tk.Label(win, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Password").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if verify_user(username, password):
            win.destroy()
            on_success(username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(win, text="Login", width=15, command=login).pack(pady=10)

    tk.Button(
        win,
        text="Sign Up",
        width=15,
        command=lambda: [win.destroy(), on_signup()]
    ).pack()

    win.grab_set()
