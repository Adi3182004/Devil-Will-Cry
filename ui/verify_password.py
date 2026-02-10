import tkinter as tk
from tkinter import messagebox
from auth.user_db import verify_user

def verify_password(username, on_success):
    win = tk.Toplevel()
    win.title("Confirm Identity")
    win.geometry("300x180")
    win.resizable(False, False)

    tk.Label(
        win,
        text="Confirm Password to Cancel Emergency",
        wraplength=260,
        font=("Arial", 11, "bold")
    ).pack(pady=10)

    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

    def confirm():
        password = password_entry.get()
        if verify_user(username, password):
            win.destroy()
            on_success()
        else:
            messagebox.showerror("Access Denied", "Incorrect password")

    tk.Button(win, text="Verify", width=15, command=confirm).pack(pady=10)

    win.grab_set()
