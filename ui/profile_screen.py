import tkinter as tk

def show_profile(user_name, email):
    win = tk.Toplevel()
    win.title("Profile")
    win.geometry("300x200")

    tk.Label(win, text=f"Name: {user_name}").pack(pady=10)
    tk.Label(win, text=f"Email: {email}").pack(pady=10)
