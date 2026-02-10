import tkinter as tk
from tkinter import messagebox
from auth.user_db import create_user

def show_signup(on_success, on_login):
    win = tk.Toplevel()
    win.title("Register – Devil Will Cry")
    win.geometry("300x280")
    win.resizable(False, False)

    tk.Label(win, text="Create Account", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Password").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    tk.Label(win, text="Confirm Password").pack()
    confirm_entry = tk.Entry(win, show="*")
    confirm_entry.pack()

    def register():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if create_user(username, password):
            messagebox.showinfo("Success", "Account created")
            win.destroy()
            on_success(username)
        else:
            messagebox.showerror("Error", "User already exists")

    tk.Button(win, text="Register", width=15, command=register).pack(pady=10)

    tk.Button(
        win,
        text="Back to Login",
        width=15,
        command=lambda: [win.destroy(), on_login()]
    ).pack()

    win.grab_set()
