import telebot
import random
import datetime
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
provider_token = 'your provider token'
list_id_stikers = ["CAACAgIAAxkBAAELZv9lzaJDYRGDA5HRMGmoXclKmhJNQgACYQADQzOdIRxX4gR4THmpNAQ","CAACAgIAAxkBAAELZwFlzaJMBebOVvM71DrqwIvVPMy4KwACYwADQzOdIVf4khZAH3xANAQ","CAACAgIAAxkBAAELZwNlzaJNL3xsfpQtpSLLQEGOJ0G8VgACZAADQzOdIWg9ZrEY53YxNAQ"]
file_log = open("./files/telegram.log", "a+", encoding="utf-8")
token = 'your bot token'
provider_token = '381764678:TEST:78166'  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(token)

prices = [LabeledPrice(label='Working Time Machine', amount=5750), LabeledPrice('Gift wrapping', 500)]

basket = []

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


@bot.message_handler(commands=['start'])
def command_start(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь запустил бота \n")
    file_log.flush()
    bot.send_message(message.chat.id,
                     "Здравствуйте, я демо-торговый бот. Я могу продать вам Машину времени."
                     " Используйте /buy, чтобы заказать один, /terms для условий, отправте выражение для его подсчета, отправте стикер и бот отправит случайную наклейку, или отправте файл и бот сохранит его")



@bot.message_handler(commands=['basket'])
def print_basket(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь выбрал команду /products \n")
    file_log.flush()
    for line in range(len(basket)):
        bot.send_message(message.chat.id,str(line + 1) + " )" + basket[line].label + " -> " + str(basket[line].amount / 100))
@bot.message_handler(commands=['product'])
def print_and_add_products(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь выбрал команду /products \n")
    file_log.flush()
    for line in range(len(prices)):
        markup = types.InlineKeyboardMarkup()
        button_add = types.InlineKeyboardButton(text='+', callback_data=str(line) + "_add")
        button_sub = types.InlineKeyboardButton(text="-", callback_data=str(line) + "_sub")
        markup.add(button_add, button_sub)
        bot.send_message(message.chat.id,str(line + 1) + " )" + prices[line].label + " -> " + str(prices[line].amount/100),reply_markup = markup)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    x = call.data.split("_")
    if x[1] == "add":
        basket.append(prices[int(x[0])])
    elif x[1] == "sub":
        for line_basket in range(len(basket)):
            if basket[line_basket].label == prices[int(x[0])].label:
                basket.pop(line_basket)
                break

@bot.message_handler(commands=['terms'])
def command_terms(message):
    file_log.write("[ " + str(datetime.datetime.now()) + "] " + "Пользователь выбрал команду /terms \n")
    file_log.flush()
    bot.send_message(message.chat.id,
                     'Благодарим вас за покупки с помощью нашего демо-бота. Мы надеемся, что вам понравится ваша новая машина времени!\n'
'1. Если ваша машина времени не была доставлена вовремя, пожалуйста, переосмыслите свое представление о времени и попробуйте еще раз.\n2. Если вы обнаружите, что ваша машина времени не работает, пожалуйста, свяжитесь с нашими будущими сервисными мастерскими на Trappist-1e.Они будут доступны в любом месте в период с мая 2075 года по ноябрь 4000 года н.э.3. Если вы хотите получить возмещение, пожалуйста, подайте заявку на него вчера, и мы немедленно отправим вам его.')
@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Настоящие карты у меня работать не будут, деньги с вашего счета списаны не будут."
                         "Используйте этот номер тестовой карты для оплаты вашей машины времени: `4242 4242 4242 4242 4242`"
                         "\n\nэто ваш демонстрационный счет-фактура:", parse_mode='Markdown')
    bot.send_invoice(
                     message.chat.id,  #chat_id
                     'Покупка', #title
                     "Операция покупки", #description
                     'HAPPY FRIDAYS COUPON', #invoice_payload
                     provider_token, #provider_token
                     'rub', #currency
                     basket, #prices
                     is_flexible=True
                     )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='О, похоже, наши курьеры прямо сейчас обедают. Попробуйте еще раз позже!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Спасибо за оплату! Мы обработаем ваш заказ для `{} {}` как можно быстрее! ' 'Оставайтесь на связи.Воспользуйтесь /buy еще раз, чтобы получить машину времени для своего друга!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    basket.clear()
@bot.message_handler(content_types= ['text'])
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

bot.infinity_polling(skip_pending = True)
