import json
import requests
import telebot

from config import TELEGRAM_TOKEN, VALUES
from extensions import CryptoConverter, ApiException


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество пеерводимой валюты>\n\
Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def help(message):
    text = 'Доступные валюты:\n' + '\n'.join(VALUES.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ApiException('Слишком много параметров')
        if len(values) < 3:
            raise ApiException('Слишком мало параметров')

        quote, base, amount = values

        total_base = CryptoConverter.get_price(quote, base, amount)
        text = f'Цена {amount} {quote} в {base} = {total_base}'

        bot.reply_to(message, text)
    except ApiException as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.infinity_polling()
