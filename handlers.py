from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import configparser

# config is used to extract remote mongo instance
config = configparser.ConfigParser()
config.read('config.ini')

mongo_client = MongoClient(config['DATABASE']['URL'])
db = mongo_client.motiwaste_bot

# states of conversation
CHOSE_BUTTON, SEND_LOCATION = range(2)


# method to execute for '/start' command
def start(update, context):
    # buttons to display under the welcome message
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

    return CHOSE_BUTTON


# method to execute on show_nearest_point button click
def show_nearest_point(update, context):
    # extracting each category name and creating an array of buttons with callback_data = type
    buttons = []
    for category in db.categories.find():
        buttons.append([InlineKeyboardButton(text=category['name'], callback_data='category_' + category['type'])])

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message with categories as inline buttons
    update.effective_message.reply_text(text="Що здаємо на переробку?", reply_markup=reply_markup)

    return CHOSE_BUTTON


# method to execute after user selects a category from the list provided by show_nearest_point method
def show_chosen_category(update, context):
    pass


def add_point(update, context):
    pass


def help_project(update, context):
    pass

def show_how_to_prepare(update, context):
    # buttons to display under the welcome message
    buttons = [
        [InlineKeyboardButton(text='Так', callback_data='show_how_to_prepare')],
        [InlineKeyboardButton(text='Ні', callback_data='do_not_show_how_to_prepare')]
    ]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /show_how_to_prepare action
    update.message.reply_text('Чим можу бути корисним?', reply_markup=reply_markup)

    return CHOSE_BUTTON

def process_location(update, context):
    pass

def extract_category_info(update, context):
    category_type = update.callback_query.data.partition('_')[2]

    description = db.categories.find_one({"type": str(category_type)})['description']

    update.effective_message.reply_text(description)

    return CHOSE_BUTTON


