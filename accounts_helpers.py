from time import time
def calculate_total_balance(accounts):
    '''Calculates total balance in all user accounts'''
    total_balance = 0.0
    for account in accounts:
        total_balance += account.balance
    return round(total_balance, 2)

def convert_total_balance(accounts, foreign_currency):
    '''Returns total balance of an account after currency exchange'''
    for account in accounts:
        account.convert_balance(foreign_currency)
        account.currency = foreign_currency
    return calculate_total_balance(accounts)
