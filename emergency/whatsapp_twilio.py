import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

class WhatsAppAlert:
    def __init__(self):
        self.sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_FROM")
        self.to_number = os.getenv("TWILIO_WHATSAPP_TO")

        if not all([self.sid, self.token, self.from_number, self.to_number]):
            self.client = None
        else:
            self.client = Client(self.sid, self.token)

    def send(self, message):
        if not self.client:
            print("[WHATSAPP] Twilio not configured")
            return

        try:
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            print("[WHATSAPP] Alert sent")
        except Exception as e:
            print("[WHATSAPP] Failed:", e)
