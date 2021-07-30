import os
import json
import requests
from pprint import pprint
from telebot.types import ReplyKeyboardMarkup
from telegram_bot import bot
from config import (bot_key, 
                    separator, 
                    callback_sep_upd,
                    callback_sep_hel,
                    callback_sep_gro,
                    callback_sep_loc,
                    callback_sep_set,
                    callback_sep_sup,
                    button_help, 
                    button_update,
                    button_groups,
                    button_support,
                    button_settings,
                    button_locations,
                    chat_id_default,
                    value_const_int,
                    command_name_location_add,
                    command_name_location_edit)

class TelegramManager:
    """
    class which is dedicated to manage some values
    """
    def __init__(self) -> None:
        self.link_update = f"https://api.telegram.org/bot{bot_key}/getUpdates"

    def produce_necessary_update(self, data_usage:object):
        """
        Method which is dedicatd to work with a 
        Input:  data_usage = object of the database
        Output: we successfully updated the database
        """
        for id_group, group_name, id_user, name_first, name_last, username in self.make_updates():
            data_usage.insert_group(id_group, group_name, id_user, username, name_first, name_last)

    @staticmethod
    def proceed_message_values(message_error:str) -> None:
        """
        Static method which is dedicated to send values to the special user in cases of error
        Input:  bot = telegram bot values
                message_error = error which we faced
        Output: we send message values
        """
        bot.send_message(chat_id_default, message_error)

    @staticmethod
    def return_reply_keyboard():
        markup_test = ReplyKeyboardMarkup(True, True, row_width=1)
        markup_test.row(button_locations, button_groups)
        markup_test.row(button_update, button_settings, button_help)
        markup_test.row(button_support)
        return markup_test

    def make_updates(self) -> list:
        """
        Method which is dedicated to get values 
        Input:  requested values from the 
        Output: list with updated values of the group
        """
        value_dictionary = requests.post(self.link_update).json()
        # value_dictionary = json.load(open(os.path.join(os.getcwd(), 'config', 'tst.json')))
        value_parsed = []
        if value_dictionary.get('ok', False) and value_dictionary.get('result', []):
            value_result = value_dictionary.get('result', [])
            for results in value_result:
                members_dictionary = results.get('my_chat_member', {})
                members_chat = members_dictionary.get('chat', {})
                chat_id, chat_title = members_chat.get('id'), members_chat.get('title')
                members_from = members_dictionary.get('from', {})
                user_id, name_first = members_from.get('id'), members_from.get('first_name')
                name_last, username = members_from.get('last_name'), members_from.get('username')
                value_list = [chat_id, chat_title, user_id, name_first, name_last, username]
                if all(value_list):
                    value_parsed.append(separator.join(str(f) for f in value_list))
        value_parsed = [v.split(separator) for v in list(set(value_parsed))]
        value_parsed = [[int(v[0]), v[1], int(v[2]), v[3], v[4], v[5]] for v in value_parsed]
        return value_parsed

    def manage_callback_data(self, value_string:str) -> set:
        """
        Method which is dedicated to manage all posible callback data to the function
        Input:  value_string = string which is sent to the 
        Output: set with sent values which is required
        """
        if callback_sep_sup in value_string:
            return ()
        if callback_sep_hel in value_string:
            return ()

    @staticmethod
    def manage_added_name(value_string:str) -> set:
        """
        Method which is dedicated to check that it has been added name 
        Input:  value_string = string which user has been inserted
        Output: set with values of the string name, boolean of everything is okay
        """
        #TODO firstly, create the name
        value_string = value_string.strip()
        value_name, value_command = '', f"/{command_name_location_add}"
        value_bool = value_command in value_string and value_string[:len(value_command)] == value_command and bool(value_string[len(value_command):])
        if value_bool:
            value_name = value_string[len(value_command) + 1:]
            value_name = value_name.strip()#.replace(':', '').replace(',', '')
        return value_name, value_bool

    @staticmethod
    def manage_updated_name(value_string:str) -> set:
        """
        Method which is dedicated to check the updated string for all of that
        Input:  value_string = string which user has been inserted to update
        Output: set with values of 
        """
        #TODO add additional checking on all of this
        value_name_old, value_name_new, value_command, value_bool_comm = [], [], f"/{command_name_location_edit}", False
        value_bool = value_command in value_string and value_string[:len(value_command)] == value_command and bool(value_string[len(value_command):])
        if value_bool:
            value_list_used = []
            value_list_bool = []
            value_names = value_string[len(value_command) + 1:]
            for value_phrase in value_names.split(','):
                if value_phrase:
                    value_list_check = value_phrase.split(':')
                    value_list_bool.append(len(value_list_check == 2))
                    value_list_used.extend(value_list_check)
            value_bool_comm = all(value_list_bool)
        if value_bool_comm:
            for index, value_name in enumerate(value_list_used):
                if index + 1 % 2 == 0:
                    value_name_new.append(value_name)
                else:
                    value_name_old.append(value_name)
        return value_name_new, value_name_old, value_bool, value_bool_comm

    def produce_name_added(self, value_string:str, value_list:list) -> str:
        """
        Method which is dedicated to produce the values of the 
        Input:  value_string = string values of the 
                value_list = list of the selected values of the user locations
        Output: string which is used by this user
        """
        if not value_string in value_list:
            return value_string
        return self.produce_name_added(f"{value_string}(1)", value_list)

    #CREATE VALUES FOR THE CALLBACK
    def make_callback_values(self, value_type:str, value_id:int=value_const_int, value_index:int=value_const_int, value_len:int=value_const_int) -> str:
        """
        Method which is dedicated to create the callback data for the user values
        Input:  value_type = type which is dedicated to create values
                value_id = id of the user
                value_index = index if it is required
        Output: string with callback data
        """
        if value_type == 'next_group_list':
            print(1)
            #TODO make the adequate index

    def produce_check_values(self, chat_id:int) -> bool:
        """
        Method which is dedicated to check that user 
        Input:  chat_id = chat id from the telegram message
        Output: boolean value which is dedicated 
        """
        pass


if __name__ == '__main__':
    a = TelegramManager()
    a.make_updates()