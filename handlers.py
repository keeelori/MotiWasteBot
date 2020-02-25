from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import configparser

# config is used to extract remote mongo instance
config = configparser.ConfigParser()
config.read('config.ini')

mongo_client = MongoClient(config['DATABASE']['URL'])
db = mongo_client.motiwaste_bot

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(4)


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


# method to execute after user selects a category from the list provided by show_nearest_point method
def show_chosen_category(update, context):
    pass


def show_how_to_prepare(update, context):
    pass


def add_point(update, context):
    pass


def help_project(update, context):
    pass
