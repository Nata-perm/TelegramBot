import json
import requests
import telebot

from config import CRYPTOCOMPARE_URL, VALUES


class ApiException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote : str, base : str, amount : str):
        if quote not in VALUES:
            raise ApiException(f'Неизвестная валюта: {quote}')
        quote = VALUES[quote]

        if base not in VALUES:
            raise ApiException(f'Неизвестная валюта: {base}')
        base = VALUES[base]

        if quote == base:
            raise ApiException('Невозможно перевести одинаковые валюты')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество: {amount}')

        response = requests.get(f'{CRYPTOCOMPARE_URL}?fsym={quote}&tsyms={base}')

        data = json.loads(response.content)
        rate = data[base]

        return rate * amount
