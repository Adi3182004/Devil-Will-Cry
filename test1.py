import os
from dotenv import load_dotenv
from emergency.telegram_bot import TelegramBot

load_dotenv()

bot = TelegramBot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    chat_id=os.getenv("TELEGRAM_CHAT_ID")
)

bot.send_text("🚨 TEST: Devil Will Cry Telegram working")
