from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import logging

buttons = ["FASS", "Business & Accountancy", "Computing", "Dentistry", "Engineering", "Law",
           "Medicine", "Science", "Halls/Residential Colleges", "Sports Facilities", "Others"]
comp = ["SOC Announcements", "CS1101S Attendance Bot", "TeleSource"]

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
    backButton = [[InlineKeyboardButton("Back", callback_data = "back")]]
    if reply == "Computing":
        buttons = makeButtons(comp)
        buttons.append(backButton[0])
        keyboard = InlineKeyboardMarkup(buttons)
        query.edit_message_text(text = "Below is the list of available bots and channels in {}."
                .format(reply), reply_markup=keyboard)
    elif reply == "back":
        start(update, context)
    else:
        keyboard = InlineKeyboardMarkup(backButton)
        query.edit_message_text(text="Below is the list of available bots and channels in {}. "
        .format(reply) + "If there are none listed, work is in progress.", reply_markup=keyboard)

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
