import requests

from telegram_exceptions import CurrencyException, SameCurrencyError


keys = {
    'доллар': 'usd',
    'евро': 'eur',
    'рубль': 'rub',
}


class CurrencyPrice:

    @staticmethod
    def get_price(base, quote, amount=None):

        try:
            value_base = keys[base.lower()]
        except KeyError:
            raise CurrencyException(f'Валюта {base} не найдена')

        try:
            quote_base = keys[quote.lower()]
        except KeyError:
            raise CurrencyException(f'Валюта {quote} не найдена')

        if value_base == quote_base:
            raise SameCurrencyError(f'Нельзя конвертировать одинаковые валюты {base}, {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise CurrencyException(f'Не удалось обработать количество {amount}!')

        r = requests.get(
            f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{value_base}/{quote_base}.json'
        ).json()
        return r[quote_base] * amount
