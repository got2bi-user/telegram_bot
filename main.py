import telebot
import random
import datetime
from telebot import types
file_log = open("./files/telegram.log", "a+", encoding="utf-8")
token='your token for bot'
bot=telebot.TeleBot(token)
list_id_stikers = ["CAACAgIAAxkBAAELZv9lzaJDYRGDA5HRMGmoXclKmhJNQgACYQADQzOdIRxX4gR4THmpNAQ","CAACAgIAAxkBAAELZwFlzaJMBebOVvM71DrqwIvVPMy4KwACYwADQzOdIVf4khZAH3xANAQ","CAACAgIAAxkBAAELZwNlzaJNL3xsfpQtpSLLQEGOJ0G8VgACZAADQzOdIWg9ZrEY53YxNAQ"]
@bot.message_handler(commands=['start'])
def start_message(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " +"Пользователь отправил команду /start\n")
    file_log.flush()
    bot.send_message(message.chat.id,'Привет')
@bot.message_handler(content_types = ['text'])
def calc_message(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь отправил текст " + message.text + " \n")
    file_log.flush()
    bot.send_message(message.chat.id, str(eval(message.text)))

@bot.message_handler(content_types=['document'])
def file_saves(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь отправил файл " + message.document.file_name + "\n")
    file_log.flush()
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = './files/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
@bot.message_handler(content_types = ['sticker'])
def send_stikers(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь отправил стикер\n")
    file_log.flush()
    bot.send_sticker(message.chat.id, list_id_stikers[random.randint(0,2)])
bot.infinity_polling()



