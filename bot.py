from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import configparser
from handlers import *
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# config stores config.ini file content
config = configparser.ConfigParser()
config.read('config.ini')

# updater listens to user's inputs
updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)

# dispatcher process what updater sent to it
dispatcher = updater.dispatcher

# handlers definition
handler_start = CommandHandler('start', start)
handler_show_nearest_poin = CallbackQueryHandler(shot_nearest_point)

# adding handler to the dispatcher so that it can match input with the method to execute
dispatcher.add_handler(handler_start)
dispatcher.add_handler(handler_show_nearest_poin)

updater.start_polling()
