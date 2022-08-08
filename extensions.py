import requests
import json
from config import CURRENCIES


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Same currencies given.')

        try:
            base_ticker = CURRENCIES[base]
        except KeyError:
            raise APIException(f'Unknown currency {CURRENCIES[base]}')

        try:
            quote_ticker = CURRENCIES[quote]
        except KeyError:
            raise APIException(f'Unknown currency {CURRENCIES[quote]}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Wrong amount {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')

        return float(json.loads(r.content)[CURRENCIES[quote]]) * amount
