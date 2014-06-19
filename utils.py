from django.conf import settings

from moneyed import Money, CURRENCIES
import requests

base_url = "http://openexchangerates.org/api/"


def exchange_for_date(date_obj, money, destination_currency):
    if money.currency in ('USD', CURRENCIES['USD']):
        lookup_currency = destination_currency
    elif destination_currency  in ('USD', CURRENCIES['USD']):
        lookup_currency = money.currency
    else:
        raise Exception("One side of the exchange must be USD")

    date_string = date_obj.strftime('%Y-%m-%d')

    resp = requests.get(
        "{}historical/{}.json".format(base_url, date_string),
        params={'app_id': settings.OPEN_EXCHANGE_RATES_APP_ID}
    )

    exchange_rates = resp.json()['rates']

    rate = exchange_rates[str(lookup_currency)]

    if lookup_currency == destination_currency:
        return Money(float(money * rate), currency=destination_currency)
    else:
        return Money(float(money * (1 / rate)), currency=destination_currency)
