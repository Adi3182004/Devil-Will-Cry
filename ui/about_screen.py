import tkinter as tk

def show_about():
    win = tk.Toplevel()
    win.title("About Devil Will Cry")
    win.geometry("400x250")

    text = (
        "Devil Will Cry\n\n"
        "An offline-first women safety system\n"
        "with real-time evidence capture,\n"
        "location sharing, and emergency alerts.\n\n"
        "Created by:\n"
        "Aditya Andhalkar\n\n"
        "Purpose: Save lives, not just log data."
    )

    tk.Label(win, text=text, justify="left").pack(padx=20, pady=20)
