import telebot
import os
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8270816155:AAHAks-iyvybbt7q9IkCA69ut7uuzpT0S50"
bot = telebot.TeleBot(BOT_TOKEN)

# --- Main menu ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔹 Start", "🌐 Your IP")
    markup.row("🔍 Find IP", "📤 Share")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to the IP Info Bot!\n\nSelect an option below:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    if text == "🔹 Start":
        bot.send_message(message.chat.id, "Hi! I'm your IP info bot 😊", reply_markup=main_menu())

    elif text == "🌐 Your IP":
        # Use ipinfo.io to detect IP
        try:
            ip = requests.get("https://api.ipify.org").text
            info = requests.get(f"https://ipinfo.io/{ip}/json").json()
            result = (
                f"🌍 **Your IP Info:**\n\n"
                f"IP: {info.get('ip')}\n"
                f"City: {info.get('city')}\n"
                f"Region: {info.get('region')}\n"
                f"Country: {info.get('country')}\n"
                f"Org: {info.get('org')}\n"
            )
            bot.send_message(message.chat.id, result, parse_mode="Markdown")
        except:
            bot.send_message(message.chat.id, "❌ Could not fetch your IP info.")

    elif text == "🔍 Find IP":
        bot.send_message(message.chat.id, "🔎 Send me any IP address to find its info.")
        bot.register_next_step_handler(message, find_ip)

    elif text == "📤 Share":
        bot.send_message(message.chat.id, "📩 Share this bot with friends!\n\n👉 t.me/@Ipaddress34344_bot")

    else:
        bot.send_message(message.chat.id, "Please use the buttons below.", reply_markup=main_menu())


def find_ip(message):
    ip = message.text.strip()
    try:
        info = requests.get(f"https://ipinfo.io/{ip}/json").json()
        result = (
            f"🌍 **IP Info:**\n\n"
            f"IP: {info.get('ip')}\n"
            f"City: {info.get('city')}\n"
            f"Region: {info.get('region')}\n"
            f"Country: {info.get('country')}\n"
            f"Org: {info.get('org')}\n"
        )
        bot.send_message(message.chat.id, result, parse_mode="Markdown", reply_markup=main_menu())
    except:
        bot.send_message(message.chat.id, "❌ Invalid IP or error fetching info.", reply_markup=main_menu())

import os

if __name__ == "__main__":
    bot.polling(non_stop=True, skip_pending=True)
