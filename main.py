import tkinter as tk
import threading
import socket
import sys
import time
import os

from core.state_manager import StateManager, SystemState
from core.countdown import CountdownTimer

from emergency.location_service import LocationService
from emergency.email_alert import EmailAlert
from emergency.telegram_bot import TelegramBot
from emergency.gsm_sms import GSMSender
from emergency.gsm_call import GSMCaller

from audio.recorder import AudioRecorder
from vision.camera_recorder import CameraRecorder

from auth.user_db import init_db, has_user, verify_user
from ui.login_screen import show_login
from ui.signup_screen import show_signup
from ui.profile_screen import show_profile
from ui.about_screen import show_about

# ================= INIT ================= #

init_db()

state_manager = StateManager()
countdown_timer = None
emergency_fired = False
current_user = None

emergency_stop_event = threading.Event()

location_service = LocationService()
email_alerts = EmailAlert()

telegram = TelegramBot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    chat_id=os.getenv("TELEGRAM_CHAT_ID")
)

audio_recorder = AudioRecorder(duration=10)
camera_recorder = CameraRecorder()

gsm_sms = GSMSender(port="COM5")
gsm_call = GSMCaller(port="COM5")

PAUSE_DURATION = 5

# ================= NETWORK ================= #

def internet_available(timeout=3):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False

# ================= EVIDENCE LOOP ================= #

def evidence_loop():
    while True:
        print("[EVIDENCE] Cycle START")

        image_path = camera_recorder.capture_once()
        audio_path = audio_recorder.record()

        # 🚨 ALWAYS SEND CURRENT EVIDENCE
        if image_path:
            telegram.send_photo(image_path)

        if audio_path:
            telegram.send_audio(audio_path)

        email_alerts.send(
            subject="🚨 Emergency Evidence – Devil Will Cry",
            message="New emergency evidence captured.",
            attachments=[image_path, audio_path]
        )

        print("[EVIDENCE] Cycle END")

        # 🔐 Stop ONLY AFTER evidence is sent
        if emergency_stop_event.is_set():
            print("[EVIDENCE] Stop requested → exiting safely")
            break

        for _ in range(PAUSE_DURATION):
            if emergency_stop_event.is_set():
                break
            time.sleep(1)

# ================= EMERGENCY ================= #

def emergency_mode():
    global emergency_fired, countdown_timer

    if emergency_fired:
        return

    emergency_fired = True
    countdown_timer = None
    emergency_stop_event.clear()

    state_manager.set_state(SystemState.EMERGENCY)
    update_status("EMERGENCY")

    location = location_service.get_location()

    alert_message = (
        "🚨 EMERGENCY ALERT 🚨\n\n"
        f"City: {location['city']}\n"
        f"Region: {location['region']}\n"
        f"Country: {location['country']}\n\n"
        f"{location['maps']}"
    )

    if internet_available():
        telegram.send_text(alert_message)
        email_alerts.send(
            subject="🚨 EMERGENCY ALERT – Devil Will Cry",
            message=alert_message
        )
        threading.Thread(target=evidence_loop, daemon=True).start()
    else:
        gsm_sms.send_sms("+917887547146", location["maps"])
        gsm_call.call_number("+917887547146")

# ================= COUNTDOWN ================= #

def start_countdown():
    global countdown_timer, emergency_fired

    if countdown_timer:
        return

    emergency_fired = False
    state_manager.set_state(SystemState.RISK_DETECTED)
    update_status("RISK")

    def on_tick(sec):
        root.after(
            0,
            lambda: countdown_label.config(
                text=f"Emergency in {sec} seconds"
            )
        )

    countdown_timer = CountdownTimer(
        seconds=10,
        on_timeout=emergency_mode,
        on_tick=on_tick
    )
    countdown_timer.start()

# ================= CANCEL (PASSWORD VERIFIED) ================= #

def cancel_emergency():
    if not current_user:
        return

    win = tk.Toplevel(root)
    win.title("Confirm Cancel")
    win.geometry("300x180")
    win.resizable(False, False)

    tk.Label(
        win,
        text="Enter password to cancel emergency",
        font=("Arial", 11, "bold"),
        wraplength=260
    ).pack(pady=10)

    pwd_entry = tk.Entry(win, show="*")
    pwd_entry.pack(pady=5)

    def confirm():
        global countdown_timer, emergency_fired

        if not verify_user(current_user, pwd_entry.get()):
            tk.messagebox.showerror("Denied", "Incorrect password")
            return

        # 🔐 request safe stop AFTER this cycle
        emergency_stop_event.set()

        if countdown_timer:
            countdown_timer.cancel()
            countdown_timer = None

        emergency_fired = False
        state_manager.set_state(SystemState.IDLE)
        update_status("IDLE")
        countdown_label.config(text="Countdown: --")

        win.destroy()

    tk.Button(win, text="Confirm", width=15, command=confirm).pack(pady=10)
    win.grab_set()

# ================= UI HELPERS ================= #

def update_status(text):
    status_label.config(text=f"Status: {text}")

def on_emergency_click():
    if state_manager.is_idle():
        start_countdown()

def on_quit():
    emergency_stop_event.set()
    root.destroy()
    sys.exit(0)

def logout():
    global current_user
    emergency_stop_event.set()
    current_user = None
    root.withdraw()
    launch_auth_flow()

# ================= AUTH FLOW ================= #

def after_login(user):
    global current_user
    current_user = user
    root.deiconify()

def launch_login():
    show_login(on_success=after_login, on_signup=launch_signup)

def launch_signup():
    show_signup(on_success=after_login, on_login=launch_login)

def launch_auth_flow():
    if has_user():
        launch_login()
    else:
        launch_signup()

# ================= TK UI ================= #

root = tk.Tk()
root.title("Devil Will Cry")
root.geometry("420x300")
root.resizable(False, False)

menu = tk.Menu(root)
root.config(menu=menu)

menu.add_command(label="Profile", command=lambda: show_profile(current_user))
menu.add_command(label="About", command=show_about)
menu.add_command(label="Logout", command=logout)

tk.Label(root, text="Devil Will Cry", font=("Arial", 20, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Status: IDLE", font=("Arial", 12))
status_label.pack(pady=5)

tk.Button(
    root,
    text="EMERGENCY",
    bg="red",
    fg="white",
    font=("Arial", 16, "bold"),
    width=15,
    command=on_emergency_click
).pack(pady=20)

countdown_label = tk.Label(root, text="Countdown: --", font=("Arial", 14))
countdown_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Cancel", width=10, command=cancel_emergency).pack(side="left", padx=10)
tk.Button(frame, text="Quit", width=10, command=on_quit).pack(side="right", padx=10)

# ================= START ================= #

root.withdraw()
launch_auth_flow()
root.mainloop()
