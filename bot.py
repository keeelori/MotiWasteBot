from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import configparser
from handlers import *
import logging

# config is used to extract bot token
config = configparser.ConfigParser()
config.read('config.ini')

# updater listens to user's inputs
updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)

# dispatcher processes what updater sent to it
dispatcher = updater.dispatcher

# start of handlers definition section
# matching start command with function to execute
handler_start = CommandHandler('start', start)

# callback query is what returned by pressing InlineKeyboardButton. Matching each button shown on /start command with
# function to execute
handler_show_nearest_point = CallbackQueryHandler(show_nearest_point, pattern='show_nearest_point')
handler_show_how_to_prepare = CallbackQueryHandler(show_how_to_prepare, pattern='show_how_to_prepare')
handler_add_point = CallbackQueryHandler(add_point, pattern='add_point')
handler_help_project = CallbackQueryHandler(help_project, pattern='help_project')

# matching each button for waste type with function to execute

# end of handlers definition section

# adding handler to the dispatcher
dispatcher.add_handler(handler_start)
dispatcher.add_handler(handler_show_nearest_point)
dispatcher.add_handler(handler_show_how_to_prepare)
dispatcher.add_handler(handler_add_point)
dispatcher.add_handler(handler_help_project)

updater.start_polling()
