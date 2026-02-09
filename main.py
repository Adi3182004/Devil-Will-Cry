from core.state_manager import StateManager, SystemState
from core.countdown import CountdownTimer

from emergency.location_service import LocationService
from emergency.email_alert import EmailAlert
from emergency.telegram_bot import TelegramBot
from emergency.gsm_sms import GSMSender
from emergency.gsm_call import GSMCaller

from audio.recorder import AudioRecorder
from vision.camera_recorder import CameraRecorder

import socket
import threading
import sys
import time
import os

state_manager = StateManager()
countdown_timer = None
emergency_fired = False

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


def internet_available(timeout=3):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False


def evidence_loop():
    while state_manager.is_emergency():
        print("[EVIDENCE] Cycle START")

        image_path = camera_recorder.capture_once()
        audio_path = audio_recorder.record()

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
        time.sleep(PAUSE_DURATION)


def emergency_mode():
    global emergency_fired

    if emergency_fired:
        return

    emergency_fired = True
    state_manager.set_state(SystemState.EMERGENCY)
    print("🚨 EMERGENCY MODE ACTIVATED 🚨")

    location = location_service.get_location()

    alert_message = (
        "🚨 EMERGENCY ALERT 🚨\n\n"
        "System: Devil Will Cry\n"
        "Victim: Aditya Andhalkar\n\n"
        f"City: {location['city']}\n"
        f"Region: {location['region']}\n"
        f"Country: {location['country']}\n"
        f"ISP: {location['isp']}\n\n"
        f"Live Location:\n{location['maps']}"
    )

    if internet_available():
        telegram.send_text(alert_message)
        email_alerts.send(
            subject="🚨 EMERGENCY ALERT – Devil Will Cry",
            message=alert_message
        )
        threading.Thread(target=evidence_loop, daemon=True).start()
    else:
        gsm_sms.send_sms(
            "+917887547146",
            f"EMERGENCY! Help needed.\n{location['maps']}"
        )
        gsm_call.call_number("+917887547146")


def start_countdown():
    global countdown_timer, emergency_fired

    if countdown_timer or not state_manager.is_idle():
        return

    emergency_fired = False
    print("[SYSTEM] Countdown started (10 seconds)")
    state_manager.set_state(SystemState.RISK_DETECTED)

    countdown_timer = CountdownTimer(10, emergency_mode)
    countdown_timer.start()


def cancel_emergency():
    global countdown_timer, emergency_fired

    if state_manager.is_risk() and countdown_timer:
        countdown_timer.cancel()
        countdown_timer = None
        emergency_fired = False
        state_manager.set_state(SystemState.IDLE)
        print("[SYSTEM] Emergency cancelled")


def keyboard_listener():
    while True:
        cmd = input("Press P to panic | C to cancel | Q to quit: ").strip().lower()
        if cmd == "p" and state_manager.is_idle():
            start_countdown()
        elif cmd == "c":
            cancel_emergency()
        elif cmd == "q":
            shutdown()


def shutdown():
    print("[SYSTEM] Shutdown")
    sys.exit(0)


if __name__ == "__main__":
    print("Devil Will Cry system started")
    print("System is IDLE. Awaiting manual trigger.")

    try:
        keyboard_listener()
    except KeyboardInterrupt:
        shutdown()
