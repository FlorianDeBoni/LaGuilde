import requests
import telebot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from ..models import *

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
    return send_message(
        "Here are the available commands:\n/help: Display available commands\n/give i : Validate that you gave the command n°i\n/end i : End the command n°i")


@bot.message_handler(commands=['give'])
def give(message):
    args = message.text.split()[1:]
    numbers = []
    for i in args:
        try:
            numbers.append(int(i))
        except:
            pass
    for index in numbers:
        try:
            command = Command.objects.get(message_id=index)
            for game in command.games.all():
                game.quantity = 0
                game.save()
            command.is_active = True
            command.save()
            send_message("You gave the command n°"+str(index))
        except:
            pass


@bot.message_handler(commands=['end'])
def end(message):
    args = message.text.split()[1:]
    numbers = []
    for i in args:
        try:
            numbers.append(int(i))
        except:
            pass
    for index in numbers:
        try:
            command = Command.objects.get(message_id=index)
            for game in command.games.all():
                game.quantity = 1
                game.save()
            command.is_active = False
            command.wait = False
            command.save()
            send_message("End of the command n°"+str(index))
        except:
            pass


# bot.polling()
