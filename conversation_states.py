from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


# states of conversation
MAIN_MENU, FLOW_SHOW_NEAREST_LOCATION, SEND_LOCATION, FLOW_SHOW_HOW_TO_PREPARE, FLOW_ADD_POINT, FLOW_HELP_PROJECT = range(6)

# method to execute for '/start' command
def start(update, context):
    # buttons to display under the welcome message
    buttons = [[
        InlineKeyboardButton(text='Найближчий пункт приймоу', callback_data='button_show_nearest_location')],
        [InlineKeyboardButton(text='Як підготувати сміття до утлізації', callback_data='button_show_how_to_prepare')],
        [InlineKeyboardButton(text='Додати пункт прийому вторсировини', callback_data='button_add_point')],
        [InlineKeyboardButton(text='Допомогти проекту', callback_data='button_help_project')
         ]]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /start action
    update.effective_message.reply_text('Чим можу бути корисним?', reply_markup=reply_markup)

    return MAIN_MENU