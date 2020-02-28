from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from flow_show_nearest_location import *
from flow_show_how_to_prepare import *

# config is used to extract bot token
config = configparser.ConfigParser()
config.read('config.ini')

# updater listens to user's inputs
updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)

# dispatcher processes what updater sent to it
dispatcher = updater.dispatcher


# callback query is what returned by pressing InlineKeyboardButton. Here we match each button shown on /start command
# with function to execute
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={

        MAIN_MENU: [
            CallbackQueryHandler(button_show_nearest_location, pattern='button_show_nearest_location'),
            CallbackQueryHandler(button_show_how_to_prepare, pattern='button_show_how_to_prepare')
        ],

        FLOW_SHOW_NEAREST_LOCATION: [
            CallbackQueryHandler(ask_for_location_when_category_selected, pattern='category'),
            CallbackQueryHandler(show_how_to_prepare_category, pattern='show_how_to_prepare_category'),
            CallbackQueryHandler(start, pattern='to_main_menu')
        ],

        SEND_LOCATION: [
            MessageHandler(Filters.location, process_location)
        ],

        FLOW_SHOW_HOW_TO_PREPARE: [
            CallbackQueryHandler(show_category_when_it_selected, pattern='category')
        ]
    },

    fallbacks=[CommandHandler('start', start)],

    per_message=False
)

# adding handler to the dispatcher
dispatcher.add_handler(conversation_handler)

# start asking the bot for inputs
updater.start_polling()
