from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers import *

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

        CHOSE_BUTTON: [
            CallbackQueryHandler(button_show_nearest_location, pattern='show_nearest_location'),
            CallbackQueryHandler(ask_for_location_when_category_selected, pattern='category'),
            CallbackQueryHandler(start, pattern='to_main_menu'),
            CallbackQueryHandler(show_how_to_prepare_category, pattern='show_how_to_prepare_category')
            # CallbackQueryHandler(show_chosen_category, pattern='show_chosen_category'),
            # CallbackQueryHandler(add_point, pattern='add_point'),
            # CallbackQueryHandler(help_project, pattern='help_project'),
        ],

        SEND_LOCATION: [
            MessageHandler(Filters.location, process_location)
        ],
    },

    fallbacks=[CommandHandler('start', start)],

    per_message=False
)

# adding handler to the dispatcher
dispatcher.add_handler(conversation_handler)

# start asking the bot for inputs
updater.start_polling()
