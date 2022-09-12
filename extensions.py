import requests
import json
from config import *


class APIExceptions(Exception):
    pass


class Convertation:
    @staticmethod
    def get_price(base, quot, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIExceptions(f"Валюта {base} отсутствует."
                                f" Для получения доступных валют введите в сообщении '/value'")

        try:
            quot_key = keys[quot.lower()]
        except KeyError:
            raise APIExceptions(f"Валюта {quot} отсутствует."
                                f" Для получения доступных валют введите в сообщении '/value'")

        if base_key == quot_key:
            raise APIExceptions("Конвертация одинаковых валют невозможна!"
                                " Для получения доступных валют введите в сообщении '/value'")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIExceptions(f"Сумма {amount} не может быть сконвертирована.")

        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?symbols={quot_key}&base={base_key}",
                         headers=api_key)
        result = json.loads(r.content)
        new_price = result['rates'][quot_key] * float(amount)
        return round(new_price, 2)
