from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
import logging

buttons = ["FASS", "Business & Accountancy", "Computing", "Dentistry", "Engineering", "Law",
           "Medicine", "Science", "Halls/Residential Colleges", "Sports Facilities", "Others"]

def makeButtons(array):
    number = len(array)
    isEven = (number % 2 == 0)
    buttonList = [KeyboardButton(s) for s in array]
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
    keyboard = ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Here you can find " + 
    "many useful bots and announcement channels that you may find useful during your studies in " +
    "NUS. Please select from the custom keyboard the faculty you are interested in finding bots" +
    "/channels", reply_markup=keyboard)

def regMes(update, context):
    content = update.message.text
    finished = False
    for cat in buttons:
        if content == cat:
            reply(update.effective_chat.id, context)
            finished = True
            break
        else:
            continue
    if not finished:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, unsupported text.")

def reply(chatID, context):
    context.bot.send_message(chat_id=chatID, text="Work in Progress.")

def main():
    #Remember to remove token before commit
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), regMes))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
