def calculate_total_balance(accounts):
    '''Calculates total balance in all user accounts'''
    total_balance = 0.0
    for account in accounts:
        total_balance += account.balance
    return total_balance

def convert_total_balance(accounts, foreign_currency):
    '''Returns total balance of an account after currency exchange'''
    for account in accounts:
        account.convert_balance(foreign_currency)
        account.currency = foreign_currency
    return round(calculate_total_balance(accounts), 2)