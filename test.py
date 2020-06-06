from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import logging

buttons = ["FASS", "Business & Accountancy", "Computing", "Dentistry", "Engineering", "Law",
           "Medicine", "Science", "Halls/Residential Colleges", "Sports Facilities", "Others"]
comp = ["SOC Announcements", "CS1101S Attendance Bot", "TeleSource"]

def makeButtons(array):
    number = len(array)
    isEven = (number % 2 == 0)
    i = 0
    buttonList = []
    while i < number:
        buttonList.append(InlineKeyboardButton(array[i], callback_data = array[i]))
        i += 1
    newList = []
    for i in range(0, number // 2):
        newArray = []
        newArray.append(buttonList[2 * i])
        newArray.append(buttonList[2 * i + 1])
        newList.append(newArray)
    if not isEven:
        newList.append([buttonList[number - 1]])
    return newList

def start(update, context):
    button_list = makeButtons(buttons)
    keyboard = InlineKeyboardMarkup(button_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Here you can find " + 
    "many useful bots and announcement channels that you may find useful during your studies in " +
    "NUS. Please select from the custom keyboard the faculty you are interested in finding bots" +
    "/channels.", reply_markup=keyboard)

def button(update, context):
    query = update.callback_query
    query.answer()
    reply = query.data
    if reply == "Computing":
        buttons = makeButtons(comp)
        keyboard = InlineKeyboardMarkup(buttons)
        query.edit_message_text(text = "abc", reply_markup=keyboard)
    else:
        query.edit_message_text(text="Selected option: {}".format(query.data))

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
