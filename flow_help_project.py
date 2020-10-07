from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from conversation_states import *

def button_help_project(update, context):
    button = [
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]  # add common button
    ]
    reply_markup = InlineKeyboardMarkup(button)

    update.effective_message.reply_text(text="Ти можеш на написати нам пошту team.motiwaste@gmail.com або у телеграмі @yehorkuzmin", reply_markup=reply_markup)

    return FLOW_HELP_PROJECT
