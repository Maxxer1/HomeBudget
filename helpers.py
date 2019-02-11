import requests
from app import db

# TODO Parametrize function with ip
def get_user_location():
    r = requests.get('http://api.ipstack.com/89.64.42.127?access_key=3d7a1cdae74b6991679f35d39484dc8c')
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


def get_currency_rate(account_currency, foreign_currency):
    r = requests.get('https://api.exchangeratesapi.io/latest?base={}'.format(account_currency))
    data = r.json()
    return data['rates'][foreign_currency]


def convert_balance(account, foreign_currency):
    account.balance = float(account.balance) * foreign_currency
    return account.balance