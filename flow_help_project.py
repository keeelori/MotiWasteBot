from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from conversation_states import *

def button_help_project(update, context):
    button = [
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]  # add common button
    ]
    reply_markup = InlineKeyboardMarkup(button)

    update.message.reply_text(text="Пункт прийому більше не працює? Хочеш допомогти проєкту? Ти можеш написати нам на пошту yehor.kuzmin@motiwaste.org або у телеграмі @yehorkuzmin", reply_markup=reply_markup)

    return FLOW_HELP_PROJECT
