import requests
import telebot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

TOKEN = "7072024752:AAErtw68EfM0JJl5nY1y41vekFvGW-W0F4U"
chat_id = "-4133824685"
bot = telebot.TeleBot(TOKEN)


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    return requests.get(url).json()['result']['message_id']


def edit_message(text, message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/EditMessageText?chat_id={chat_id}&message_id={message_id}&text={text}"
    requests.get(url)


def delete_message(message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/DeleteMessage?chat_id={chat_id}&message_id={message_id}"
    requests.get(url)

# message_id = send_message("Message\nrl")
# print(message_id)
# edit_message("Editons", message_id)
# delete_message(message_id)


@bot.message_handler(commands=['help'])
def help(message):
    args = message.text.split()[1:]
    send_message(
        "Here are the available commands:\n/help: Display available commands\n")


bot.polling()
