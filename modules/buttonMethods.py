from telegram.ext import Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

back1 = [InlineKeyboardButton("Back", callback_data = "home")]
back2 = InlineKeyboardButton("Back", callback_data = "back")

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
    conn = sqlite3.connect('modules/test2.db')
    if reply == "home":
        welcomeagain(query, conn)
    elif reply == "back":
        username = query.message.text.partition('\n')[0]
        if "@" in username:
            cat = conn.execute("SELECT CATEGORY FROM BOTS WHERE USERNAME = '{}'".format(username)).fetchall()
        else:
            cat = conn.execute("SELECT CATEGORY FROM ANNOUNCEMENT WHERE LINK = '{}'".format(username)).fetchall()
        level2(query, conn, cat[0][0])
    else:
        username = conn.execute("SELECT USERNAME FROM BOTS WHERE NAME = '{}'".format(reply)).fetchall()
        link = conn.execute("SELECT LINK FROM ANNOUNCEMENT WHERE NAME = '{}'".format(reply)).fetchall()
        if len(username) + len(link) == 0:
            level2(query, conn, reply)
        else:
            hit(username, link, query, conn)
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
    welcomeText.close()

def welcomeagain(query, conn):
    cursor = conn.execute("SELECT CAT FROM CATEGORY")
    buttons = [row[0] for row in cursor]
    button_list = makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    welcomeText = open("modules/L1.txt", "r")
    query.edit_message_text(text = welcomeText.read(), reply_markup = keyboard)
    welcomeText.close()

def level2(query, conn, reply):
    bots = conn.execute("SELECT NAME FROM BOTS WHERE CATEGORY = '{}'".format(reply))
    announce = conn.execute("SELECT NAME FROM ANNOUNCEMENT WHERE CATEGORY = '{}'".format(reply))
    total = [row[0] for row in bots]
    announce = [row[0] for row in announce]
    for i in range(0, len(total)):
        if total[i] == None:
            total[i] = "Placeholder Bot ({})".format(reply)
    total.extend(announce)
    buttons = makeButtons(total)
    buttons.append(back1)
    keyboard = InlineKeyboardMarkup(buttons)
    l2 = open("modules/L2.txt", "r")
    query.edit_message_text(text = l2.read().format(reply), reply_markup = keyboard)
    
def hit(username, link, query, conn):
    keyboard = InlineKeyboardMarkup([[back2, InlineKeyboardButton("Home", callback_data ="home")]])
    if len(username) == 1:
        username = username[0][0]
        desc = conn.execute("SELECT DESCRIPTION FROM BOTS WHERE USERNAME = '{}'".format(username)).fetchall()
        query.edit_message_text(text = username + "\n" + desc[0][0] , reply_markup = keyboard)
    else:
        link = link[0][0]
        query.edit_message_text(text = link, reply_markup = keyboard)
