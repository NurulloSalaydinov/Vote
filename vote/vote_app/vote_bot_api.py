import telebot
from .models import *

bot = telebot.TeleBot("Your Bot Api")

@bot.message_handler(commands=["start"])
def get_user_data(message):
    username = str(message.from_user.username)
    first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    user_id = str(message.chat.id)
    print(message)
    bot.send_message(user_id, 'Start Kommandasi Bosildi')


bot.polling(none_stop=True)