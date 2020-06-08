from telegram.ext import Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from modules import commands as com

def makeButtons(array):
    number = len(array)
    isEven = (number % 2 == 0)
    buttonList = [InlineKeyboardButton(array[i], callback_data = array[i]) for i in range(0, number)]
    newList = []
    for j in range(0, number // 2):
        newArray = []
        newArray.append(buttonList[2 * j])
        newArray.append(buttonList[2 * j + 1])
        newList.append(newArray)
    if not isEven:
        newList.append([buttonList[number - 1]])
    return newList

def button(update, context):
    query = update.callback_query
    query.answer()
    reply = query.data
    backButton = [InlineKeyboardButton("Back", callback_data = "back")]
    if "@" in reply:
        keyboard = InlineKeyboardMarkup([backButton, [InlineKeyboardButton("Home", callback_data =
            "home")]])
        query.edit_message_text(text = reply, reply_markup = keyboard)
    else:
        conn = sqlite3.connect('modules/test.db')
        cursor = conn.execute("SELECT Username FROM BOTS WHERE Category = '{}'".format(reply))
        bots = [row[0] for row in cursor]
        buttons = makeButtons(bots)
        buttons.append(backButton)
        if reply == "back":
            com.start(update, context)
        elif reply == "home":
            com.start(update, context)
        else:
            keyboard = InlineKeyboardMarkup(buttons)
            query.edit_message_text(text = "Below is the list of available bots and channels in {}. "
            .format(reply) + "If there are none listed, work is in progress.", reply_markup = keyboard)
        conn.close()

