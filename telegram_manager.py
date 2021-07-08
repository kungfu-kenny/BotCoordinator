import os
import json
import requests
from pprint import pprint
from config import bot_key, separator

class TelegramManager:
    """
    class which is dedicated to manage some values
    """
    def __init__(self) -> None:
        self.link_update = f"https://api.telegram.org/bot{bot_key}/getUpdates"

    def make_updates(self) -> None:
        """
        Method which is dedicated to get values 
        Input:  None
        Output: we successfully added 
        """
        # value_dictionary = requests.post(self.link_update).json()
        value_dictionary = json.load(open('E:\Projects\BotCoordinator\config\\tst.json'))
        # pprint(value_dictionary)
        print(value_dictionary['ok'])
        print('##################################################')
        print(value_dictionary['result'])
        value_parsed = []
        if value_dictionary.get('ok', False) and value_dictionary.get('result', []):
            value_result = value_dictionary.get('result', [])
            for results in value_result:
                print(results)
                members_dictionary = results.get('my_chat_member', {})
                members_chat = members_dictionary.get('chat', {})
                chat_id, chat_title = members_chat.get('id'), members_chat.get('title')
                members_from = members_dictionary.get('from', {})
                user_id, name_first = members_from.get('id'), members_from.get('first_name')
                name_last, username = members_from.get('last_name'), members_from.get('username')
                value_list = [chat_id, chat_title, user_id, name_first, name_last, username]
                if all(value_list):
                    value_parsed.append(separator.join(str(f) for f in value_list))
                print('---------------------------------')
                print(chat_id, chat_title)
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print(user_id, name_first, name_last, username)
                print('==============================================================')
        value_parsed = [v.split(separator) for v in list(set(value_parsed))]
        value_parsed = [[int(v[0]), v[1], int(v[2]), v[3], v[4], v[5]] for v in value_parsed]
        print(value_parsed)
if __name__ == '__main__':
    a = TelegramManager()
    a.make_updates()