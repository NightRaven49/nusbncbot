from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import sqlite3

#Deprecated, for reference only
buttons = ["FASS", "Business & Accountancy", "Computing", "Dentistry", "Engineering", "Law",
           "Medicine", "Science", "Halls/Residential Colleges", "Sports Facilities", "Others"]

def makeButtons(array):
    number = len(array)
    isEven = (number % 2 == 0)
    buttonList = []
    for i in range(0, number):
        buttonList.append(InlineKeyboardButton(array[i], callback_data = array[i]))
    newList = []
    for j in range(0, number // 2):
        newArray = []
        newArray.append(buttonList[2 * j])
        newArray.append(buttonList[2 * j + 1])
        newList.append(newArray)
    if not isEven:
        newList.append([buttonList[number - 1]])
    return newList

def start(update, context):
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT Category FROM BOTS")
    buttons = []
    for row in cursor:
        buttons.append(row[0])
    buttons = list(set(buttons))
    button_list = makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Here you can find " + 
    "many useful bots and announcement channels that you may find useful during your studies in " +
    "NUS. Please select from the custom keyboard the faculty you are interested in finding bots" +
    "/channels.", reply_markup=keyboard)
    conn.close()

def button(update, context):
    query = update.callback_query
    query.answer()
    reply = query.data
    backButton = [InlineKeyboardButton("Back", callback_data = "back")]
    if "@" in reply:
        keyboard = InlineKeyboardMarkup([backButton])
        query.edit_message_text(text=reply, reply_markup=keyboard)
    else:
        conn = sqlite3.connect('test.db')
        cursor = conn.execute("SELECT Username FROM BOTS WHERE Category = '{}'".format(reply))
        bots = []
        for row in cursor:
            bots.append(row[0])
        buttons = makeButtons(bots)
        buttons.append(backButton)
        if reply == "back":
            start(update, context)
        else:
            keyboard = InlineKeyboardMarkup(buttons)
            query.edit_message_text(text="Below is the list of available bots and channels in {}. "
            .format(reply) + "If there are none listed, work is in progress.", reply_markup=keyboard)
        conn.close()

def main():
    #Remember to remove token before commit
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
