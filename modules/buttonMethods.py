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
    username = conn.execute("SELECT USERNAME FROM BOTS WHERE NAME = '{}'".format(reply)).fetchall()
    link = conn.execute("SELECT LINK FROM ANNOUNCEMENT WHERE NAME = '{}'".format(reply)).fetchall()
    if len(username) + len(link) == 0:
        bots = conn.execute("SELECT NAME FROM BOTS WHERE CATEGORY = '{}'".format(reply))
        announce = conn.execute("SELECT NAME FROM ANNOUNCEMENT WHERE CATEGORY = '{}'".format(reply))
        total = [row[0] for row in bots]
        announce = [row[0] for row in announce]
        for i in range(0, len(total)):
            if total[i] == None:
               total[i] = "Placeholder Bot ({})".format(reply)
        total.extend(announce)
        buttons = makeButtons(total)
        buttons.append(backButton)
        if reply == "back":
            welcome(update, context)
        elif reply == "home":
            welcomeagain(query, conn)
        else:
            keyboard = InlineKeyboardMarkup(buttons)
            query.edit_message_text(text = "Below is the list of available bots and channels in {}. "
            .format(reply) + "If there are none listed, work is in progress.", reply_markup = keyboard)
    else:
        hit(username, link, query, conn, backButton[0])
    conn.close()

def hit(username, link, query, conn, back):
    keyboard = InlineKeyboardMarkup([[back, InlineKeyboardButton("Home", callback_data =
        "home")]])
    if len(username) == 1:
        username = username[0][0]
        desc = conn.execute("SELECT DESCRIPTION FROM BOTS WHERE USERNAME = '{}'".format(username)).fetchall()
        query.edit_message_text(text = username + "\n" + desc[0][0] , reply_markup = keyboard)
    else:
        link = link[0][0]
        query.edit_message_text(text = link, reply_markup = keyboard)

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

def welcomeagain(query, conn):
    cursor = conn.execute("SELECT CAT FROM CATEGORY")
    buttons = [row[0] for row in cursor]
    button_list = makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    welcomeText = open("modules/L1.txt", "r")
    query.edit_message_text(text = welcomeText.read(), reply_markup = keyboard)
    welcomeText.close()
