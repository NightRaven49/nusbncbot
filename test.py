from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import sqlite3
from modules import commands as com
from modules import buttonMethods as bm

#Deprecated, for reference only
buttons = ["FASS", "Business & Accountancy", "Computing", "Dentistry", "Engineering", "Law",
           "Medicine", "Science", "Halls/Residential Colleges", "Sports Facilities", "Others"]

def regMes(update, context):
    textRes = open("modules/Text.txt", "r")
    context.bot.send_message(chat_id = update.effective_chat.id, text = textRes.read())
    textRes.close()

def main():
    #Remember to remove token before commit
    updater = Updater(token = 'TOKEN', use_context = True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level =
            logging.INFO)

    dispatcher.add_handler(CommandHandler("start", com.start))
    dispatcher.add_handler(CommandHandler("help", com.helpMe))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), regMes))
    dispatcher.add_handler(CallbackQueryHandler(bm.button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
