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
# matching start command with function to execute
handler_start = CommandHandler('start', start)

# callback query is what returned by pressing InlineKeyboardButton.
handler_show_nearest_point = CallbackQueryHandler(show_nearest_point, pattern='show_nearest_point')

# adding handler to the dispatcher
dispatcher.add_handler(handler_start)
dispatcher.add_handler(handler_show_nearest_point)

updater.start_polling()
