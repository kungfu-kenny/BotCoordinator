import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot import bot
from db_usage import DataUsage
from user_profiler import UserProfiler
from telegram_manager import TelegramManager
from config import (button_help, 
                    button_update,
                    button_groups,
                    button_change,
                    button_support,
                    button_settings,
                    button_locations,
                    button_location_add,
                    button_group_mine,
                    button_group_search,
                    button_location_send,
                    button_location_show,
                    button_groups_mine_del,
                    button_groups_mine_text,
                    button_groups_mine_prev,
                    button_groups_mine_next,
                    button_groups_mine_check,
                    button_settings_mine_text,
                    button_settings_message,
                    button_settings_timing,
                    button_settings_name_default,
                    chat_id_default,
                    entrance_groups_list,
                    entrance_bot_usage,
                    entrance_update_bad,
                    entrance_update_good,
                    entrance_bot_check_true,
                    entrance_bot_check_false,
                    entrance_bot_check_group,
                    entrance_groups_absent,
                    entrance_locations_absent,
                    callback_next_loc,
                    callback_show_loc,
                    callback_delete_loc,
                    callback_next_group,
                    callback_check_group,
                    callback_delete_group,
                    callback_sep_addloc,
                    callback_next_search,
                    callback_sep_loc_del,
                    callback_sep_loc_next,
                    callback_sep_loc_show,
                    callback_sep_group_upd,
                    callback_sep_group_next,
                    callback_sep_group_mine,
                    callback_sep_group_check,
                    callback_sep_group_search,
                    callback_sep_search_next,
                    callback_settings_update,
                    callback_settings_groups,
                    callback_settings_locations,
                    callback_settings_default_name,
                    callback_settings_default_text,
                    callback_settings_default_minute,
                    value_limit_locations,
                    command_name_start,
                    command_name_location_add,
                    command_name_group_update,
                    command_name_location_edit)

    
data_usage = DataUsage()
user_profiler = UserProfiler()
telegram_manager = TelegramManager()


def make_lambda_check() -> bool:
    try:
        telegram_manager.produce_necessary_update(data_usage)
        return True
    except Exception as e:
        bot.send_message(chat_id_default, f'We faced problem with updating groups: {e}')
        return False

def additional_group_check(message) -> None:
    """
    Function for additionall adding values to the database
    Input:  message = value from the 
    Output: we added values to the groups additionally
    """
    try:
        if message.chat.id < 0 and message.chat.type in ['group', 'supergroup']:
            data_usage.insert_group_additional(message.chat.id, message.chat.title)
    except Exception as e:
        msg = f"We faced problems with checking values to the values; Mistake: {e}"
        bot.send_message(chat_id_default, msg)

def produce_location_show(value_user:int, value_list:list) -> None:
    if value_list:
        *_, value_latitude, value_longitude = value_list
        value_loc = bot.send_location(value_user, value_latitude, value_longitude, disable_notification=False)
        bot.reply_to(value_loc, telegram_manager.produce_message_for_location(value_list), parse_mode='Markdown')
    else:
        msg = "Unfortunatelly, you have ***removed*** this location from the database"
        bot.send_message(value_user, msg, parse_mode='Markdown')

def produce_location_delete(value_user:int, value_list:list) -> None:
    if value_list:
        value_id, value_name, *_ = value_list
        msg = f"We successfully deleted your coordinate with name: {value_name}"
        bot.send_message(value_user, msg, disable_notification=False)
        data_usage.delete_location_user(value_user, value_id)
    else:
        msg = "You have already ***removed*** this location previously"
        bot.send_message(value_user, msg, disable_notification=False, parse_mode='Markdown')

def make_deletion_check_group(id_user:int, id_group:int, send_message:bool=False) -> bool:
    """
    Function which is dedicated to make the test of the deletion from the 
    Input:  id_user = id value which we require to test
            id_group = group which is require to check
    Output: we check group that we can produce message
    """
    try:
        new_message = bot.send_message(id_group, entrance_bot_check_group)
        bot.delete_message(id_group, new_message.id)
        if send_message:
            bot.send_message(id_user, entrance_bot_check_true)
        return True
    except Exception as e:
        if send_message:
            bot.send_message(id_user, entrance_bot_check_false)
        msg = f"We faced problems with the value; Mistake: {e}"
        bot.send_message(chat_id_default, msg)
        return False

#TODO work here
def produce_groups_search_show(message, value_id:list, value_name:list, value_index:int, value_edit:bool=False) -> None:
    """
    Method which is dedicated to produce
    Input:  message = message of the user
            value_id = list with id values of the groups
            value_name = list with names of the groups
            value_index = index of the search which is required to work with
    Output: we produced values for search of the
    """
    try:
        keyboard_group_search = InlineKeyboardMarkup()
        button_loc_middle = f'{value_index+1}/{len(value_id)}'
        value_index_next = telegram_manager.make_callback_values(callback_next_search, message.chat.id, value_index+1, len(value_id))
        value_index_prev = telegram_manager.make_callback_values(callback_next_search, message.chat.id, value_index-1, len(value_id))
        print(value_index_next)
        print('lllllllllllllllllllllllllll')
        for id, name in zip(value_id[value_index], value_name[value_index]):
            keyboard_group_search.row(InlineKeyboardButton(id, callback_data='1'),
                                    InlineKeyboardButton(name, callback_data='1'),
                                    InlineKeyboardButton('Connect', callback_data='2'))
        keyboard_group_search.row(InlineKeyboardButton(button_groups_mine_prev, callback_data=value_index_prev), 
                            InlineKeyboardButton(button_loc_middle, callback_data='1'),
                            InlineKeyboardButton(button_groups_mine_next, callback_data=value_index_next))
        if not value_edit:
            bot.send_message(message.chat.id, 'button_groups_mine_text', reply_markup=keyboard_group_search)  
        else:
            bot.edit_message_reply_markup(message.chat.id, message.id, 'button_settings_mine_text', reply_markup=keyboard_group_search)   
    except Exception as e:
        msg = f"We found problems with the creation of the search show; Mistake: {e}"
        bot.send_message(chat_id_default, msg)
        
#TODO work here!
def produce_settings_show(value_list:list, value_check:bool=False, message_id:int=0) -> None:
    """
    Produce the settings values for the user
    Input:  value_user = id for the callback
            value_list = list of the settings
    Output: produced values of the settings
    """
    keyboard_user_settings = InlineKeyboardMarkup()
    user_id, user_text, user_min, user_name_def, user_name_bool, len_loc, len_group = value_list
    keyboard_user_settings.row(InlineKeyboardButton(button_settings_message, callback_data = '1'),
                            InlineKeyboardButton(button_change, callback_data = '2')) #TODO change
    keyboard_user_settings.row(InlineKeyboardButton(user_text, callback_data=callback_settings_default_text))
    keyboard_user_settings.row(InlineKeyboardButton(button_settings_timing, callback_data = '1'),
                            InlineKeyboardButton(button_change, callback_data = '2'),#TODO change
                            InlineKeyboardButton(user_min, callback_data=callback_settings_default_minute)) #TODO change
    keyboard_user_settings.row(InlineKeyboardButton(button_settings_name_default, callback_data = '1'),
                            InlineKeyboardButton(telegram_manager.manage_additional_values(user_name_bool), 
                                                                    callback_data=callback_settings_update),
                            InlineKeyboardButton(button_change, callback_data = '2')) #TODO change
    keyboard_user_settings.row(InlineKeyboardButton(user_name_def, callback_data=callback_settings_default_name))
    button_locations_settings = f"Locations | {telegram_manager.manage_additional_values(len_loc)}:"
    keyboard_user_settings.row(InlineKeyboardButton(button_locations_settings, callback_data=callback_settings_locations),
                                InlineKeyboardButton(len_loc, callback_data='1'))
    button_groups_settings = f"Groups | {telegram_manager.manage_additional_values(len_group)}:" 
    keyboard_user_settings.row(InlineKeyboardButton(button_groups_settings, callback_data=callback_settings_groups),
                                InlineKeyboardButton(len_group, callback_data='1'))
    if not value_check:
        bot.send_message(user_id, button_settings_mine_text, reply_markup=keyboard_user_settings)
    else:
        bot.edit_message_reply_markup(user_id, message_id, button_settings_mine_text, reply_markup=keyboard_user_settings)        

def produce_groups(message):
    keyboard_group_choice = InlineKeyboardMarkup()
    keyboard_group_choice.row(InlineKeyboardButton(button_group_search, callback_data=callback_sep_group_search))
    if data_usage.check_presence_groups(message.chat.id):
        keyboard_group_choice.row(InlineKeyboardButton(button_group_mine, callback_data=callback_sep_group_mine))
    bot.reply_to(message, entrance_groups_list, reply_markup=keyboard_group_choice)

def produce_reply_locations(message:object, value_list:list, value_list_name:list, value_index:int) -> None:
    keyboard_location_reply = InlineKeyboardMarkup()
    value_index_next = telegram_manager.make_callback_values(callback_next_loc, message.chat.id, value_index+1, len(value_list))
    value_index_prev = telegram_manager.make_callback_values(callback_next_loc, message.chat.id, value_index-1, len(value_list))
    button_loc_middle = f'{value_index+1}/{len(value_list)}'
    for i, j in zip(value_list[value_index], value_list_name[value_index]):
        value_callback_show = telegram_manager.make_callback_values(callback_show_loc, message.chat.id, i)
        value_callback_del = telegram_manager.make_callback_values(callback_delete_loc, message.chat.id, i)
        keyboard_location_reply.row(InlineKeyboardButton(j, callback_data='1'),
                                InlineKeyboardButton(button_location_show, callback_data=value_callback_show),
                                InlineKeyboardButton(button_groups_mine_del, callback_data=value_callback_del))
    keyboard_location_reply.row(InlineKeyboardButton(button_groups_mine_prev, callback_data=value_index_prev), 
                            InlineKeyboardButton(button_loc_middle, callback_data='1'),
                            InlineKeyboardButton(button_groups_mine_next, callback_data=value_index_next))
    bot.send_message(message.chat.id, button_groups_mine_text, reply_markup=keyboard_location_reply)        

def produce_reply_locations_edit(message:object, value_list:list, value_list_name:list, value_index:int) -> None:
    keyboard_location_reply_edit = InlineKeyboardMarkup()
    value_index_next = telegram_manager.make_callback_values(callback_next_loc, message.chat.id, value_index+1, len(value_list))
    value_index_prev = telegram_manager.make_callback_values(callback_next_loc, message.chat.id, value_index-1, len(value_list))
    button_loc_middle = f'{value_index+1}/{len(value_list)}'
    for i, j in zip(value_list[value_index], value_list_name[value_index]):
        value_callback_show = telegram_manager.make_callback_values(callback_show_loc, message.chat.id, i)
        value_callback_del = telegram_manager.make_callback_values(callback_delete_loc, message.chat.id, i)
        keyboard_location_reply_edit.row(InlineKeyboardButton(j, callback_data='1'),
                                InlineKeyboardButton(button_location_show, callback_data=value_callback_show),
                                InlineKeyboardButton(button_groups_mine_del, callback_data=value_callback_del))
    keyboard_location_reply_edit.row(InlineKeyboardButton(button_groups_mine_prev, callback_data=value_index_prev), 
                            InlineKeyboardButton(button_loc_middle, callback_data='1'),
                            InlineKeyboardButton(button_groups_mine_next, callback_data=value_index_next))
    bot.edit_message_reply_markup(message.chat.id, message.id, button_groups_mine_text, reply_markup=keyboard_location_reply_edit)

def produce_reply_groups(message:object, value_list:list, value_list_name:list, value_index:int) -> None:
    """
    Function test which is dedicated to make the list of selected by users groups
    Input:  message = selected message which is dedicated 
            value_list = list of lists with the groups id
            value_list_name = list of lists with the group name 
            value_index = index of this list which is sent to the values
    Output: sent input keyboard with this values
    """
    value_index_next = telegram_manager.make_callback_values(callback_next_group, message.chat.id, value_index+1, len(value_list))
    value_index_prev = telegram_manager.make_callback_values(callback_next_group, message.chat.id, value_index-1, len(value_list))
    keyboard_group_reply = InlineKeyboardMarkup()
    button_group_middle = f'{value_index+1}/{len(value_list)}'
    for i, j in zip(value_list[value_index], value_list_name[value_index]):
        value_callback_del = telegram_manager.make_callback_values(callback_delete_group, message.chat.id, i)
        value_callback_check = telegram_manager.make_callback_values(callback_check_group, message.chat.id, i)
        keyboard_group_reply.row(InlineKeyboardButton(i, callback_data='1'), 
                                InlineKeyboardButton(j, callback_data='1'),
                                # telebot.types.InlineKeyboardButton(text="link", url="https://google.com"),
                                InlineKeyboardButton(button_groups_mine_check, callback_data=value_callback_check),
                                InlineKeyboardButton(button_groups_mine_del, callback_data=value_callback_del))
    keyboard_group_reply.row(InlineKeyboardButton(button_groups_mine_prev, callback_data=value_index_prev), 
                            InlineKeyboardButton(button_group_middle, callback_data='1'),
                            InlineKeyboardButton(button_groups_mine_next, callback_data=value_index_next))
    bot.send_message(message.chat.id, button_groups_mine_text, reply_markup=keyboard_group_reply)

def produce_reply_groups_edit(message:object, value_list:list, value_list_name:list, value_index:int) -> None:
    """
    Function which is dedicated to make edit of the reply groups and 
    Input:  message = object of the message in the telegram
            value_list = list with the groups for the users
            value_list_name = list of lists with the group name
            value_index = index with the new values
    Output: we edited values of the group sending
    """
    keyboard_group_edit = InlineKeyboardMarkup()
    button_group_middle = f'{value_index+1}/{len(value_list)}'
    value_index_next = telegram_manager.make_callback_values(callback_next_group, message.chat.id, value_index+1, len(value_list))
    value_index_prev = telegram_manager.make_callback_values(callback_next_group, message.chat.id, value_index-1, len(value_list))
    for i, j in zip(value_list[value_index], value_list_name[value_index]):
        keyboard_group_edit.row(InlineKeyboardButton(i, callback_data='1'), 
                                InlineKeyboardButton(j, callback_data='1'),
                                # InlineKeyboardButton(text="link", url="https://google.com"),
                                InlineKeyboardButton(button_groups_mine_del, callback_data='12'))

    keyboard_group_edit.row(InlineKeyboardButton(button_groups_mine_prev, callback_data=value_index_prev), 
                            InlineKeyboardButton(button_group_middle, callback_data='1'),
                            InlineKeyboardButton(button_groups_mine_next, callback_data=value_index_next))
    bot.edit_message_reply_markup(message.chat.id, message.id, button_groups_mine_text, reply_markup=keyboard_group_edit)

#TODO add on all content_types 
@bot.message_handler(content_types=['location', 'venue'])
def check_coordinates(message):
    additional_group_check(message)
    presence_user, presence_group = data_usage.check_chat_id(message.chat.id)
    value_bool, value_text = telegram_manager.produce_check_values(presence_user, presence_group, message.chat.id, data_usage, message)
    if value_text:
        bot.send_message(chat_id_default, value_text)
        return
    if not value_bool and not value_text:
        return
    keyboard_locations_choice = InlineKeyboardMarkup()
    keyboard_locations_choice.row(InlineKeyboardButton(button_location_add, callback_data=callback_sep_addloc))
    if data_usage.check_presence_groups(message.chat.id):
        keyboard_locations_choice.row(InlineKeyboardButton(button_location_send, callback_data=115))
    if data_usage.check_presence_locations(message.chat.id):
        keyboard_locations_choice.row(InlineKeyboardButton('Update Tags', callback_data=114),
                                    InlineKeyboardButton('Remove Tags', callback_data=111))
    bot.reply_to(message, 'Select command what to do with a location:', reply_markup=keyboard_locations_choice)

@bot.message_handler(commands=[command_name_start])
def start_messages(message):
    additional_group_check(message)
    presence_user, presence_group = data_usage.check_chat_id(message.chat.id)
    value_bool, value_text = telegram_manager.produce_check_values(presence_user, presence_group, message.chat.id, data_usage, message)
    if value_text:
        bot.send_message(chat_id_default, value_text)
        return
    if not value_bool and not value_text:
        return
    markup_test = telegram_manager.return_reply_keyboard()
    link_image = user_profiler.work_on_the_picture()
    if link_image:
        with open(link_image, 'rb') as instance_img:
            bot.send_photo(message.from_user.id, instance_img, caption=entrance_bot_usage, reply_markup=markup_test)

@bot.message_handler(commands=[command_name_location_add])
def add_location_name(message):
    additional_group_check(message)
    presence_user, presence_group = data_usage.check_chat_id(message.chat.id)
    value_bool, value_text = telegram_manager.produce_check_values(presence_user, presence_group, message.chat.id, data_usage, message)
    if value_text:
        bot.send_message(chat_id_default, value_text)
        return
    if not value_bool and not value_text:
        return
    if message.reply_to_message and message.reply_to_message.content_type != "location":
        bot.reply_to(message, 'You have replied your message not to the location, please correct that mistake')
        return
    elif not message.reply_to_message:
        bot.reply_to(message, "You need to reply this message to youre coordinate which you have sent")
        return    
    value_coordinates, _, value_limit = data_usage.get_user_coordinates(message.chat.id)
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
    bot.send_message(message.chat.id, f"We successfully added location with name:\n '{value_name}'")

@bot.message_handler(commands=[command_name_group_update])
def change_group_name(message):
    """
    Method which is dedicated to update the group name; 
    """
    #TODO think about this later
    pass

@bot.message_handler(commands=[command_name_location_edit])
def change_location_name_message(message):
    """
    Method which is dedicated to work with updating the names of the 
    """
    #TODO make the functions of checkings, make values check of the strings
    #TODO make the check these values in the database
    pass

@bot.callback_query_handler(func=lambda call: True)
def calculate_answer_on_the_buttons(query):
    data = query.data
    if data == callback_sep_addloc and query.message.reply_to_message.venue:
        new_name = '|'.join([query.message.reply_to_message.venue.title, query.message.reply_to_message.venue.address])
        new_longitude = query.message.reply_to_message.venue.location.longitude
        new_latitude = query.message.reply_to_message.venue.location.latitude
        new_chat_id = query.message.chat.id
        new_chat_name_first = query.message.chat.first_name
        new_chat_name_last = query.message.chat.last_name
        new_chat_name_user = query.message.chat.username
        data_usage.insert_location([new_chat_id, new_chat_name_user, new_chat_name_first, 
                                new_chat_name_last], new_name, new_latitude, new_longitude)
        bot.send_message(new_chat_id, f"We successfully added location with name:\n '{new_name}'")
        return 

    if data == callback_sep_addloc and not query.message.reply_to_message.venue and query.message.reply_to_message.location:
        new_latitude = query.message.reply_to_message.location.latitude
        new_longitude = query.message.reply_to_message.location.longitude
        new_chat_id = query.message.chat.id
        new_chat_name_first = query.message.chat.first_name
        new_chat_name_last = query.message.chat.last_name
        new_chat_name_user = query.message.chat.username
        
        boolean_default_name = data_usage.return_user_name_default_bool(new_chat_id)
        if boolean_default_name:
            message_print = "Unfortunatelly, u didn't added default name feature, so u need to type the name with a command: "+\
                            f"/{command_name_location_add}: <name which you have selected>\n" +\
                            "Also, u can just include the autoname injection"
            bot.send_message(new_chat_id, message_print)
        else:
            new_name = data_usage.return_user_name_settings(new_chat_id)
            value_coordinates, _, value_limit = data_usage.get_user_coordinates(new_chat_id)
            if not value_limit:
                bot.reply_to(query.message, "You have surpassed the limit of the values")
                return
            new_name = telegram_manager.produce_name_added(new_name, value_coordinates)
            data_usage.insert_location([new_chat_id, new_chat_name_user, new_chat_name_first, 
                                    new_chat_name_last], new_name, new_latitude, new_longitude)
            bot.send_message(new_chat_id, f"We successfully added location with name:\n '{new_name}'")
        return
    
    if data == callback_settings_update:
        data_usage.update_user_settings_default_name(query.message.chat.id)
        user_id, user_text, user_minutes, username_def, username_bool, *_ = data_usage.return_user_settings(query.message.chat.id)
        len_loc, len_group = data_usage.get_length_settings(user_id)
        user_list = [user_id, user_text, user_minutes, username_def, bool(username_bool), len_loc, len_group] 
        produce_settings_show(user_list, True, query.message.id)
        if username_bool:
            message_create = 'Now, you always need to add name for added location'
        else:
            message_create = "Now, you have automated adding location's name."
        bot.send_message(user_id, f'We have changed default parameters of the name. {message_create}')
        return

    if data in [callback_settings_groups, callback_sep_group_mine]:
        _, len_group = data_usage.get_length_settings(query.message.chat.id)
        if len_group:
            value_id, value_name = data_usage.return_group_values(query.message.chat.id)
            value_id = telegram_manager.reconfigure_list_sublists(value_id)
            value_name = telegram_manager.reconfigure_list_sublists(value_name)
            produce_reply_groups(query.message, value_id, value_name, 0)
        else:
            bot.send_message(query.message.chat.id, entrance_groups_absent)
        return

    if data == callback_settings_locations:
        len_loc, _ = data_usage.get_length_settings(query.message.chat.id)
        if len_loc:
            value_name, value_id, _ = data_usage.get_user_coordinates(query.message.chat.id)
            value_id = telegram_manager.reconfigure_list_sublists(value_id, value_limit_locations)
            value_name = telegram_manager.reconfigure_list_sublists(value_name, value_limit_locations)
            if value_name and value_id:
                produce_reply_locations(query.message, value_id, value_name, 0)
        else:
            bot.send_message(query.message.chat.id, entrance_locations_absent)
        return

    if data == callback_settings_default_name:
        name_print = data_usage.return_user_name_settings(query.message.chat.id)
        bot.send_message(query.message.chat.id, f"Your default name is: \n`{name_print}`", parse_mode='Markdown')
        return

    if data == callback_settings_default_text:
        text_print = data_usage.return_user_text(query.message.chat.id)
        bot.send_message(query.message.chat.id, f"Your default text is: \n`{text_print}`", parse_mode='Markdown')
        return
    
    if data == callback_settings_default_minute:
        min_print = data_usage.return_user_minutes(query.message.chat.id)
        bot.send_message(query.message.chat.id, f"Your default minute value is: \n`{min_print}`", parse_mode='Markdown')
        return
    
    #TODO work here
    if data == callback_sep_group_search:
        groups_last = data_usage.get_search_button_basic()
        value_id, value_name = [i[0] for i in groups_last], [i[1] for i in groups_last]
        value_id = telegram_manager.reconfigure_list_sublists(value_id)
        value_name = telegram_manager.reconfigure_list_sublists(value_name)
        produce_groups_search_show(query.message, value_id, value_name, 0)
        # message_print = "Unfortunatelly, we didn't produce this feature yet"
        # bot.send_message(query.message.chat.id, message_print)
        return

    if callback_sep_search_next in data:
        value_index, value_len = data.split(callback_sep_search_next)
        value_index, value_len = int(value_index), int(value_len)
        value_index = telegram_manager.check_index_inserted(value_index, value_len)
        groups_last = data_usage.get_search_button_basic()
        value_id, value_name = [i[0] for i in groups_last], [i[1] for i in groups_last]
        produce_groups_search_show(query.message, value_id, value_name, value_index, True)
        return

    if callback_sep_group_check in data:
        value_id, value_group = data.split(callback_sep_group_check)
        value_id, value_group = int(value_id), int(value_group)
        make_deletion_check_group(value_id, value_group, True)
        return

    if callback_sep_group_upd in data:
        value_id, value_group = data.split(callback_sep_group_upd)
        value_id, value_group = int(value_id), int(value_group)
        check_working, check_further, check_nonremoved = data_usage.disconnect_user_group(value_id, value_group)
        if check_working:
            if not check_nonremoved:
                bot.send_message(value_id, f"Group with id of `{value_group}` was previously removed; you need to check it", parse_mode='Markdown')
            if check_further:
                value_check_usage = make_deletion_check_group(value_id, value_group)
                if not value_check_usage:
                    data_usage.disconnect_whole_group(value_group)
        else:
            bot.send_message(chat_id_default, f'We faced problem with removing groups; Check SQL code later')
        return

    if callback_sep_group_next in data:
        value_id, value_index, value_len = data.split(callback_sep_group_next)
        value_id, value_index, value_len = int(value_id), int(value_index), int(value_len)
        
        values_id, values_name = data_usage.return_group_values(value_id)
        values_id = telegram_manager.reconfigure_list_sublists(values_id)
        values_name = telegram_manager.reconfigure_list_sublists(values_name)
        value_index = telegram_manager.check_index_inserted(value_index, value_len)
        if value_len > 1:
            produce_reply_groups_edit(query.message, values_id, values_name, value_index)
        return

    if callback_sep_loc_next in data:
        value_id, value_index, value_len = data.split(callback_sep_loc_next)
        value_id, value_index, value_len = int(value_id), int(value_index), int(value_len)
        values_name, values_id, _ = data_usage.get_user_coordinates(value_id)
        values_id = telegram_manager.reconfigure_list_sublists(values_id, value_limit_locations)
        values_name = telegram_manager.reconfigure_list_sublists(values_name, value_limit_locations)
        value_index = telegram_manager.check_index_inserted(value_index, value_len)
        if value_len > 1:
            produce_reply_locations_edit(query.message, values_id, values_name, value_index)
        return

    if callback_sep_loc_show in data:
        value_id, value_loc_id = data.split(callback_sep_loc_show)
        value_id, value_loc_id = int(value_id), int(value_loc_id)
        value_list = data_usage.get_user_coordinate(value_id, value_loc_id)
        produce_location_show(value_id, value_list)
        return

    if callback_sep_loc_del in data:
        value_id, value_loc_id = data.split(callback_sep_loc_del)
        value_id, value_loc_id = int(value_id), int(value_loc_id)
        value_list = data_usage.get_user_coordinate(value_id, value_loc_id)
        produce_location_delete(value_id, value_list)
        return

@bot.message_handler(content_types=["text"])
def send_test_message_check(message):
    #TODO rework this shit again
    previously_updated = make_lambda_check()
    additional_group_check(message)
    presence_user, presence_group = data_usage.check_chat_id(message.chat.id)
    value_bool, value_text = telegram_manager.produce_check_values(presence_user, presence_group, message.chat.id, data_usage, message)
    if value_text:
        bot.send_message(chat_id_default, value_text)
        return
    if not value_bool and not value_text:
        return
    if message.text == button_update:
        try:
            if not previously_updated:
                make_lambda_check()
            bot.send_message(message.chat.id, entrance_update_good)
        except Exception as e:
            bot.send_message(message.chat.id, entrance_update_bad)
            bot.send_message(chat_id_default, f'We faced problem with updating groups: {e}')

    if message.text == button_settings:
        data_usage.insert_settings(message.chat.id)
        user_id, user_text, user_minutes, username_def, username_bool, *_ = data_usage.return_user_settings(message.chat.id)
        len_loc, len_group = data_usage.get_length_settings(user_id)
        user_list = [user_id, user_text, user_minutes, username_def, bool(username_bool), len_loc, len_group] 
        produce_settings_show(user_list)

    if message.text == button_help:
        bot.send_message(message.chat.id, 'TEST5')
        data_usage.check_db()

    if message.text == button_groups:
        produce_groups(message)

    if message.text == button_locations:
        value_name, value_id, _ = data_usage.get_user_coordinates(message.chat.id)
        value_id = telegram_manager.reconfigure_list_sublists(value_id, value_limit_locations)
        value_name = telegram_manager.reconfigure_list_sublists(value_name, value_limit_locations)
        if value_name and value_id:
            produce_reply_locations(message, value_id, value_name, 0)
        else:
            bot.send_message(message.chat.id, entrance_locations_absent)

    if message.text == button_support:
        value_msg = bot.send_message(message.chat.id, 'TEST6')


if __name__ == '__main__':
    bot.polling()
    data_usage.close_connection()