from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# define a method to execute for '/start' command
def start(update, context):
    # buttons to display under the bot's message
    buttons = [[
        InlineKeyboardButton(text='Найближчий пункт приймоу', callback_data='show_nearest_point')],
        [InlineKeyboardButton(text='Як підготувати сміття до утлізації', callback_data='show_how_to_prepare')],
        [InlineKeyboardButton(text='Додати пункт прийому вторсировини', callback_data='add_point')],
        [InlineKeyboardButton(text='Допомогти проекту', callback_data='help_project')
         ]]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)

    # send message on /start action
    update.message.reply_text('Чим можу бути корисним?', reply_markup=reply_markup)


def shot_nearest_point(update, contect):
    query = update.callback_query

    query.edit_message_text(text="test")
