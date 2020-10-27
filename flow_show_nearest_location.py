from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import geopy.distance
from conversation_states import *
from db_connection import *


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

    return FLOW_SHOW_NEAREST_LOCATION


def ask_for_location_when_category_selected(update, context):
    # store selected category to process after user sends location
    selected_category_type = update.callback_query.data.partition('_')[2]
    context.user_data['selected_category_type'] = selected_category_type

    # button 'how to send location'
    button = [
        [InlineKeyboardButton(text='Я не знаю як відправити локацію', callback_data='how_to_send_location')]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    update.effective_message.reply_text('Де ти зараз є? Відправ мені геолокацію.', reply_markup=reply_markup)

    return SEND_LOCATION

def show_gif_how_to_send_location(update, context):
    
    update.effective_message.reply_document('CgACAgIAAxkBAAIBS1-YVr2B70MhHQk7k9DGATX2FTsXAAKvCQACuNvISBhNUvXZPliGGwQ')

    return SEND_LOCATION


def process_location(update, context):
    # extract coordinates that users sends
    longitude = update.message.location.longitude
    latitude = update.message.location.latitude

    # fetch category user saved in ask_for_location func
    selected_category_type = context.user_data['selected_category_type']

    # fetch location collection from db
    all_locations_collection = db.locations

    # assume first location that matches selected category is nearest
    nearest_location = all_locations_collection.find_one({'categories': selected_category_type})
    # distance calculation
    min_distance = geopy.distance.geodesic((longitude, latitude), reversed(nearest_location['coordinates']))

    # search for nearest location
    all_locations = all_locations_collection.find()
    for location in all_locations:
        if selected_category_type in location['categories']:
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
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]  # add common button
    ]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /show_how_to_prepare action
    update.message.reply_text('Розказати, як підготувати його до здачі?', reply_markup=reply_markup)

    return FLOW_SHOW_NEAREST_LOCATION


def show_how_to_prepare_category(update, context):
    selected_category_type = context.user_data['selected_category_type']

    selected_category = db.categories.find_one({'type': selected_category_type})

    button = [
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]  # add common button
    ]

    reply_markup = InlineKeyboardMarkup(button)

    # update.effective_message.reply_text(
    #     text='Як підготувати сміття категорії *{'+nearest_location['description']+'}* до переробки:\n',
    #     reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    update.effective_message.reply_text( # add formatters
        'Як підготувати сміття категорії *{}* до переробки:\n\n{}\n\n✅{}\n\n❌{}\n\nℹ️{}'.format(
            selected_category['name'],
            selected_category['description'],
            selected_category['do'],
            selected_category['dont'],
            selected_category['steps']),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN)

    return FLOW_SHOW_NEAREST_LOCATION

# category_type = update.callback_query.data.partition('_')[2]
#
#     description = db.categories.find_one({"type": str(category_type)})['description']
#
#     update.effective_message.reply_text(description)
