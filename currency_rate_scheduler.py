from apscheduler.schedulers.background import BackgroundScheduler
import requests

rates = {}

def get_currency_rates():
    r = requests.get('https://api.exchangeratesapi.io/latest?base=PLN')
    currency_rates = r.json()
    print(currency_rates)
    return currency_rates
    
if not rates:
    rates = get_currency_rates()

def get_currency_rate_date(rates=rates):
    '''Returns date of currency rates'''
    return rates['date']

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(get_currency_rates, 'interval', hours=3)
scheduler.start()
