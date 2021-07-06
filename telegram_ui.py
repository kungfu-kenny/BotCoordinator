import telebot
from config import bot_key


bot = telebot.TeleBot(bot_key)

# @bot.message_handler(content_types=["text"])
# def send_test_message_check(message):
#     print(message)
#     bot.send_message(message.chat.id, 'Hi')

@bot.message_handler(content_types=['location'])
def check_coordinates(message):
    print(message)
    #TODO add keyboard of save, edit, delete
    print('################################################')
    bot.send_message(message.chat.id, 'Hi')

if __name__ == '__main__':
    bot.polling()