from conversation_states import *


def button_add_point(update, context):
    button = [
        [InlineKeyboardButton(text='До головного меню', callback_data='to_main_menu')]  # add common button
    ]
    reply_markup = InlineKeyboardMarkup(button)

    update.effective_message.reply_text(text="Респект! Заповни цю невеличку анкету і ми додамо пункт до карти. bit.ly/2NPuvpT", reply_markup=reply_markup)

    return FLOW_ADD_POINT