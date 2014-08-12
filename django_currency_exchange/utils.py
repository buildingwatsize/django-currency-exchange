from django.conf import settings
from django.core.cache import cache

from moneyed import Money, CURRENCIES
import requests

base_url = "http://openexchangerates.org/api/"


class ExchangeRateSource(object):
    def get_cache_key(self, date_obj):
        return 'currency_exchange:{}'.format(
            date_obj.strftime('%Y-%m-%d')
        )

    def get_exchange_data_for_date(self, date_obj):
        date_string = date_obj.strftime('%Y-%m-%d')
        resp = requests.get(
            "{}historical/{}.json".format(base_url, date_string),
            params={'app_id': settings.OPEN_EXCHANGE_RATES_APP_ID}
        )

        return resp.json()['rates']

    def get_rate_for_date(self, date_obj, source_currency, destination_currency):

        cache_key = self.get_cache_key(date_obj)
        exchange_rates = cache.get(cache_key, False)
        if not exchange_rates:
            exchange_rates = self.get_exchange_data_for_date(date_obj)
            cache.set(cache_key, exchange_rates)

        if source_currency in ('USD', CURRENCIES['USD']):
            lookup_currency = destination_currency
        elif destination_currency in ('USD', CURRENCIES['USD']):
            lookup_currency = source_currency
        else:
            rate_usd_source = exchange_rates[str(source_currency)]
            rate_usd_destination = exchange_rates[str(destination_currency)]
            return (1 / rate_usd_source) * rate_usd_destination

        rate = exchange_rates[str(lookup_currency)]
        if lookup_currency == destination_currency:
            return rate
        else:
            return 1 / rate


def exchange_for_date(date_obj, money, destination_currency):
    rate = ExchangeRateSource().get_rate_for_date(
        date_obj,
        money.currency,
        destination_currency
    )

    return Money(float(money.amount) * rate, currency=destination_currency)
