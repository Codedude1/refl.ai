# bots/echo_chat_id.py
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def send_back_chat_id(m):
    chat_id = m.chat.id
    bot.reply_to(m, f"Your chat_id is: {chat_id}")

if __name__ == "__main__":
    print("Starting echo bot. Send any message to get your chat_id...")
    bot.polling(non_stop=True)
