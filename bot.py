from telegram.ext import Updater, CommandHandler
import configparser

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()