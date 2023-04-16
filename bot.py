from telegram.ext import Application, Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from flow_show_nearest_location import *
from flow_show_how_to_prepare import *
from flow_add_point import *
from flow_help_project import *
from flow_entry import *

# config is used to extract bot token
config = configparser.ConfigParser()
config.read('config.ini')

# updater listens to user's inputs
#updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)

application = Application.builder().token(config['APP']['TELEGRAM_TOKEN']).build()

# dispatcher processes what updater sent to it
#dispatcher = updater.dispatcher


# callback query is what returned by pressing InlineKeyboardButton. Here we match each button shown on /start command
# with function to execute
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={

        MAIN_MENU: [
            CallbackQueryHandler(button_show_nearest_location, pattern='button_show_nearest_location'),
            CallbackQueryHandler(button_show_how_to_prepare, pattern='button_show_how_to_prepare'),
            CallbackQueryHandler(button_add_point, pattern='button_add_point'),
            CallbackQueryHandler(button_help_project, pattern='button_help_project')
        ],

        FLOW_SHOW_NEAREST_LOCATION: [
            CallbackQueryHandler(ask_for_location_when_category_selected, pattern='category'),
            CallbackQueryHandler(show_how_to_prepare_category, pattern='show_how_to_prepare_category'),
            CallbackQueryHandler(start, pattern='to_main_menu')
        ],

        SEND_LOCATION: [
            MessageHandler(filters._Location, process_location),
            CallbackQueryHandler(show_gif_how_to_send_location, pattern='how_to_send_location')
        ],

        FLOW_SHOW_HOW_TO_PREPARE: [
            CallbackQueryHandler(show_category_when_it_selected, pattern='category')
        ],

        FLOW_ADD_POINT: [
            CallbackQueryHandler(start, pattern='to_main_menu')
        ],

        FLOW_HELP_PROJECT: [
            CallbackQueryHandler(start, pattern='to_main_menu')
        ]
    },

    fallbacks=[CommandHandler('start', start)],

    per_message=False
)

# adding handler to the dispatcher
#dispatcher.add_handler(conversation_handler)

# start asking the bot for inputs
#updater.start_polling()

application.add_handler(conversation_handler)
application.run_polling()
