from telegram.ext import Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

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
    conn = sqlite3.connect('modules/test2.db')
    cursor = conn.execute("SELECT USERNAME FROM BOTS WHERE NAME = '{}'".format(reply)).fetchall()
    if len(cursor) != 0:
        username = cursor[0][0]
        keyboard = InlineKeyboardMarkup([[backButton[0], InlineKeyboardButton("Home", callback_data =
            "home")]])
        desc = conn.execute("SELECT DESCRIPTION FROM BOTS WHERE USERNAME = '{}'".format(username)).fetchall()
        query.edit_message_text(text = username + "\n" + desc[0][0] , reply_markup = keyboard)
    else:
        newCursor = conn.execute("SELECT NAME FROM BOTS WHERE CATEGORY = '{}'".format(reply))
        bots = [row[0] for row in newCursor]
        for i in range(0, len(bots)):
            if bots[i] == None:
               bots[i] = "Placeholder Bot ({})".format(reply)
        buttons = makeButtons(bots)
        buttons.append(backButton)
        if reply == "back":
            welcome(update, context)
        elif reply == "home":
            welcome(update, context)
        else:
            keyboard = InlineKeyboardMarkup(buttons)
            query.edit_message_text(text = "Below is the list of available bots and channels in {}. "
            .format(reply) + "If there are none listed, work is in progress.", reply_markup = keyboard)
        conn.close()

def welcome(update, context):
    conn = sqlite3.connect('modules/test2.db')
    cursor = conn.execute("SELECT CAT FROM CATEGORY")
    buttons = [row[0] for row in cursor]
    button_list = makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    welcomeText = open("modules/L1.txt", "r")
    context.bot.send_message(chat_id = update.effective_chat.id, text = welcomeText.read(),
            reply_markup = keyboard)
    conn.close()
    welcomeText.close()
