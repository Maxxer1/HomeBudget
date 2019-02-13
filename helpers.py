import requests
from app import db
from currency_rate_scheduler import rates

# TODO Parametrize function with ip


def get_user_location():
    r = requests.get(
        'http://api.ipstack.com/89.64.42.127?access_key=3d7a1cdae74b6991679f35d39484dc8c')
    data = r.json()
    return data['city'], data['country_name']


def calculate_total_balance(accounts):
    total_balance = 0.0
    for account in accounts:
        total_balance += account.balance
    return total_balance


def lower_balance(account, expense):
    account.balance = account.balance - float(expense.ammout)
    return account.balance


def increment_balance(account, income):
    account.balance = account.balance + float(income.ammout)
    return account.balance


def convert_from_euro(account, rates, foreign_currency):
    euro_rate = rates['rates']['EUR']
    usd_rate = rates['rates']['USD']
    gbp_rate = rates['rates']['GBP']
    if foreign_currency == 'PLN':
        account.balance = float(account.balance) / euro_rate
    elif foreign_currency == 'USD':
        account.balance = float(account.balance) * (euro_rate / usd_rate)
    elif foreign_currency == 'GBP':
        account.balance = float(account.balance) * (euro_rate / gbp_rate)
    return round(account.balance, 2)


def convert_from_usd(account, rates, foreign_currency):
    euro_rate = rates['rates']['EUR']
    usd_rate = rates['rates']['USD']
    gbp_rate = rates['rates']['GBP']
    if foreign_currency == 'PLN':
        account.balance = float(account.balance) / usd_rate
    elif foreign_currency == 'EUR':
        account.balance = float(account.balance) * (usd_rate / euro_rate)
    elif foreign_currency == 'GBP':
        account.balance = float(account.balance) * (gbp_rate / usd_rate)
    return round(account.balance, 2)


def convert_from_gbp(account, rates, foreign_currency):
    euro_rate = rates['rates']['EUR']
    usd_rate = rates['rates']['USD']
    gbp_rate = rates['rates']['GBP']
    if foreign_currency == 'PLN':
        account.balance = float(account.balance) / gbp_rate
    elif foreign_currency == 'EUR':
        account.balance = float(account.balance) * (gbp_rate / euro_rate)
    elif foreign_currency == 'USD':
        account.balance = float(account.balance) * (gbp_rate / usd_rate)
    return round(account.balance, 2)


def convert_from_pln(account, rates, foreign_currency):
    euro_rate = rates['rates']['EUR']
    usd_rate = rates['rates']['USD']
    gbp_rate = rates['rates']['GBP']
    if foreign_currency == 'EUR':
        account.balance = float(account.balance) * euro_rate
    elif foreign_currency == 'USD':
        account.balance = float(account.balance) * usd_rate
    elif foreign_currency == 'GBP':
        account.balance = float(account.balance) * gbp_rate
    return round(account.balance, 2)


def convert_balance(account, foreign_currency, rates=rates):
    '''Converts balance of single account to desired currency'''
    if account.currency == 'EUR':
        account.balance = convert_from_euro(account, rates, foreign_currency)
    elif account.currency == 'USD':
        account.balance = convert_from_usd(account, rates, foreign_currency)
    elif account.currency == 'GBP':
        account.balance = convert_from_gbp(account, rates, foreign_currency)
    elif account.currency == 'PLN':
        account.balance = convert_from_pln(account, rates, foreign_currency)
    return account.balance


def convert_total_balance(accounts, foreign_currency):
    '''Returns total balance of an account after currency exchange'''
    for account in accounts:
        convert_balance(account, foreign_currency)
    return round(calculate_total_balance(accounts), 2)


def get_currency_rate_date(rates=rates):
    '''Returns date of currency rates'''
    return rates['date']