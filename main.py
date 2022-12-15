import dotenv
import os

from telebot import TeleBot, types

from extensions import CurrencyPrice

from telegram_exceptions import TooManyValuesException, CurrencyException

from extensions import keys


token = dotenv.load_dotenv()

bot = TeleBot(token=os.getenv("TOKEN"))


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: types.Message):
    bot.send_message(message.chat.id,
                     'Введите <имя валюты цену которой он хотите '
                     'узнать> <имя валюты в которой надо узнать цену первой валюты> '
                     '<количество первой валюты> Пример: доллар рубль 1')


@bot.message_handler(commands=['values', ])
def handle_values(message: types.Message):
    text = ""
    for k in keys.keys():
        text = '\n'.join((text, k))
    bot.send_message(message.chat.id, f'Валюты: {text}')


@bot.message_handler(content_types=['text', ])
def handle_values(message: types.Message):
    value = message.text.split(' ')
    try:
        if len(value) != 3:
            raise TooManyValuesException('Не верное кол-во параметров')

        base, quote, amount = value
        price = CurrencyPrice.get_price(base, quote, amount)
    except CurrencyException as e:
        bot.reply_to(message, f"Ошибка в команде: {e}")
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка: {e}')
    else:
        bot.send_message(message.chat.id, str(price))


bot.polling(none_stop=True)
