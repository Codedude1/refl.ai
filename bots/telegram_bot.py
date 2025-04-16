import os 
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
API_URL = "http://127.0.0.1:8000/chat"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    payload = {"message": message.text}
    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()
        reply = f"Logged successfully! Entry ID: {data['data']['id']} (Type: {data['data']['log_type']})"
    except Exception as e:
        reply = f"Error logging message: {str(e)}"
    bot.reply_to(message, reply)

if __name__ == '__main__':
    bot.polling(non_stop=True)

