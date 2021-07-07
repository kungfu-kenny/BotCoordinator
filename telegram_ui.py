import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
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
    bot.send_message(message.chat.id, '222')

@bot.message_handler(func=lambda call: True)
def start_message(query):
    print(query)
    print('#####################################4444')
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('1', '2')
    bot.register_next_step_handler(query, process_step)

def process_step(query):
    chat_id = query.from_user.id
    print(query)
    print('####################################2#')
    if query.text=='1':
        bot.send_message(chat_id, 'Hi')
    else:
        bot.send_message(chat_id, 'Bye')

if __name__ == '__main__':
    bot.polling()