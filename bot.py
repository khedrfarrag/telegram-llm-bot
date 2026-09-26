import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
MODEL = os.getenv("MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت شغال ✅ (NVIDIA Nemotron) — اكتبلي أي حاجة")

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        resp = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": message.text}],
                "temperature": 0.7,
                "max_tokens": 4096
            },
            timeout=60
        )
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"خطأ: {e}"
    bot.reply_to(message, reply)

bot.infinity_polling()