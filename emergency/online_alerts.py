from emergency.telegram_bot import TelegramBot

class OnlineAlerts:
    def __init__(self):
        self.telegram = TelegramBot(
            token="8527240038:AAF_FXL-jtBGLmThpqIYo74cCOLqvmGpKHE",
            chat_id="1245787494"
        )
        self.sent = False

    def send_emergency_alert(self, message):
        if self.sent:
            return
        self.telegram.send_alert(message)
        self.sent = True

    def reset(self):
        self.sent = False
