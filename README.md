# django-currency-exchange
========================
Utilities which thinly wrap around the openexchangerates.org API.
Uses caching so that we don't exceed our API quota.

## Usage
Use `utils.exchange_for_date()` to get a Money instance of desired currency

## Developer notes
To convert from one non-USD source to another, we must convert via USD. This is because base exchange rates in openexchangerates.org can only be changed with an Enterprise account (we currently use a Developer account)
