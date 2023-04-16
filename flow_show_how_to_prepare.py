from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from conversation_states import *
from db_connection import *


# method to execute on show_nearest_point button click
def button_show_how_to_prepare(update, context):
    # extracting each category name and creating an array of buttons with callback_data = type
    buttons = []

    # extracting categories from db and creating buttons for each of them
    all_categories = db.categories.find()
    for category in all_categories:
        buttons.append(
            [InlineKeyboardButton(text=category['name'], callback_data='category_' + category['type'])])

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message with categories as inline buttons
    update.message.reply_text(text="Що здаємо на переробку?", reply_markup=reply_markup)

    return FLOW_SHOW_HOW_TO_PREPARE


def show_category_when_it_selected(update, context):
    selected_category_type = update.callback_query.data.partition('_')[2]
    context.user_data['selected_category_type'] = selected_category_type

    selected_category = db.categories.find_one({'type': selected_category_type})

    button = [
        [InlineKeyboardButton(text='Хочу здати', callback_data='category_' + selected_category['type'])]
    ]

    reply_markup = InlineKeyboardMarkup(button)

    update.message.reply_text(  # add formatters
        'Як підготувати сміття категорії *{}* до переробки:\n\n{}\n\n✅{}\n\n❌{}\n\nℹ️{}'.format(
            selected_category['name'],
            selected_category['description'],
            selected_category['do'],
            selected_category['dont'],
            selected_category['steps']),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN)

    return FLOW_SHOW_NEAREST_LOCATION
