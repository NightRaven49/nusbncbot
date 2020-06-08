from telegram.ext import Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from modules import buttonMethods as bm

def start(update, context):
    conn = sqlite3.connect('modules/test.db')
    cursor = conn.execute("SELECT Category FROM BOTS")
    buttons = list(set([row[0] for row in cursor]))
    button_list = bm.makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    welcomeText = open("modules/Welcome.txt", "r")
    context.bot.send_message(chat_id = update.effective_chat.id, text = welcomeText.read(),
            reply_markup = keyboard)
    conn.close()
    welcomeText.close()

def helpMe(update, context):
    helpText = open("modules/Help.txt", "r")
    context.bot.send_message(chat_id = update.effective_chat.id, text = helpText.read())
