from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from conversation_states import *
from db_connection import *
import datetime

# method to execute for '/start' command
def start(update, context):

    #writing a user into db
    if (db.users.find_one({"_id": update.effective_chat.id}) == None):
        db.users.insert_one( { "_id": update.effective_chat.id, "username": update.effective_chat.username, "firstName": update.effective_chat.first_name, 
            "lastName": update.effective_chat.last_name, "lastActivity": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ) 
    else: #updating user info if exists
        db.users.replace_one({"_id": update.effective_chat.id}, { "username": update.effective_chat.username, "firstName": update.effective_chat.first_name, 
            "lastName": update.effective_chat.last_name, "lastActivity": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} )
        
    # buttons to display under the welcome message
    buttons = [[
        InlineKeyboardButton(text='Найближчий пункт прийому', callback_data='button_show_nearest_location')],
        [InlineKeyboardButton(text='Як підготувати сміття до утилізації', callback_data='button_show_how_to_prepare')],
        [InlineKeyboardButton(text='Додати пункт прийому вторсировини', callback_data='button_add_point')],
        [InlineKeyboardButton(text='Зв\'язатися з нами', callback_data='button_help_project')
         ]]

    # create keyboard instance
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message on /start action
    update.effective_message.reply_text('Чим можу бути корисним?', reply_markup=reply_markup)

    return MAIN_MENU