from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import geopy.distance
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
        InlineKeyboardButton(text='Найближчий пункт приймоу', callback_data='show_nearest_location')],
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
def show_nearest_location(update, context):
    # extracting each category name and creating an array of buttons with callback_data = type
    buttons = []

    all_categories = db.categories.find()
    for category in all_categories:
        buttons.append([InlineKeyboardButton(text=category['name'], callback_data='category_' + category['type'])])

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message with categories as inline buttons
    update.effective_message.reply_text(text="Що здаємо на переробку?", reply_markup=reply_markup)

    return CHOSE_BUTTON


# # method to execute after user selects a category from the list provided by show_nearest_point method
# def show_chosen_category(update, context):
#     pass


def add_point(update, context):
    pass


def help_project(update, context):
    pass


def ask_for_location(update, context):
    selected_category = update.callback_query.data.partition('_')[2]
    context.user_data['selected_category'] = selected_category
    update.effective_message.reply_text('Де ти зараз є? Відправ мені геолокацію.')

    return SEND_LOCATION


def process_location(update, context):
    longitude = update.message.location.longitude
    latitude = update.message.location.latitude

    all_locations_collection = db.locations

    # assuming first location is nearest
    nearest_point = all_locations_collection.find_one()
    min_distance = geopy.distance.geodesic((longitude, latitude), nearest_point['coordinates'])

    # searching for nearest location
    all_locations = all_locations_collection.find()
    for location in all_locations:
        local_min = geopy.distance.geodesic((longitude, latitude), (location['longitude'], location['latitude']))
        if local_min < min_distance:
            min_distance = local_min
            nearest_point = location

    update.effective_message.reply_text(
        'Ось що знайшов поблизу: /n{}/n{}/n{}/n/n{}/n/n{}'.format(nearest_point['name'],
                                                                  nearest_point['address'],
                                                                  nearest_point['workingHours'],
                                                                  nearest_point['categories'],
                                                                  min_distance.m))

    return CHOSE_BUTTON


def show_how_to_prepare(update, context):
    # buttons to display under the welcome message
    buttons = [
        [InlineKeyboardButton(text='Так', callback_data='show_how_to_prepare')],
        [InlineKeyboardButton(text='Ні', callback_data='do_not_show_how_to_prepare')]
    ]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /show_how_to_prepare action
    update.message.reply_text('Розказати, як підготувати його до здачі?', reply_markup=reply_markup)

    return CHOSE_BUTTON


def extract_category_info(update, context):
    pass
# category_type = update.callback_query.data.partition('_')[2]
#
#     description = db.categories.find_one({"type": str(category_type)})['description']
#
#     update.effective_message.reply_text(description)
