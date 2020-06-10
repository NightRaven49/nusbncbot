from telegram.ext import Updater
from telegram import ChatAction
import time
from modules import buttonMethods as bm

def start(update, context):
    chatID = update.effective_chat.id
    welcomeText = open("modules/Welcome.txt", "r")
    context.bot.send_message(chat_id = chatID, text = welcomeText.read())
    welcomeText.close()
    context.bot.send_chat_action(chat_id= chatID, action = ChatAction.TYPING)
    time.sleep(2)
    bm.welcome(update, context)

def helpMe(update, context):
    helpText = open("modules/Help.txt", "r")
    context.bot.send_message(chat_id = update.effective_chat.id, text = helpText.read())
