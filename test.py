from telegram.ext import Updater, CommandHandler
import logging

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="start text")

def main():
    updater = Updater(token="""token""", use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
