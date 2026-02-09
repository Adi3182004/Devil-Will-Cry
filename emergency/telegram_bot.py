import requests
import os

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_text(self, message):
        try:
            r = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message
                },
                timeout=5
            )
            if r.status_code == 200:
                print("[TELEGRAM] Text alert sent")
            else:
                print("[TELEGRAM] Text failed:", r.text)
        except Exception as e:
            print("[TELEGRAM] Error:", e)

    def send_photo(self, image_path):
        if not image_path or not os.path.exists(image_path):
            return
        try:
            with open(image_path, "rb") as img:
                requests.post(
                    f"{self.base_url}/sendPhoto",
                    data={"chat_id": self.chat_id},
                    files={"photo": img},
                    timeout=10
                )
                print("[TELEGRAM] Image sent")
        except Exception as e:
            print("[TELEGRAM] Image failed:", e)

    def send_audio(self, audio_path):
        if not audio_path or not os.path.exists(audio_path):
            return
        try:
            with open(audio_path, "rb") as audio:
                requests.post(
                    f"{self.base_url}/sendAudio",
                    data={"chat_id": self.chat_id},
                    files={"audio": audio},
                    timeout=15
                )
                print("[TELEGRAM] Audio sent")
        except Exception as e:
            print("[TELEGRAM] Audio failed:", e)
