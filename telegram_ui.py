import telebot
from telebot.types import (ReplyKeyboardMarkup, 
                            InlineKeyboardMarkup, 
                            InputTextMessageContent,
                            InlineQueryResultArticle)
from telegram_bot import bot
from db_usage import DataUsage
from user_profiler import UserProfiler
from telegram_manager import TelegramManager
from config import (separator,
                    button_help, 
                    button_update,
                    button_groups,
                    button_support,
                    button_settings,
                    button_locations,
                    button_location_add,
                    button_location_send,
                    entrance_bot_usage,
                    entrance_values,
                    command_name_location_add,
                    command_name_location_edit)

    
data_usage = DataUsage()
user_profiler = UserProfiler()
telegram_manager = TelegramManager()
markup_test = telegram_manager.return_reply_keyboard()

@bot.message_handler(content_types=['location'])
def check_coordinates(message):
    telegram_manager.produce_necessary_update(data_usage)
    #TODO add keyboard of save, edit, delete, rename values
    keyboard_locations_choice = telebot.types.InlineKeyboardMarkup()
    callback_add = 1
    keyboard_locations_choice.row(telebot.types.InlineKeyboardButton(button_location_add, callback_data=112))
    if data_usage.check_presence_groups(message.chat.id):
        keyboard_locations_choice.row(telebot.types.InlineKeyboardButton(button_location_send, callback_data=115))
    if data_usage.check_presence_locations(message.chat.id):
        keyboard_locations_choice.row(telebot.types.InlineKeyboardButton('Update Tags', callback_data=114),
                telebot.types.InlineKeyboardButton('Remove Tags', callback_data=111))
    
    bot.reply_to(message, 'Select command what to do with a location:', reply_markup=keyboard_locations_choice)
    print('################################################')

@bot.message_handler(commands=['start'])
def start_messages(message):
    telegram_manager.produce_necessary_update(data_usage)
    markup_test = telegram_manager.return_reply_keyboard()
    link_image = user_profiler.work_on_the_picture()
    if link_image:
        with open(link_image, 'rb') as instance_img:
            bot.send_photo(message.from_user.id, instance_img, caption=entrance_bot_usage, reply_markup=markup_test)

@bot.message_handler(commands=[command_name_location_add])
def add_location_name(message):
    if message.reply_to_message and message.reply_to_message.content_type != "location":
        bot.reply_to(message, 'You have replied your message not to the location, please correct that mistake')
        return
    elif not message.reply_to_message:
        bot.reply_to(message, "You need to reply this message to youre coordinate which you have sent")
        return    
    value_coordinates, value_limit = data_usage.get_user_coordinates(message.chat.id)
    if not value_limit:
        bot.reply_to(message, "You have surpassed the limit of the values")
        return
    value_name, value_check = telegram_manager.manage_added_name(message.text)
    if not value_check:
        bot.reply_to(message, "Unfortunatelly, you pressed the wrong values to this values")
        return
    
    value_name = telegram_manager.produce_name_added(value_name, value_coordinates)
    value_latitude = message.reply_to_message.location.latitude
    value_longitude = message.reply_to_message.location.longitude
    data_usage.insert_location([message.from_user.id, message.from_user.username, message.from_user.first_name, 
                                message.from_user.last_name], value_name, value_latitude, value_longitude)

@bot.message_handler(commands=[command_name_location_edit])
def change_location_name_message(message):
    """
    Method which is dedicated to work with updating the names
    """
    pass

@bot.callback_query_handler(func=lambda call: True)
def calculate_answer_on_the_buttons(query):
    data = query.data
    data_user = query.from_user.id
    print(data_user)
    print(query)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # try:
    #     r1 = InlineQueryResultArticle('1', 'Result1', InputTextMessageContent('hi'))
    #     r2 = InlineQueryResultArticle('2', 'Result2', InputTextMessageContent('hi'))
    #     bot.answer_inline_query(query.id, [r1, r2])
    # except Exception as e:
    #     print(e)

@bot.message_handler(content_types=["text"])
def send_test_message_check(message):
    telegram_manager.produce_necessary_update(data_usage)
    if message.text == button_update:
        value_msg = bot.send_message(message.from_user.id, 'TEST3')
        # bot.delete_message(message.chat.id, message.message_id)
        # delete_message(message.chat.id, .message_id)
    elif message.text == button_settings:
        value_msg = bot.send_message(message.from_user.id, 'TEST4')
    if message.text == button_help:
        value_msg = bot.send_message(message.from_user.id, 'TEST5')
    # r1 = InlineQueryResultArticle('1', 'Result1', InputTextMessageContent('hi'))
    # r2 = InlineQueryResultArticle('2', 'Result2', InputTextMessageContent('hi'))
    # bot.answer_inline_query(message.from_user.id, [r1, r2])

    # print(query)
    # print('#####################################4444')
    # data_usage.check_db()
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # markup_default.add(button_help)
    
    # bot.register_next_step_handler(query, process_step)
    # markup_test = ReplyKeyboardMarkup(True, True, row_width=1)
    # markup_test.row('5', '6')
    # markup_test.row('4', '7')
    # bot.send_message(message.from_user.id, "Yeezus2", reply_markup=markup_test)


if __name__ == '__main__':
    bot.polling()
    data_usage.close_connection()