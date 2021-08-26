import os
import pafy
import requests
from telegram_manager import TelegramManager
from config import (url_sound,
                    name_sound,
                    folder_config,
                    # chat_id_default,
                    card_donations,
                    entrance_bot_img_name,
                    entrance_bot_img_link)


class UserProfiler:
    """
    class which is dedicated to work with the style of this bot;
    It adds musical layer and returns music to send
    """
    def __init__(self) -> None:
        self.folder_current = os.getcwd()
        self.folder_config = os.path.join(self.folder_current, folder_config)
        self.folder_create = lambda x: os.path.exists(x) or os.mkdir(x)

    @staticmethod
    def produce_request(value_link:str) -> object:
        """
        Method for making 
        Input:  value_link = link which is dedicated to make the request
        Output: object valus
        """
        return requests.get(value_link, stream=True)

    def work_on_the_picture(self) -> None:
        """
        Method which is dedicated to download the picture and store it to the folder
        Input:  None
        Output: We stored the folder to the 
        """
        self.folder_create(self.folder_config)
        value_image_used = os.path.join(self.folder_config, entrance_bot_img_name)
        if os.path.exists(value_image_used) and os.path.isfile(value_image_used):
            return value_image_used
        a = TelegramManager()
        try:
            value_img = self.produce_request(entrance_bot_img_link)
            if value_img.status_code == 200:
                with open(value_image_used, 'wb') as new_picture:
                    for chunk in value_img:
                        new_picture.write(chunk)
                return value_image_used
            a.proceed_message_values('Unfortunatelly, your link to the image is not working.')
        except Exception as e:
            a.proceed_message_values(f'We faced problem with the getting requests. Mistake: {e}')
        return ''

    def produce_music_start(self) -> str:
        """
        Method which is dedicated to create the audio for the start
        Input:  None
        Output: path to the audio message for stat
        """
        try:
            self.folder_create(self.folder_config)
            value_path = os.path.join(self.folder_config, name_sound)
            if not (os.path.exists(value_path) and os.path.isfile(value_path)):
                audio_get = pafy.new(url=url_sound)
                best_audio = audio_get.getbestaudio()
                best_audio.download(filepath=value_path)
            return value_path
        except Exception as e:
            a = TelegramManager()
            a.proceed_message_values(f'We faced problem with the getting audio. Mistake: {e}')
            return ''

    @staticmethod
    def produce_message_for_sending() -> str:
        """
        Static method for getting values from
        Input:  None
        Output: we returning string for the getting the support button 
        """
        return f"You can donate your money here:\n`{card_donations}`"


if __name__ == '__main__':
    a = UserProfiler()
    # a.work_on_the_picture()
    a.produce_music_start()