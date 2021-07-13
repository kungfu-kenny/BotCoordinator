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
                    chat_id_default)

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


if __name__ == '__main__':
    a = TelegramManager()
    a.make_updates()