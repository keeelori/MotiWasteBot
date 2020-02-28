from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
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
    update.effective_message.reply_text('Чим можу бути корисним?', reply_markup=reply_markup)

    return CHOSE_BUTTON


# method to execute on show_nearest_point button click
def button_show_nearest_location(update, context):
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
    update.effective_message.reply_text(text="Що здаємо на переробку?", reply_markup=reply_markup)

    return CHOSE_BUTTON


def button_show_how_to_prepare(update, context):
    pass

def button_add_point(update, context):
    pass


def button_help_project(update, context):
    pass


def ask_for_location_when_category_selected(update, context):
    # store selected category to process after user sends location
    selected_category_name = update.callback_query.data.partition('_')[2]
    context.user_data['selected_category_name'] = selected_category_name

    update.effective_message.reply_text('Де ти зараз є? Відправ мені геолокацію.')

    return SEND_LOCATION


def process_location(update, context):
    # extract coordinates that users sends
    longitude = update.message.location.longitude
    latitude = update.message.location.latitude

    # fetch category user saved in ask_for_location func
    selected_category_name = context.user_data['selected_category_name']

    # fetch location collection from db
    all_locations_collection = db.locations

    # assume first location that matches selected category is nearest
    nearest_location = all_locations_collection.find_one({'categories': selected_category_name})
    # distance calculation
    min_distance = geopy.distance.geodesic((longitude, latitude), reversed(nearest_location['coordinates']))

    # search for nearest location
    all_locations = all_locations_collection.find()
    for location in all_locations:
        if selected_category_name in location['categories']:
            local_min = geopy.distance.geodesic((longitude, latitude), (location['coordinates']))
            if local_min < min_distance:
                min_distance = local_min
                nearest_location = location

    # replacing each category.type in location with category.name. for example [paper] is replaced with string 'Paper'
    categories_names = ''
    # fetch categories collection to find real name
    for category_in_location in nearest_location['categories']:
        for category in db.categories.find():
            if category_in_location == category['type']:
                categories_names = categories_names + (category['name']) + '\n'
                break

    # send category info
    update.effective_message.reply_text(
        'Ось що знайшов поблизу:\n\n{}\n{}\n{}\n\n*{}*\n{}км'.format(nearest_location['name'],
                                                                     nearest_location['address'],
                                                                     nearest_location['workingHours'],
                                                                     categories_names,
                                                                     int(min_distance.km)),
        parse_mode=ParseMode.MARKDOWN)

    # send the Location object
    nearest_latitude, nearest_longitude = reversed(nearest_location['coordinates'])
    update.message.bot.send_location(chat_id=update.effective_chat.id,
                                     latitude=nearest_latitude,
                                     longitude=nearest_longitude)

    # buttons to display after location has been sent
    buttons = [
        [InlineKeyboardButton(text='Так', callback_data='show_how_to_prepare_category')],
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]
    ]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /show_how_to_prepare action
    update.message.reply_text('Розказати, як підготувати його до здачі?', reply_markup=reply_markup)

    return CHOSE_BUTTON


def show_how_to_prepare_category(update, context):
    selected_category_name = context.user_data['selected_category_name']

    selected_category = db.categories.find_one({'type': selected_category_name})

    button = [
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(button)

    # update.effective_message.reply_text(
    #     text='Як підготувати сміття категорії *{'+nearest_location['description']+'}* до переробки:\n',
    #     reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    update.effective_message.reply_text(
    'Як підготувати сміття категорії *{}* до переробки:\n\n{}\n\n✅{}\n\n❌{}\n\nℹ️{}'.format(selected_category['name'], #add formatters
                                                                                        selected_category['description'],
                                                                                        selected_category['do'],
                                                                                        selected_category['dont'],
                                                                                        selected_category['steps']),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN)

    return CHOSE_BUTTON

# category_type = update.callback_query.data.partition('_')[2]
#
#     description = db.categories.find_one({"type": str(category_type)})['description']
#
#     update.effective_message.reply_text(description)
